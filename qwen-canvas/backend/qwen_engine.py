import gc,os,random,torch
from diffusers import QwenImage21Pipeline
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_MODEL=os.path.join(ROOT,"models","Qwen-Image-2.1")
def model_source():
 configured=os.getenv("QWEN_MODEL","").strip()
 if configured:return configured
 if os.path.isfile(os.path.join(LOCAL_MODEL,"model_index.json")):return LOCAL_MODEL
 return "Qwen/Qwen-Image-2.1"
class QwenEngine:
 def __init__(self):self.pipe=None
 def load(self):
  if self.pipe is None:
   if not torch.cuda.is_available():raise RuntimeError("CUDA unavailable. Run check.bat and verify the NVIDIA PyTorch installation.")
   source=model_source();print("[Qwen Canvas] Loading model:",source)
   self.pipe=QwenImage21Pipeline.from_pretrained(source,torch_dtype=torch.bfloat16,local_files_only=os.path.isdir(source))
   self.pipe.enable_model_cpu_offload()
  return self.pipe
 def generate(self,prompt,width=1024,height=1024,steps=30,seed=-1,images=None):
  pipe=self.load();seed=random.randint(0,2**31-1) if seed<0 else seed;g=torch.Generator("cuda").manual_seed(seed)
  kw=dict(prompt=prompt,width=width,height=height,num_inference_steps=steps,generator=g)
  if images:kw["image"]=images[0] if len(images)==1 else images
  try:return pipe(**kw).images[0],seed
  except torch.OutOfMemoryError:
   torch.cuda.empty_cache();gc.collect()
   if width>1024 or height>1024:
    scale=min(1024/width,1024/height);kw["width"]=max(512,int(width*scale)//32*32);kw["height"]=max(512,int(height*scale)//32*32)
    try:return pipe(**kw).images[0],seed
    except torch.OutOfMemoryError:torch.cuda.empty_cache();gc.collect()
   raise RuntimeError("RTX 显存不足：已自动尝试降低工作分辨率，仍失败。请减少参考图或使用 1K。")
engine=QwenEngine()
