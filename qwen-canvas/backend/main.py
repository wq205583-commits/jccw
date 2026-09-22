import io,os,uuid,base64
from typing import List
from fastapi import FastAPI,UploadFile,File,Form,Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from PIL import Image
from qwen_engine import engine
from providers import enhance,status
from project_store import save,load,list_projects
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUTPUT=os.path.join(ROOT,"outputs");os.makedirs(OUTPUT,exist_ok=True)
app=FastAPI(title="Qwen Canvas API");app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
@app.get("/api/health")
def health():return {"ok":True,"model":"Qwen/Qwen-Image-2.1","providers":status()}
@app.post("/api/enhance")
def prompt_enhance(provider:str=Form(...),prompt:str=Form(...)):
 try:return {"prompt":enhance(provider,prompt)}
 except Exception as e:return {"error":str(e)}
@app.get("/api/projects")
def projects():return {"projects":list_projects()}
@app.post("/api/projects/{name}")
def save_project(name:str,data:dict=Body(...)):return {"file":save(name,data)}
@app.get("/api/projects/{name}")
def load_project(name:str):
 try:return load(name.replace(".json",""))
 except Exception as e:return {"error":str(e)}
@app.post("/api/generate")
async def generate(prompt:str=Form(...),mode:str=Form("generate"),width:int=Form(1024),height:int=Form(1024),steps:int=Form(20),seed:int=Form(-1),transparent:bool=Form(False),images:List[UploadFile]=File(default=[])):
 refs=[]
 for f in images[:10]:refs.append(Image.open(io.BytesIO(await f.read())).convert("RGBA"))
 if transparent and "RGBA image with transparency" not in prompt:prompt=f"This is an RGBA image with transparency. {prompt}. The image has alpha channel and the background is transparent."
 if mode=="edit" and not refs:return {"error":"图片编辑模式至少需要 1 张参考图"}
 try:
  image,used_seed=engine.generate(prompt,width,height,steps,seed,refs);name=f"{uuid.uuid4().hex}.png";image.save(os.path.join(OUTPUT,name));return {"url":f"/api/output/{name}","seed":used_seed,"mode":mode,"references":len(refs)}
 except Exception as e:return {"error":str(e)}
@app.get("/api/output/{name}")
def output(name:str):return FileResponse(os.path.join(OUTPUT,os.path.basename(name)),media_type="image/png")


# OpenAI-compatible image endpoints for Infinite Canvas.
def _parse_size(size: str):
    try:
        w,h=(size or "1024x1024").lower().split("x",1)
        return int(w),int(h)
    except Exception:
        return 1024,1024

def _b64_image(image):
    buf=io.BytesIO(); image.save(buf,format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")

@app.post("/v1/images/generations")
async def openai_image_generate(payload:dict=Body(...)):
    prompt=str(payload.get("prompt","")).strip()
    width,height=_parse_size(str(payload.get("size","1024x1024")))
    count=max(1,min(int(payload.get("n",1) or 1),4))
    transparent=payload.get("background")=="transparent"
    if transparent and "RGBA image with transparency" not in prompt:
        prompt=f"This is an RGBA image with transparency. {prompt}. The image has alpha channel and the background is transparent."
    try:
        data=[]
        for _ in range(count):
            image,_seed=engine.generate(prompt,width,height,20,-1,[])
            data.append({"b64_json":_b64_image(image)})
        return {"created":0,"data":data}
    except Exception as e:
        return {"error":{"message":str(e)}}

@app.post("/v1/images/edits")
async def openai_image_edit(
    prompt:str=Form(...), model:str=Form("Qwen-Image-2.1"),
    n:int=Form(1), size:str=Form("1024x1024"),
    background:str=Form("auto"),
    image:List[UploadFile]=File(default=[]),
    images:List[UploadFile]=File(default=[],alias="image[]")
):
    files=(image or [])+(images or [])
    refs=[]
    for f in files[:10]:
        refs.append(Image.open(io.BytesIO(await f.read())).convert("RGBA"))
    if not refs:return {"error":{"message":"Image editing requires at least one reference image."}}
    width,height=_parse_size(size)
    if background=="transparent" and "RGBA image with transparency" not in prompt:
        prompt=f"This is an RGBA image with transparency. {prompt}. The image has alpha channel and the background is transparent."
    try:
        data=[]
        for _ in range(max(1,min(n,4))):
            out,_seed=engine.generate(prompt,width,height,20,-1,refs)
            data.append({"b64_json":_b64_image(out)})
        return {"created":0,"data":data}
    except Exception as e:
        return {"error":{"message":str(e)}}
