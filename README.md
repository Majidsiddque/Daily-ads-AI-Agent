# CrowdWisdomTrading Daily Ads AI Agent

A CrewAI-powered pipeline that researches top-performing Meta ads, extracts marketing insights, writes a 60-second ad script, generates a voiceover, and produces a Remotion video composition config.

---

## Architecture

```
main.py
  │
  ├── Agent 1: Meta Ads Researcher      → output/top_ads.json
  │     tool: MetaAdScraperTool (Apify)
  │
  ├── Agent 2: Marketing Analyst        → output/marketing_analysis.md
  │     (no external tool, uses LLM on Agent 1 output)
  │
  ├── Agent 3: Ad Scriptwriter          → output/ad_script.md
  │     tool: GDriveFetcherTool
  │
  └── Agent 4: Video Producer           → output/remotion_config.json
        tool: ElevenLabsTTSTool              output/voiceover.mp3
```

**LLM:** OpenRouter (free model: `mistralai/mistral-7b-instruct:free`)  
**Scraping:** Apify — Meta Ad Library  
**Voice:** ElevenLabs free tier  
**Video:** Remotion (React-based video framework)  
**Images:** Pollinations.ai (free, no API key needed)

---

## Setup

### 1. Clone & install Python deps
```bash
cd TZURONI
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Fill in your keys in .env
```

Required keys:
| Key | Where to get |
|-----|-------------|
| `OPENROUTER_API_KEY` | https://openrouter.ai/keys |
| `APIFY_API_TOKEN` | https://console.apify.com/account/integrations |
| `ELEVENLABS_API_KEY` | https://elevenlabs.io/app/settings/api-keys |

### 3. Run the pipeline
```bash
python main.py
```

### 4. Render the video (after pipeline completes)
```bash
cd remotion
npm install
npm run start        # opens Remotion Studio (preview)
npm run build        # renders out/ad.mp4
```

---

## Output Files

| File | Description |
|------|-------------|
| `output/top_ads.json` | Top 10 Meta ads from last 30 days |
| `output/marketing_analysis.md` | Pain points, hooks, marketing angles |
| `output/ad_script.md` | 60-second video ad script with timestamps |
| `output/remotion_config.json` | Remotion composition config (scenes + subtitles) |
| `output/voiceover.mp3` | ElevenLabs generated voiceover |
| `output/run.log` | Full execution log |

---

## Project Structure

```
TZURONI/
├── agents/
│   ├── search_agent.py      # Agent 1 — Meta ad research
│   ├── analysis_agent.py    # Agent 2 — Marketing analysis
│   ├── script_agent.py      # Agent 3 — Script writing
│   └── video_agent.py       # Agent 4 — Video production
├── tools/
│   ├── apify_tool.py        # Apify Meta Ads scraper
│   ├── gdrive_tool.py       # Google Drive reference fetcher
│   └── elevenlabs_tool.py   # ElevenLabs TTS
├── remotion/
│   ├── src/
│   │   ├── index.tsx        # Remotion root
│   │   └── AdComposition.tsx
│   ├── package.json
│   └── tsconfig.json
├── output/                  # All generated artifacts
├── config.py                # Centralized config + LLM factory
├── tasks.py                 # CrewAI task definitions
├── main.py                  # Entry point
├── requirements.txt
└── .env.example
```

---

## Notes

- The Apify actor used is `apify/facebook-ads-scraper`. Make sure your Apify account has free credits.
- ElevenLabs free tier allows ~10k characters/month. The script is capped at 2500 chars.
- Pollinations.ai (`https://pollinations.ai/p/<prompt>`) is used for scene images — completely free, no key needed.
- To swap the LLM, change `OPENROUTER_MODEL` in `.env` to any free model on OpenRouter.
