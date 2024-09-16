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


def send_notification(loop, bot, ad):
    """
    Sends a notification for a specific ad.

    Args:
        loop: The asyncio event loop.
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

    loop.run_until_complete(send(bot, CHAT_ID, message))

    return 1


def notify_ads(ads):
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
    bot = application.bot
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    notified_ads_count = 0
    for ad in ads:
        notified_ads_count += send_notification(loop, bot, ad)

    if notified_ads_count > 0:
        loop.run_until_complete(
            send(bot, CHAT_ID, f"Total new ads sent: {notified_ads_count}")
        )
    else:
        loop.run_until_complete(send(bot, CHAT_ID, "No new ads found!"))

    loop.close()
