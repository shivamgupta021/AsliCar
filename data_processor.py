from api_client import fetch_user_data
import logging
from config import AD_URL
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


def filter_user_data(user_data: Optional[Dict[str, any]]) -> bool:
    """
    Filter user data based on certain criteria.

    Args:
        user_data (Optional[Dict[str, any]]): The user data to be filtered.

    Returns:
        bool: True if the user data should be filtered out, False otherwise.
    """
    if not user_data:
        return True
    user_name = user_data.get("name", "").lower()
    motor_keywords = {"motors", "automobile", "cars", "vehicles", "motor", "enterprise"}
    return (
            user_data.get("is_business")
            or user_data.get("kyc", {}).get("status") == "verified"
            or any(keyword in user_name for keyword in motor_keywords)
    )


def process_ads(ads_data: List[Dict[str, any]]) -> List[Dict[str, any]]:
    """
    Process the ads data by fetching user data and filtering ads.

    Args:
        ads_data (List[Dict[str, any]]): The raw ads data.

    Returns:
        List[Dict[str, any]]: The processed ads data.
    """
    processed_ads = []
    for item in ads_data:
        user_id = item.get("user_id", "")
        try:
            user_data = fetch_user_data(user_id)
            if filter_user_data(user_data):
                continue

            processed_ad = {
                "ad_id": item.get("ad_id", ""),
                "description": item.get("description", "N/A"),
                "created_at": item.get("created_at", "N/A"),
                "title": item.get("title", "N/A"),
                "car_body_type": item.get("car_body_type", "N/A"),
                "user_type": item.get("user_type", "N/A"),
                "user_name": user_data.get("name", "N/A"),
                "price": item.get("price", {}).get("value", {}).get("display", "N/A"),
                "partner_code": item.get("partner_code", "N/A"),
                "certified_car": item.get("certified_car", False),
                "main_info": item.get("main_info", "N/A"),
                "user_id": user_id,
                "display_date": item.get("display_date", "N/A").split("T")[0],
                "ad_url": AD_URL.format(ad_id=item.get("ad_id", "")),
            }
            processed_ads.append(processed_ad)
        except Exception as e:
            logger.error(f"Error processing ad ID {item.get('ad_id', '')}: {e}")

    return processed_ads
