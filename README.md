
# NVIDIA NIM Voice Gateway (Chat-only)

This gateway exposes **/chat** that calls **NVIDIA NIM** using its **OpenAI-compatible** API at `https://integrate.api.nvidia.com/v1` with your `NVIDIA_API_KEY`. It pairs with the provided **Web Client v2** which handles microphone (STT) and speaker (TTS) in the **browser**.

> NIM provides OpenAI-compatible endpoints like **/v1/chat/completions** for LLMs. You can point the OpenAI SDK to `integrate.api.nvidia.com/v1` and use a NIM model name (e.g., `meta/llama-3.1-8b-instruct`). citeturn42search25turn42search26

> NVIDIA confirms you can build a real-time voice agent stack with **NIM (STT, LLM, TTS)** and frameworks like **Pipecat**; developers report a **free tier** with **no credit card** and **~40 requests/min** for demos. citeturn42search31

## Environment
Create a `.env` (or set Render Environment vars):

```
NVIDIA_API_KEY=nvapi-...   # from https://build.nvidia.com (profile → API Keys)
NIM_BASE_URL=https://integrate.api.nvidia.com/v1
NIM_LLM_MODEL=meta/llama-3.1-8b-instruct
```

## Run locally
```bash
pip install -r requirements.txt
python server.py
# → http://localhost:10000
```

## Deploy on Render (Free)
1. Push this folder to GitHub
2. Render → New Web Service → **Docker** → Instance Type **Free**
3. Add environment variables above → Save, Rebuild & Deploy

## API
```http
POST /chat
Content-Type: application/json
{
  "text": "Say hello in one sentence."
}
→ { "reply": "Hello! ..." }
```

## Notes
- This gateway keeps **voice** on the client using browser STT/TTS APIs for **zero cost** and **no extra keys**.
- You can later swap in **NIM Speech (Riva) ASR/TTS** for server-side audio: see the NIM Speech tutorials and Pipecat NVIDIA services. citeturn42search33turn42search34turn42search28
