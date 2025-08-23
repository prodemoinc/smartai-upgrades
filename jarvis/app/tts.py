from __future__ import annotations

import subprocess
from pathlib import Path


class PiperTTS:
	def __init__(self, piper_exe: str, voice_path: str, sample_rate: int = 16000):
		self.piper_exe = piper_exe
		self.voice_path = voice_path
		self.sample_rate = sample_rate

	def synthesize_to_wav(self, text: str, output_wav: str) -> None:
		cmd = [
			self.piper_exe,
			"--model",
			self.voice_path,
			"--output_file",
			output_wav,
			"--sentence_silence",
			"0.3",
		]
		proc = subprocess.run(cmd, input=text.encode("utf-8"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		if proc.returncode != 0:
			raise RuntimeError(f"Piper failed: {proc.stderr.decode(errors='ignore')}")