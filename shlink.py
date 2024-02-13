from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests
import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
SHLINK_API_TOKEN = os.getenv('SHLINK_API_TOKEN')
SHLINK_SERVER_URL = os.getenv('SHLINK_SERVER_URL')
ALLOWED_TELEGRAM_IDS = set(int(x) for x in os.getenv('ALLOWED_TELEGRAM_IDS', '').split(','))

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_TELEGRAM_IDS:
        await update.message.reply_text('You do not have access to this bot.')
        return
    await update.message.reply_text('Hi. Send me the link and I\'ll shorten it for you.')

def shorten_url(url: str) -> str:
    headers = {'X-Api-Key': f'{SHLINK_API_TOKEN}'}
    data = {'longUrl': url}
    response = requests.post(f'{SHLINK_SERVER_URL}/rest/v2/short-urls', headers=headers, json=data)
    if response.status_code == 200:
        short_url = response.json().get('shortUrl', '')
        return short_url
    else:
        return 'Error when shortening a link.'

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_TELEGRAM_IDS:
        await update.message.reply_text('You do not have access to this bot.')
        return
    url = update.message.text
    short_url = shorten_url(url)
    await update.message.reply_text(short_url)

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == '__main__':
    main()
