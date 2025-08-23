from __future__ import annotations

from typing import Iterable, Optional
import requests


class OllamaClient:
	def __init__(self, base_url: str, model: str):
		self.base_url = base_url.rstrip("/")
		self.model = model

	def chat(self, messages: list[dict[str, str]], stream: bool = False) -> str:
		url = f"{self.base_url}/api/chat"
		payload = {"model": self.model, "messages": messages, "stream": False}
		resp = requests.post(url, json=payload, timeout=600)
		resp.raise_for_status()
		data = resp.json()
		return data.get("message", {}).get("content", "")