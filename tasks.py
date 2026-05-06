from crewai import Task
from config import TARGET_NICHE, TARGET_PRODUCT, TARGET_URL, OUTPUT_DIR
import os


def create_tasks(search_agent, analysis_agent, script_agent, video_agent):

    search_task = Task(
        description=(
            f"Search the Meta Ad Library for ads related to '{TARGET_PRODUCT}' "
            f"and the '{TARGET_NICHE}' niche (site: {TARGET_URL}). "
            "Use the meta_ads_scraper tool with the query 'trading education profit signals'. "
            "From the results, select the top 10 ads with the highest impressions or engagement "
            "from the last 30 days. Return a JSON array of the selected ads."
        ),
        expected_output=(
            "A JSON array of the 10 best-performing ads, each containing: "
            "id, page_name, ad_text, start_date, impressions, url, media_type."
        ),
        agent=search_agent,
        output_file=os.path.join(OUTPUT_DIR, "top_ads.json"),
    )

    analysis_task = Task(
        description=(
            "Analyze the top ads JSON provided by the previous task. "
            "For each ad, identify: (1) the primary pain point addressed, "
            "(2) the emotional trigger used, (3) the core marketing angle/hook, "
            "(4) the persuasion technique (scarcity, social proof, authority, etc.). "
            "Then summarize the top 3 recurring pain points and the single strongest hook concept."
        ),
        expected_output=(
            "A structured markdown report with: "
            "per-ad breakdown, top 3 pain points, strongest hook, and recommended marketing angle."
        ),
        agent=analysis_agent,
        context=[search_task],
        output_file=os.path.join(OUTPUT_DIR, "marketing_analysis.md"),
    )

    script_task = Task(
        description=(
            "Use the gdrive_fetcher tool to retrieve the reference ad examples. "
            "Then, using the marketing analysis (pain points + hook) from the previous task, "
            f"write a 60-second video ad script for '{TARGET_PRODUCT}'. "
            "Structure: Hook (0-5s) | Problem Agitation (5-20s) | Solution (20-45s) | CTA (45-60s). "
            "The script must feel authentic, urgent, and speak directly to the target audience's pain."
        ),
        expected_output=(
            "A complete 60-second ad script with timestamps, spoken lines, "
            "and brief visual direction notes for each segment."
        ),
        agent=script_agent,
        context=[analysis_task],
        output_file=os.path.join(OUTPUT_DIR, "ad_script.md"),
    )

    video_task = Task(
        description=(
            "Take the 60-second ad script from the previous task. "
            "1. Use the elevenlabs_tts tool to generate the voiceover audio from the script text. "
            "2. Produce a Remotion video composition config as a JSON object with: "
            "   - scenes array (each with: start_ms, end_ms, visual_prompt, subtitle_text) "
            "   - voiceover_path (from TTS tool output) "
            "   - fps: 30, durationInFrames: 1800 (60s * 30fps) "
            "3. Write image generation prompts (for a free tool like Lexica or Pollinations) "
            "   for each scene's background visual."
        ),
        expected_output=(
            "A JSON Remotion composition config saved to output/remotion_config.json, "
            "plus a list of image prompts per scene, and the voiceover file path."
        ),
        agent=video_agent,
        context=[script_task],
        output_file=os.path.join(OUTPUT_DIR, "remotion_config.json"),
    )

    return [search_task, analysis_task, script_task, video_task]
