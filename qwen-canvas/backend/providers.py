import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

SYSTEM = """You are the prompt director inside a professional AI image canvas. Rewrite the user's Chinese or English request into a precise production prompt for image generation/editing. Preserve identities and constraints explicitly requested. Return only the improved prompt, no commentary."""

def enhance(provider: str, prompt: str) -> str:
    if provider == "openai":
        from openai import OpenAI
        key=os.getenv("OPENAI_API_KEY")
        if not key: raise RuntimeError("未配置 OPENAI_API_KEY，请在 qwen-canvas/.env 中填写。")
        client=OpenAI(api_key=key)
        r=client.responses.create(model=os.getenv("OPENAI_MODEL","gpt-5.6-luna"),instructions=SYSTEM,input=prompt)
        return r.output_text.strip()
    if provider == "gemini":
        from google import genai
        from google.genai import types
        key=os.getenv("GEMINI_API_KEY")
        if not key: raise RuntimeError("未配置 GEMINI_API_KEY，请在 qwen-canvas/.env 中填写。")
        client=genai.Client(api_key=key)
        r=client.models.generate_content(model=os.getenv("GEMINI_MODEL","gemini-3.8-flash"),contents=prompt,config=types.GenerateContentConfig(system_instruction=SYSTEM))
        return (r.text or "").strip()
    return prompt

def status():
    return {"qwen":True,"openai":bool(os.getenv("OPENAI_API_KEY")),"gemini":bool(os.getenv("GEMINI_API_KEY"))}
