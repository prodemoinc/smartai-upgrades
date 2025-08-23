from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(slots=True)
class Settings:
	ollama_host: str
	ollama_model: str
	stt_model: str
	sample_rate: int
	channels: int
	piper_exe: str
	voice_path: str
	data_dir: Path


def load_settings() -> Settings:
	project_root = Path(__file__).resolve().parents[1]
	data_dir = project_root / "data"
	os.makedirs(data_dir, exist_ok=True)

	ollama_host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
	ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
	stt_model = os.getenv("STT_MODEL", "small")
	sample_rate = int(os.getenv("SAMPLE_RATE", "16000"))
	channels = int(os.getenv("CHANNELS", "1"))
	piper_exe = os.getenv("PIPER_EXE", "")
	voice_path = os.getenv("VOICE_PATH", "")

	return Settings(
		ollama_host=ollama_host,
		ollama_model=ollama_model,
		stt_model=stt_model,
		sample_rate=sample_rate,
		channels=channels,
		piper_exe=piper_exe,
		voice_path=voice_path,
		data_dir=data_dir,
	)