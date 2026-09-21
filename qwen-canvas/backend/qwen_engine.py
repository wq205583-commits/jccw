import gc
import os
import random
import torch
from PIL import Image
from diffusers import QwenImage21Pipeline

MODEL_ID = os.getenv("QWEN_MODEL", "Qwen/Qwen-Image-2.1")

class QwenEngine:
    def __init__(self):
        self.pipe = None

    def load(self):
        if self.pipe is None:
            self.pipe = QwenImage21Pipeline.from_pretrained(
                MODEL_ID, torch_dtype=torch.bfloat16
            )
            # RTX 4080 16GB: keep the full model from permanently occupying VRAM.
            self.pipe.enable_model_cpu_offload()
        return self.pipe

    def generate(self, prompt, width=1024, height=1024, steps=30, seed=-1, images=None):
        pipe = self.load()
        seed = random.randint(0, 2**31 - 1) if seed < 0 else seed
        generator = torch.Generator("cuda").manual_seed(seed)
        kwargs = dict(
            prompt=prompt, width=width, height=height,
            num_inference_steps=steps, generator=generator
        )
        if images:
            kwargs["image"] = images[0] if len(images) == 1 else images
        try:
            result = pipe(**kwargs).images[0]
            return result, seed
        except torch.OutOfMemoryError:
            torch.cuda.empty_cache()
            gc.collect()
            raise RuntimeError("GPU显存不足。请降低分辨率/参考图数量后重试。")

engine = QwenEngine()
