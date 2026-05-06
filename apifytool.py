import json
import logging
from datetime import datetime, timedelta
from apify_client import ApifyClient
from crewai.tools import BaseTool
from pydantic import Field
from config import APIFY_API_TOKEN

logger = logging.getLogger(__name__)


class MetaAdScraperTool(BaseTool):
    name: str = "meta_ads_scraper"
    description: str = (
        "Scrapes Meta Ad Library for active ads related to a given niche/keyword. "
        "Returns a list of ads with their text, engagement, and metadata."
    )
    api_token: str = Field(default=APIFY_API_TOKEN)

    def _run(self, query: str) -> str:
        client = ApifyClient(self.api_token)
        cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        logger.info(f"Scraping Meta Ads for query: '{query}' since {cutoff}")
        try:
            run = client.actor("apify/facebook-ads-scraper").call(
                run_input={
                    "searchTerms": [query],
                    "adType": "ALL",
                    "country": "US",
                    "startDate": cutoff,
                    "maxResults": 50,
                }
            )
            ads = []
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                ads.append({
                    "id": item.get("id"),
                    "page_name": item.get("pageName"),
                    "ad_text": item.get("adText") or item.get("body"),
                    "start_date": item.get("startDate"),
                    "impressions": item.get("impressions", {}).get("lowerBound", 0),
                    "url": item.get("url"),
                    "media_type": item.get("mediaType"),
                })
            logger.info(f"Scraped {len(ads)} ads")
            return json.dumps(ads)
        except Exception as e:
            logger.error(f"Apify scrape failed: {e}")
            return json.dumps({"error": str(e)})
