# 🦷 Smile Clinic AI Assistant — On-Premise LLM (Demo Project)

A private AI assistant for a dental clinic that runs **fully offline, on the clinic's own computer**.
Patient data never leaves the building.

> ⚠️ This is a **demo / learning project**. "Smile Dental Clinic" is a fictional client used to practise a real-world on-premise AI deployment end to end.

## 🎬 Demo video
https://github.com/user-attachments/assets/12f9cd2c-00de-4980-9349-36820e29366f



---

## The problem

A small clinic wants a ChatGPT-like assistant so reception staff can answer patient questions (prices, working hours) quickly.
But patient information is private and **must not be sent to cloud AI services**.

## The solution

Run an open-source model (**Qwen**) on a local machine with **Ollama**, give it the clinic's information, and let staff use it from a browser on the clinic's Wi-Fi — protected by a password.

---

## Architecture

```
📱 Staff device (browser)
        │  clinic Wi-Fi
        ▼
💂 Guard (Python, port 8080)    ← open to the local network, password check + access log
        │
        ▼
⚙️ Ollama API (port 11434)      ← closed to the network, localhost only
        │
        ▼
🧠 Qwen model + clinic info     ← answers only from the clinic's information
```

### Design decisions

| Question | Decision | Why |
|---|---|---|
| Concurrent users | 3–5 | 10 staff, but not everyone uses it at the same time |
| Model size | Qwen ~14B (production) / 3B (this demo) | Good Arabic + reliable answers at a reasonable cost |
| Hardware | Desktop with NVIDIA GPU, 16 GB VRAM | 14B × ~0.7 GB ≈ 10 GB, leaving room for several users |
| Access | Browser chat page → API, internal network only | No software to install; data stays inside the clinic |
| Clinic knowledge | Instructions + clinic info file given to the model | Easy to update prices without retraining |

### Hardware test (demo laptop)
- Intel i5 (11th gen), 8 GB RAM, no usable GPU → model ran on CPU
- Measured speed: **~9.5 tokens/second** with Qwen2.5 3B
- Conclusion: fine for one user and testing; a real clinic needs a GPU machine

---

## Features

- ✅ Runs **100% offline**
- ✅ Answers **only** from clinic information — refuses to invent prices
- ✅ Replies in the patient's language (Arabic / English)
- ✅ Web chat page usable from any device on the clinic network
- ✅ Password-protected access, every attempt logged (`ALLOWED` / `BLOCKED`)
- ✅ Starts automatically when the computer boots
- ✅ Operations & troubleshooting guide for clinic staff

---

## Files

| File | Purpose |
|---|---|
| `clinic.txt` | Ollama Modelfile: base model, temperature, clinic information and rules |
| `guard.py` | Password guard + serves the chat page + forwards questions to Ollama |
| `chat.html` | Chat interface (RTL, mobile friendly) |
| `start.bat` | Starts Ollama and the guard with one click (placed in Windows Startup) |
| `GUIDE.txt` | Staff guide: how to use, update prices, and troubleshoot |

---

## How to run

1. Install [Ollama](https://ollama.com/download)
2. Download the model:
   ```
   ollama pull qwen2.5:3b
   ```
3. Build the clinic assistant:
   ```
   ollama create clinic -f clinic.txt
   ```
4. Set your own password in `guard.py` (`PASSWORD = "CHANGE_ME"`)
5. Start everything:
   ```
   start.bat
   ```
6. Open `http://localhost:8080` (or `http://<computer-ip>:8080` from another device on the same network)

---

## Testing

| Test | Expected result | Result |
|---|---|---|
| "How much is teeth cleaning?" | 200 AED | ✅ |
| Question in Arabic | Answer in Arabic | ✅ |
| "Are you open on Friday?" | Closed | ✅ |
| "How much is a root canal?" (not in the info) | Does not invent — asks to call the clinic | ✅ |
| Wrong password | Blocked + logged | ✅ |
| Access from a phone on the same Wi-Fi | Works through the guard only | ✅ |
| Direct access to Ollama from the phone | Refused | ✅ |

---

## Production readiness assessment

| Check | Status |
|---|---|
| Correct, grounded answers | ✅ |
| Access control | ✅ |
| Auto-start after reboot | ✅ |
| Handles 3–5 users at once | ❌ needs GPU hardware |
| Auto-restart if a process crashes (run as a service) | ❌ |
| Monitoring / alerts | ❌ |
| Backups of configuration files | ❌ |

**Verdict:** ready for a pilot, not yet for full production.

## Security recommendations

1. Keep Ollama bound to localhost; all access goes through the guard ✅
2. Require a password on every request ✅
3. Log every access attempt ✅
4. Ground the model in clinic data only ✅
5. Use **HTTPS** between staff devices and the guard
6. Store the password outside the code and rotate it regularly
7. Rate-limit requests per user
8. Separate the staff Wi-Fi from the guest Wi-Fi

---

## Skills demonstrated

On-premise LLM architecture · Model-serving deployment (Ollama) · Qwen installation & configuration · Inference API exposure · LLM platform security · Production readiness assessment · Documentation & knowledge transfer · Troubleshooting / support

---

**Author:** Abdulla Waleed Khaled
