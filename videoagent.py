import json
import logging
import os
from crewai import Agent
from config import get_llm, OUTPUT_DIR
from elevenlabstool import ElevenLabsTTSTool

logger = logging.getLogger(__name__)


def create_video_agent() -> Agent:
    return Agent(
        role="Video Producer",
        goal=(
            "Generate the voiceover audio from the ad script using ElevenLabs, "
            "then produce a complete Remotion video project config with scene breakdown, "
            "subtitles, and image prompts for each scene."
        ),
        backstory=(
            "You are a video production specialist who bridges AI tools and Remotion. "
            "You generate voiceovers, write subtitle tracks, and produce detailed "
            "Remotion composition configs that a developer can run immediately."
        ),
        tools=[ElevenLabsTTSTool()],
        llm=get_llm(),
        verbose=True,
        max_iter=3,
    )
