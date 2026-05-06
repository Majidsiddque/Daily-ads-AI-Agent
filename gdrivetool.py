import logging
import requests
from crewai.tools import BaseTool
from pydantic import Field
from config import GDRIVE_FILE_ID_1, GDRIVE_FILE_ID_2

logger = logging.getLogger(__name__)

GDRIVE_EXPORT_URL = "https://drive.google.com/uc?export=download&id={file_id}"


class GDriveFetcherTool(BaseTool):
    name: str = "gdrive_fetcher"
    description: str = (
        "Fetches marketing reference documents from Google Drive. "
        "Returns the text content of the ad example files."
    )
    file_ids: list = Field(default_factory=lambda: [GDRIVE_FILE_ID_1, GDRIVE_FILE_ID_2])

    def _run(self, _: str = "") -> str:
        contents = []
        for fid in self.file_ids:
            url = GDRIVE_EXPORT_URL.format(file_id=fid)
            try:
                resp = requests.get(url, timeout=15)
                resp.raise_for_status()
                text = resp.text[:4000]
                contents.append(f"--- File {fid} ---\n{text}")
                logger.info(f"Fetched GDrive file {fid} ({len(text)} chars)")
            except Exception as e:
                logger.warning(f"Could not fetch GDrive file {fid}: {e}")
                contents.append(f"--- File {fid} --- ERROR: {e}")
        return "\n\n".join(contents)
