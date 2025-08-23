from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

from app.config import load_settings
from app.audio import AudioIO
from app.stt import SpeechToText
from app.llm import OllamaClient
from app.tts import PiperTTS
from app.tools import route_intent


def main() -> None:
	load_dotenv()
	settings = load_settings()

	print("Starting local assistant (Windows)")
	print(f"LLM: {settings.ollama_model} @ {settings.ollama_host}")

	audio = AudioIO(sample_rate=settings.sample_rate, channels=settings.channels)
	stt = SpeechToText(model_size=settings.stt_model)
	llm = OllamaClient(base_url=settings.ollama_host, model=settings.ollama_model)
	tps = PiperTTS(piper_exe=settings.piper_exe, voice_path=settings.voice_path, sample_rate=settings.sample_rate)

	messages: list[dict[str, str]] = [
		{"role": "system", "content": "You are a helpful Persian/English assistant on a local PC. Be concise."},
	]

	while True:
		print("\n[Enter to speak 5s, or type a message. Type /quit to exit]")
		user_text = input(">").strip()
		if user_text == "":
			print("Recording 5s... speak now")
			audio_np = audio.record_seconds(5.0)
			user_text = stt.transcribe(audio_np, settings.sample_rate)
			print(f"You said: {user_text}")
		elif user_text.lower() == "/quit":
			break

		if not user_text:
			continue

		tool_res = route_intent(user_text)
		tool_note = ""
		if tool_res is not None:
			tool_note = f"\nTool: {tool_res.message}"

		messages.append({"role": "user", "content": user_text})
		assistant_text = llm.chat(messages)
		assistant_text = assistant_text.strip()
		if tool_note:
			assistant_text += tool_note
		print(f"Assistant: {assistant_text}")
		messages.append({"role": "assistant", "content": assistant_text})

		# Speak the response
		out_wav = str((settings.data_dir / "reply.wav").resolve())
		try:
			tps.synthesize_to_wav(assistant_text, out_wav)
			from app.audio import AudioIO as _A
			_A(settings.sample_rate, settings.channels).play_wav(out_wav)
		except Exception as exc:
			print(f"[TTS error] {exc}")


if __name__ == "__main__":
	main()