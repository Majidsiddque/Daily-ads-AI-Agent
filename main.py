import logging
import os
import sys
from crewai import Crew, Process
from config import OUTPUT_DIR
from searchagent import create_search_agent
from analysisagent import create_analysis_agent
from scriptagent import create_script_agent
from videoagent import create_video_agent
from tasks import create_tasks

os.makedirs(OUTPUT_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(OUTPUT_DIR, "run.log")),
    ],
)
logger = logging.getLogger(__name__)


def main():
    logger.info("=== CrowdWisdomTrading Ad Generation Pipeline START ===")

    search_agent = create_search_agent()
    analysis_agent = create_analysis_agent()
    script_agent = create_script_agent()
    video_agent = create_video_agent()

    tasks = create_tasks(search_agent, analysis_agent, script_agent, video_agent)

    crew = Crew(
        agents=[search_agent, analysis_agent, script_agent, video_agent],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    logger.info("=== Pipeline COMPLETE ===")
    logger.info(f"Outputs saved to: {OUTPUT_DIR}")
    logger.info(f"Final result summary:\n{result}")

    print("\n✅ Done! Check the output/ folder for:")
    print("  - top_ads.json          (Agent 1: best performing ads)")
    print("  - marketing_analysis.md (Agent 2: pain points & hooks)")
    print("  - ad_script.md          (Agent 3: 60s video script)")
    print("  - remotion_config.json  (Agent 4: Remotion composition config)")
    print("  - voiceover.mp3         (Agent 4: ElevenLabs voiceover)")
    print("  - run.log               (full execution log)")


if __name__ == "__main__":
    main()
