from crewai import Agent
from config import get_llm


def create_analysis_agent() -> Agent:
    return Agent(
        role="Marketing Analyst",
        goal=(
            "Extract the core marketing angles, pain points, emotional triggers, "
            "and persuasion concepts from the top-performing ads."
        ),
        backstory=(
            "You are a direct-response copywriter and consumer psychology expert. "
            "You dissect ads to uncover the exact pain points, desires, and hooks "
            "that make them convert. You produce structured, actionable insights."
        ),
        tools=[],
        llm=get_llm(),
        verbose=True,
        max_iter=3,
    )
