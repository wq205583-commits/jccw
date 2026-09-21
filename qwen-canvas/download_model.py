import os
from huggingface_hub import snapshot_download
ROOT=os.path.dirname(os.path.abspath(__file__))
target=os.path.join(ROOT,"models","Qwen-Image-2.1")
os.makedirs(target,exist_ok=True)
print("Downloading Qwen/Qwen-Image-2.1")
print("Target:",target)
snapshot_download(repo_id="Qwen/Qwen-Image-2.1",local_dir=target,token=os.getenv("HF_TOKEN") or None)
print("DONE:",target)
