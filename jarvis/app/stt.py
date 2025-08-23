from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
from faster_whisper import WhisperModel


class SpeechToText:
	def __init__(self, model_size: str = "small", device: str = "auto"):
		self.model = WhisperModel(model_size, device=device, compute_type="int8")

	def transcribe(self, audio_np: np.ndarray, sample_rate: int) -> str:
		if audio_np.size == 0:
			return ""
		# faster-whisper expects mono float32 in range [-1,1]
		if audio_np.ndim > 1:
			audio_np = audio_np[:, 0]
		audio_np = audio_np.astype("float32")
		segments, _ = self.model.transcribe(audio_np, language=None)
		text_parts: list[str] = []
		for seg in segments:
			text_parts.append(seg.text)
		return " ".join(text_parts).strip()