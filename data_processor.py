from api_client import fetch_user_data
import logging
from config import AD_URL
from typing import List, Dict

logger = logging.getLogger(__name__)


def filter_user_data(user_data: Dict[str, any]) -> bool:
    """
    Filter user data based on certain criteria.

    Args:
        user_data (Dict[str, any]): The user data to be filtered.

    Returns:
        bool: True if the user data should be filtered out, False otherwise.
    """
    if not bool(user_data):
        return True
    user_name = user_data.get("name", "")
    motor_keywords = ["motors", "automobile", "cars", "vehicles", "motor", "enterprise"]
    if (
            user_data.get("is_business")
            or user_data.get("kyc", {}).get("status") == "verified"
            or any(keyword in user_name.lower() for keyword in motor_keywords)
    ):
        return True
    return False


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
        except Exception as e:
            logger.error(
                f"Error fetching user data for ad ID {item.get('ad_id', '')}: {str(e)}"
            )
            continue

        if filter_user_data(user_data):
            continue

        ad_id = item.get("ad_id", "")
        ad_url = AD_URL.format(ad_id=ad_id)
        description = item.get("description", "N/A")
        created_at = item.get("created_at", "N/A")
        title = item.get("title", "N/A")
        car_body_type = item.get("car_body_type", "N/A")
        user_type = item.get("user_type", "N/A")
        user_name = user_data.get("name", "N/A")
        price = item.get("price", {}).get("value", {}).get("display", "N/A")
        partner_code = item.get("partner_code", "N/A")
        certified_car = item.get("certified_car", False)
        main_info = item.get("main_info", "N/A")
        display_date = item.get("display_date", "N/A")
        display_date = display_date.split("T")[0]

        processed_ads.append(
            {
                "ad_id": ad_id,
                "description": description,
                "created_at": created_at,
                "title": title,
                "car_body_type": car_body_type,
                "user_type": user_type,
                "user_name": user_name,
                "price": price,
                "partner_code": partner_code,
                "certified_car": certified_car,
                "main_info": main_info,
                "user_id": user_id,
                "display_date": display_date,
                "ad_url": ad_url,
            }
        )

    return processed_ads
