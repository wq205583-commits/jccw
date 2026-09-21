import io
import os
import uuid
from typing import List
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from PIL import Image
from qwen_engine import engine

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(ROOT, "outputs")
os.makedirs(OUTPUT, exist_ok=True)

app = FastAPI(title="Qwen Canvas API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
def health():
    return {"ok": True, "model": "Qwen/Qwen-Image-2.1"}

@app.post("/api/generate")
async def generate(
    prompt: str = Form(...), width: int = Form(1024), height: int = Form(1024),
    steps: int = Form(30), seed: int = Form(-1),
    images: List[UploadFile] = File(default=[])
):
    refs = []
    for f in images[:10]:
        refs.append(Image.open(io.BytesIO(await f.read())).convert("RGBA"))
    image, used_seed = engine.generate(prompt, width, height, steps, seed, refs)
    name = f"{uuid.uuid4().hex}.png"
    path = os.path.join(OUTPUT, name)
    image.save(path)
    return {"url": f"/api/output/{name}", "seed": used_seed}

@app.get("/api/output/{name}")
def output(name: str):
    return FileResponse(os.path.join(OUTPUT, os.path.basename(name)), media_type="image/png")
