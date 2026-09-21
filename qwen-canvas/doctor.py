import sys,subprocess,urllib.request
print("Qwen Canvas Doctor")
print("Python:",sys.version.split()[0])
try:
 import torch
 print("PyTorch:",torch.__version__,"CUDA:",torch.cuda.is_available())
 if torch.cuda.is_available(): print("GPU:",torch.cuda.get_device_name(0),"VRAM(GB):",round(torch.cuda.get_device_properties(0).total_memory/1024**3,1))
except Exception as e: print("PyTorch ERROR:",e)
for m in ["fastapi","diffusers","transformers","accelerate","openai","google.genai"]:
 try:__import__(m);print("[OK]",m)
 except Exception as e:print("[X]",m,e)
try:print("Backend:",urllib.request.urlopen("http://127.0.0.1:8000/api/health",timeout=2).read().decode())
except Exception as e:print("Backend not running:",e)
input("\nPress Enter to close...")
