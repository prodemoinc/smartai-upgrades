from __future__ import annotations

import os
import subprocess
import webbrowser
from dataclasses import dataclass
from typing import Optional


ALLOWED_APPS = {
	"notepad": r"C:\\Windows\\system32\\notepad.exe",
	"calc": r"C:\\Windows\\system32\\calc.exe",
}


@dataclass
class ToolResult:
	success: bool
	message: str


def open_application(app_key: str) -> ToolResult:
	path = ALLOWED_APPS.get(app_key.lower())
	if not path:
		return ToolResult(False, f"App not allowed: {app_key}")
	try:
		subprocess.Popen([path])
		return ToolResult(True, f"Opened {app_key}")
	except Exception as exc:
		return ToolResult(False, f"Failed to open {app_key}: {exc}")


def open_url(url: str) -> ToolResult:
	try:
		webbrowser.open(url)
		return ToolResult(True, f"Opened URL: {url}")
	except Exception as exc:
		return ToolResult(False, f"Failed to open URL: {exc}")


def route_intent(user_text: str) -> Optional[ToolResult]:
	text = user_text.strip().lower()
	if not text:
		return None
	if "باز کن" in text and "نوت پد" in text or "notepad" in text:
		return open_application("notepad")
	if text.startswith("open ") and "." in text:
		url = text.split("open ", 1)[1].strip()
		if not url.startswith("http"):
			url = "http://" + url
		return open_url(url)
	return None