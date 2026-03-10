import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY") or os.getenv("NIM_API_KEY") or ""
NIM_BASE_URL   = os.getenv("NIM_BASE_URL", "https://integrate.api.nvidia.com/v1")
NIM_LLM_MODEL  = os.getenv("NIM_LLM_MODEL", "meta/llama-3.1-8b-instruct")

if not NVIDIA_API_KEY:
    raise RuntimeError("Missing NVIDIA_API_KEY env var. Get it from build.nvidia.com -> API Keys.")

CHAT_URL = NIM_BASE_URL.rstrip("/") + "/chat/completions"

app = FastAPI(title="NVIDIA NIM Voice Gateway")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatIn(BaseModel):
    text: str

class ChatOut(BaseModel):
    reply: str

@app.get("/")
def root():
    return {"service": "nim-gateway", "status": "ok", "model": NIM_LLM_MODEL}

@app.post("/chat", response_model=ChatOut)
def chat(body: ChatIn):
    text = (body.text or "").strip()
    if not text:
        return {"reply": ""}

    payload = {
        "model": NIM_LLM_MODEL,
        "messages": [
            {"role": "system", "content": "You are a concise, helpful assistant."},
