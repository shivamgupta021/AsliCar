import asyncio
from telegram.ext import ApplicationBuilder
import logging
from config import BOT_TOKEN, CHAT_ID

logger = logging.getLogger(__name__)


async def send(bot, chat, msg):
    """
    Sends a message to the specified Telegram chat.

    Args:
        bot: The Telegram bot instance.
        chat (str): The chat ID where the message will be sent.
        msg (str): The message content.
    """
    await bot.send_message(chat_id=chat, text=msg)


async def send_notification(bot, ad):
    """
    Sends a notification for a specific ad.

    Args:
        bot: The Telegram bot instance.
        ad (dict): The ad information in the form of a dictionary.
            Expected keys: 'title', 'main_info', 'price', 'car_body_type',
            'description', 'display_date', 'ad_url', 'ad_id'.

    Returns:
        int: 1 indicating a notification was sent successfully.
    """
    message = (
        f"Title: {ad['title']}\n\n"
        f"Main Info: {ad['main_info']}\n\n"
        f"Price: {ad['price']}\n\n"
        f"Car Body Type: {ad['car_body_type']}\n\n"
        f"Description: {ad['description']}\n\n"
        f"Ad Post Date: {ad['display_date']}\n\n"
        f"Ad URL: {ad['ad_url']}\n\n"
    )

    logger.info(f"Sending notification for AD ID: {ad['ad_id']} ({ad['ad_url']})...")
    await send(bot, CHAT_ID, message)
    return 1


async def notify_ads(ads):
    """
    Sends notifications for a list of ads to a specified Telegram chat.

    Args:
        ads (list): A list of dictionaries, each representing an ad.
            Each dictionary should include the keys: 'title', 'main_info',
            'price', 'car_body_type', 'description', 'display_date',
            'ad_url', 'ad_id'.

    Returns:
        None
    """
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    async with application:
        bot = application.bot
        notified_ads_count = 0

        # Send notifications for each ad
        for ad in ads:
            notified_ads_count += await send_notification(bot, ad)

        # Send a summary message
        if notified_ads_count > 0:
            await send(bot, CHAT_ID, f"Total new ads sent: {notified_ads_count}")
        else:
            await send(bot, CHAT_ID, "No new ads found!")


def start_notifying(ads):
    """
    Entry point to trigger ad notifications.

    Args:
        ads (list): A list of ads to notify about.

    Returns:
        None
    """
    asyncio.run(notify_ads(ads))
