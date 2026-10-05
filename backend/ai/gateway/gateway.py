import os
import requests

COSMIC_SYSTEM = """You are COSMIC, the user's personal AI system.

Your name is COSMIC.
Do not introduce yourself as Gemini unless the user specifically asks which underlying model is being used.
Gemini is the underlying AI engine; COSMIC is the assistant/interface.

Be practical, technically capable, concise, and honest.
Never claim to control the user's phone, files, apps, microphone, camera, or other devices unless an actual connected tool provides that capability.
Preserve the user's conversation context when supplied.
"""

class AIGateway:
    def __init__(self):
        self.key = os.getenv("GEMINI_API_KEY", "")
        self.url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent"
        self.model = "gemini-3.6-flash"

    def chat(self, message, history=None):
        if not self.key:
            return {
                "success": False,
                "provider": "gemini",
                "error": "GEMINI_API_KEY not configured"
            }

        contents = []

        if history:
            for item in history:
                role = "user" if item.get("role") == "user" else "model"
                text = item.get("content", "")
                if text:
                    contents.append({
                        "role": role,
                        "parts": [{"text": text}]
                    })

        contents.append({
            "role": "user",
            "parts": [{"text": message}]
        })

        try:
            r = requests.post(
                self.url,
                params={"key": self.key},
                headers={"Content-Type": "application/json"},
                json={
                    "systemInstruction": {
                        "parts": [{"text": COSMIC_SYSTEM}]
                    },
                    "contents": contents
                },
                timeout=60
            )

            if not r.ok:
                return {
                    "success": False,
                    "provider": "gemini",
                    "error": f"Gemini HTTP {r.status_code}: {r.text}"
                }

            data = r.json()

            candidates = data.get("candidates", [])
            if not candidates:
                return {
                    "success": False,
                    "provider": "gemini",
                    "error": "Gemini returned no candidates"
                }

            parts = candidates[0].get("content", {}).get("parts", [])
            text = "".join(
                p.get("text", "")
                for p in parts
                if p.get("text")
            ).strip()

            if not text:
                return {
                    "success": False,
                    "provider": "gemini",
                    "error": "Gemini returned an empty response"
                }

            return {
                "success": True,
                "provider": "gemini",
                "model": self.model,
                "message": text,
                "type": "response",
                "verified": True
            }

        except requests.RequestException as e:
            return {
                "success": False,
                "provider": "gemini",
                "error": f"Network error: {e}"
            }

        except Exception as e:
            return {
                "success": False,
                "provider": "gemini",
                "error": f"Gateway error: {e}"
            }
