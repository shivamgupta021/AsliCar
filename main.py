import os
import pickle
import logging
from api_client import fetch_ads
from data_processor import process_ads
from notification_sender import notify_ads
from config import notified_ads_file
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

if os.path.exists(notified_ads_file):
    with open(notified_ads_file, "rb") as f:
        notified_ads = pickle.load(f)
else:
    notified_ads = set()


def run_job():
    ads_data = fetch_ads()
    processed_ads = process_ads(ads_data)

    new_ads = [ad for ad in processed_ads if ad["ad_id"] not in notified_ads]
    notify_ads(new_ads)

    with open(notified_ads_file, "wb") as f:
        pickle.dump(notified_ads | {ad["ad_id"] for ad in new_ads}, f)

    logger.info(f"Job executed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    run_job()
