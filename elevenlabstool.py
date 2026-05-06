import logging
import os
import requests
from crewai.tools import BaseTool
from pydantic import Field
from config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, OUTPUT_DIR

logger = logging.getLogger(__name__)


class ElevenLabsTTSTool(BaseTool):
    name: str = "elevenlabs_tts"
    description: str = (
        "Converts a script text to speech using ElevenLabs API. "
        "Saves the audio file and returns the file path."
    )
    api_key: str = Field(default=ELEVENLABS_API_KEY)
    voice_id: str = Field(default=ELEVENLABS_VOICE_ID)

    def _run(self, script: str) -> str:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {"xi-api-key": self.api_key, "Content-Type": "application/json"}
        payload = {
            "text": script[:2500],
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        }
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            out_path = os.path.join(OUTPUT_DIR, "voiceover.mp3")
            with open(out_path, "wb") as f:
                f.write(resp.content)
            logger.info(f"Voiceover saved to {out_path}")
            return out_path
        except Exception as e:
            logger.error(f"ElevenLabs TTS failed: {e}")
            return f"ERROR: {e}"
