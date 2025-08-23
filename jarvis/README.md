# Jarvis-like Local Voice Assistant (Windows 10)

A minimal local assistant that runs fully on your PC using:
- STT: faster-whisper (offline)
- LLM: Ollama (local model, e.g., qwen2.5)
- TTS: Piper (offline)

## 1) Prerequisites (Windows 10)

- Python 3.10+ x64
- [Ollama for Windows](https://ollama.com/download/windows)
  - After install, open PowerShell and pull a multilingual model:
    ```powershell
    ollama pull qwen2.5:7b
    ```
- FFmpeg (audio tooling)
  - If you have Chocolatey:
    ```powershell
    choco install ffmpeg -y
    ```
  - Or install manually from the official site and add to PATH.
- Piper (TTS) for Windows
  - Download `piper.exe` from the [Piper releases](https://github.com/rhasspy/piper/releases)
  - Download a voice model (for Persian or English). Example voices:
    - Persian (Farsi): `fa_IR-mls_2-low.onnx` from the [voice list](https://github.com/rhasspy/piper/blob/master/VOICES.md)
    - English (US): `en_US-amy-low.onnx`

## 2) Project Setup

1. Clone or copy this folder to your Windows machine.
2. Open PowerShell in the project directory and create a virtual environment:
   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Configure environment by copying `.env.example` to `.env` and updating values:
   - `OLLAMA_MODEL` (default `qwen2.5:7b`)
   - `PIPER_EXE` path to your `piper.exe`
   - `VOICE_PATH` path to your `.onnx` voice file
   - Optional: `STT_MODEL` (`small`, `medium`, etc.)

## 3) Run Ollama

Start the Ollama service (if not already running) and ensure the model is present:
```powershell
ollama serve
# In another terminal
ollama run qwen2.5:7b
```

## 4) Run the Assistant

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

- By default, it records 5 seconds from the microphone per turn.
- You can also type instead of speaking; just enter your message at the prompt.
- The assistant will optionally execute a few safe Windows actions (opening apps/URLs) via a strict allowlist.

## 5) Configuration

See `.env.example` for all options. Key settings:
- `OLLAMA_HOST`: `http://127.0.0.1:11434`
- `OLLAMA_MODEL`: `qwen2.5:7b`
- `STT_MODEL`: Whisper model size (e.g., `small`)
- `PIPER_EXE`: Full path to `piper.exe`
- `VOICE_PATH`: Full path to voice `.onnx`
- `SAMPLE_RATE`: `16000`

## 6) Notes

- For best Persian support, `qwen2.5:7b` works well locally.
- If audio libraries fail to build, use a recent Python and upgrade `pip`.
- Make sure your microphone is selected as default recording device in Windows.

## 7) Next Steps

- Add hotword detection (e.g., Porcupine or open-source alternatives)
- Continuous listening with VAD and barge-in
- Calendar, email, and desktop automation integrations
- Rich tool calling with confirmation flows