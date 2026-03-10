
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# OpenAI SDK can point to NVIDIA NIM (OpenAI-compatible) by changing base_url
from openai import OpenAI

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY") or os.getenv("NIM_API_KEY") or ""
NIM_BASE_URL = os.getenv("NIM_BASE_URL", "https://integrate.api.nvidia.com/v1")
NIM_LLM_MODEL = os.getenv("NIM_LLM_MODEL", "meta/llama-3.1-8b-instruct")

if not NVIDIA_API_KEY:
    raise RuntimeError("Missing NVIDIA_API_KEY env var. Get it from build.nvidia.com → API Keys.")

client = OpenAI(api_key=NVIDIA_API_KEY, base_url=NIM_BASE_URL)

class ChatIn(BaseModel):
    text: str

class ChatOut(BaseModel):
    reply: str

app = FastAPI(title="NVIDIA NIM Voice Gateway (Chat endpoint)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"service": "nim-gateway", "status": "ok", "model": NIM_LLM_MODEL}

@app.post("/chat", response_model=ChatOut)
async def chat(body: ChatIn):
    prompt = body.text.strip()
    if not prompt:
        return {"reply": ""}
    # Call NVIDIA NIM via OpenAI-compatible Chat Completions
    r = client.chat.completions.create(
        model=NIM_LLM_MODEL,
        messages=[{"role": "system", "content": "You are a concise helpful assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=300,
    )
    out = r.choices[0].message.content
    return {"reply": out}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
