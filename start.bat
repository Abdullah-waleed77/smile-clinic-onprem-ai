@echo off
echo Starting Smile Clinic Assistant...
start "Ollama - Doctor" ollama serve
timeout /t 5
cd /d C:\clinic
start "Guard" python guard.py
echo Done! Open http://localhost:8080