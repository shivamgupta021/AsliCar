import requests
from config import HEADERS, USER_API_URL, API_URL
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def fetch_user_data(user_id: str) -> Dict[str, any]:
    """
    Fetch user data from the API using the provided user ID.

    Args:
        user_id (str): The ID of the user.

    Returns:
        Dict[str, any]: The user data, or an empty dictionary if the request fails.
    """
    user_url = USER_API_URL.format(user_id=user_id)
    try:
        response = requests.get(user_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json().get("data", {})
    except requests.exceptions.RequestException as e:
        logger.error(
            f"Error fetching user data for user_id: {user_id}. Exception: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error occurred while fetching user data: {str(e)}")
    return {}


def fetch_ads(pages: int = 10) -> List[Dict[str, any]]:
    """
    Fetch ads data from the API for the specified number of pages.

    Args:
        pages (int): The number of pages to fetch (default is 10).

    Returns:
        List[Dict[str, any]]: The list of ads data.
    """
    all_ads = []
    for page in range(1, pages + 1):
        page_url = API_URL.replace("?page=1", f"?page={page}")
        try:
            response = requests.get(page_url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            ads_data = response.json()
            all_ads.extend(ads_data.get("data", []))
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request on page {page}: {str(e)}")
            break
        except Exception as e:
            logger.error(
                f"Unexpected error occurred while fetching ads on page {page}: {str(e)}"
            )
            break
    return all_ads
