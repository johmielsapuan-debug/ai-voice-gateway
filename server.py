import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse          # NEW ⚠️
from fastapi.staticfiles import StaticFiles         # NEW ⚠️

# ... keep your NVIDIA_API_KEY / NIM_* code as-is ...

app = FastAPI(title="NVIDIA NIM Voice Gateway")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# (optional) expose /public/ so assets load if you add any
app.mount("/public", StaticFiles(directory="public"), name="public")   # NEW (safe)

class ChatIn(BaseModel):
    text: str

class ChatOut(BaseModel):
    reply: str

# ✅ Render the Web Client if public/index.html exists; otherwise show JSON status
@app.get("/", include_in_schema=False)
def root():
    index_path = os.path.join(os.path.dirname(__file__), "public", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
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

    try:
        reply = data["choices"][0]["message"]["content"]
    except Exception:
        reply = str(data)

    return {"reply": reply}
