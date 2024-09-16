import asyncio
from telegram.ext import ApplicationBuilder
import logging
from config import BOT_TOKEN, CHAT_ID

logger = logging.getLogger(__name__)


async def send_message(bot, chat_id: str, message: str):
    """
    Sends a message to the specified Telegram chat.

    Args:
        bot: The Telegram bot instance.
        chat_id (str): The chat ID where the message will be sent.
        message (str): The message content.
    """
    await bot.send_message(chat_id=chat_id, text=message)


def format_ad_message(ad: dict) -> str:
    """
    Formats the ad information into a message string.

    Args:
        ad (dict): The ad information.

    Returns:
        str: Formatted message string.
    """
    return (
        f"Title: {ad['title']}\n\n"
        f"Main Info: {ad['main_info']}\n\n"
        f"Price: {ad['price']}\n\n"
        f"Car Body Type: {ad['car_body_type']}\n\n"
        f"Description: {ad['description']}\n\n"
        f"Ad Post Date: {ad['display_date']}\n\n"
        f"Ad URL: {ad['ad_url']}\n\n"
    )


async def send_notification(bot, ad: dict) -> int:
    """
    Sends a notification for a specific ad.

    Args:
        bot: The Telegram bot instance.
        ad (dict): The ad information.

    Returns:
        int: 1 indicating a notification was sent successfully.
    """
    message = format_ad_message(ad)
    logger.info(f"Sending notification for AD ID: {ad['ad_id']} ({ad['ad_url']})...")
    await send_message(bot, CHAT_ID, message)
    return 1


async def notify_ads(ads: list):
    """
    Sends notifications for a list of ads to a specified Telegram chat.

    Args:
        ads (list): A list of dictionaries, each representing an ad.
    """
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    bot = application.bot

    notified_ads_count = sum(
        await asyncio.gather(*(send_notification(bot, ad) for ad in ads))
    )

    if notified_ads_count > 0:
        await send_message(bot, CHAT_ID, f"Total new ads sent: {notified_ads_count}")
    else:
        await send_message(bot, CHAT_ID, "No new ads found!")


def run_notify_ads(ads: list):
    """
    Run the notify_ads function in an event loop.

    Args:
        ads (list): A list of dictionaries, each representing an ad.
    """
    asyncio.run(notify_ads(ads))
