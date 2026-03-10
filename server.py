import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# --- Environment ---
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY") or os.getenv("NIM_API_KEY") or ""
NIM_BASE_URL   = os.getenv("NIM_BASE_URL", "https://integrate.api.nvidia.com/v1")
NIM_LLM_MODEL  = os.getenv("NIM_LLM_MODEL", "meta/llama-3.1-8b-instruct")

if not NVIDIA_API_KEY:
    raise RuntimeError("Missing NVIDIA_API_KEY env var. Get it from build.nvidia.com → API Keys.")

CHAT_URL = NIM_BASE_URL.rstrip("/") + "/chat/completions"
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")

# --- App ---
app = FastAPI(title="NVIDIA NIM Voice Gateway")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount /public only if the folder exists (prevents startup crash)
if os.path.isdir(PUBLIC_DIR):
    app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")

class ChatIn(BaseModel):
    text: str

class ChatOut(BaseModel):
    reply: str

# Root: serve web client if present, else JSON status
@app.get("/", include_in_schema=False)
def root():
    index_path = os.path.join(PUBLIC_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path, media_type="text/html")
    return {"service": "nim-gateway", "status": "ok", "model": NIM_LLM_MODEL}

# Chat endpoint → NVIDIA NIM (OpenAI-compatible)
@app.post("/chat", response_model=ChatOut)
def chat(body: ChatIn):
    text = (body.text or "").strip()
    if not text:
        return {"reply": ""}

    payload = {
        "model": NIM_LLM_MODEL,
        "messages": [
            {"role": "system", "content": "You are a concise, helpful assistant."},
            {"role": "user",   "content": text}
        ],
        "temperature": 0.6,
        "max_tokens": 300
    }
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }

    resp = requests.post(CHAT_URL, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    # OpenAI-compatible shape
    try:
        reply = data["choices"][0]["message"]["content"]
    except Exception:
        reply = str(data)

    return {"reply": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")
if os.path.isdir(PUBLIC_DIR):
    app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")

@app.get("/", include_in_schema=False)
def root():
    index_path = os.path.join(PUBLIC_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path, media_type="text/html")
    return {"service": "nim-gateway", "status": "ok", "model": NIM_LLM_MODEL}
