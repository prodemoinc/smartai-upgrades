from __future__ import annotations

import queue
import time
from typing import Optional

import numpy as np
import sounddevice as sd
import soundfile as sf
import simpleaudio as sa


class AudioIO:
	def __init__(self, sample_rate: int = 16000, channels: int = 1):
		self.sample_rate = sample_rate
		self.channels = channels

	def record_seconds(self, seconds: float = 5.0) -> np.ndarray:
		q: queue.Queue[np.ndarray] = queue.Queue()

		def _callback(indata, frames, time_info, status):
			if status:
				print(f"Audio status: {status}")
			q.put(indata.copy())

		with sd.InputStream(
			samplerate=self.sample_rate,
			channels=self.channels,
			dtype="float32",
			callback=_callback,
		):
			start = time.time()
			frames: list[np.ndarray] = []
			while time.time() - start < seconds:
				try:
					chunk = q.get(timeout=0.1)
					frames.append(chunk)
				except queue.Empty:
					pass

		if not frames:
			return np.zeros((0, self.channels), dtype=np.float32)
		return np.concatenate(frames, axis=0)

	def save_wav(self, path: str, audio: np.ndarray) -> None:
		if audio.dtype != np.float32:
			audio = audio.astype(np.float32)
		sf.write(path, audio, self.sample_rate, subtype="PCM_16")

	def play_wav(self, path: str) -> None:
		data, sr = sf.read(path, dtype="int16")
		if sr != self.sample_rate:
			print(f"Warning: sample rate mismatch ({sr} != {self.sample_rate})")
		play_obj = sa.play_buffer(data, num_channels=data.shape[1] if data.ndim > 1 else 1, bytes_per_sample=2, sample_rate=sr)
		play_obj.wait_done()