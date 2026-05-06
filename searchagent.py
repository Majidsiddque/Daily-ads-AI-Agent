from crewai import Agent
from config import get_llm, TARGET_NICHE, TARGET_PRODUCT
from apifytool import MetaAdScraperTool


def create_search_agent() -> Agent:
    return Agent(
        role="Meta Ads Researcher",
        goal=(
            f"Find the top 10 best-performing Meta ads in the last 30 days "
            f"related to '{TARGET_PRODUCT}' in the '{TARGET_NICHE}' niche."
        ),
        backstory=(
            "You are an expert digital marketer who specializes in competitive ad research. "
            "You identify high-performing ads by analyzing engagement signals, "
            "copy patterns, and creative formats in the Meta Ad Library."
        ),
        tools=[MetaAdScraperTool()],
        llm=get_llm(),
        verbose=True,
        max_iter=3,
    )
