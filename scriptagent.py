from crewai import Agent
from config import get_llm, TARGET_PRODUCT
from gdrivetool import GDriveFetcherTool


def create_script_agent() -> Agent:
    return Agent(
        role="Ad Scriptwriter",
        goal=(
            f"Write a compelling 60-second video ad script for '{TARGET_PRODUCT}' "
            "based on identified pain points and the reference ad examples from Google Drive."
        ),
        backstory=(
            "You are a world-class direct-response video scriptwriter. "
            "You craft 60-second scripts with a strong hook (0-5s), problem agitation (5-20s), "
            "solution reveal (20-45s), and a clear CTA (45-60s). "
            "You always ground scripts in real audience pain points."
        ),
        tools=[GDriveFetcherTool()],
        llm=get_llm(),
        verbose=True,
        max_iter=3,
    )
