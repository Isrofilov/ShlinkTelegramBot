from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests
import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
SHLINK_API_TOKEN = os.getenv('SHLINK_API_TOKEN')
SHLINK_SERVER_URL = os.getenv('SHLINK_SERVER_URL')
ALLOWED_TELEGRAM_IDS = os.getenv('ALLOWED_TELEGRAM_IDS')
SEND_QR_CODE = os.getenv('SEND_QR_CODE', 'false').lower() == 'true'

if not TELEGRAM_BOT_TOKEN or not SHLINK_API_TOKEN or not SHLINK_SERVER_URL:
    raise EnvironmentError('Missing one or more required environment variables.')

if ALLOWED_TELEGRAM_IDS:
    ALLOWED_TELEGRAM_IDS = set(int(x) for x in ALLOWED_TELEGRAM_IDS.split(','))
else:
    ALLOWED_TELEGRAM_IDS = None

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_TELEGRAM_IDS:
        await update.message.reply_text('You do not have access to this bot.')
        return
    await update.message.reply_text('Hi. Send me the link and I\'ll shorten it for you.')

def shorten_url(url: str) -> str:
    headers = {'X-Api-Key': f'{SHLINK_API_TOKEN}'}
    data = {'longUrl': url}
    response = requests.post(f'{SHLINK_SERVER_URL}/rest/v3/short-urls', headers=headers, json=data)
    if response.status_code == 200:
        short_url_data = response.json()
        short_url = short_url_data.get('shortUrl', '')
        short_code = short_url_data.get('shortCode', '')
        return short_url, short_code
    else:
        return 'Error when shortening a link.', None

def generate_qr_code(short_code: str) -> (bytes, str):
    if short_code is None:
        return None, 'Error when generating QR code because short link was not created.'
    response = requests.get(f'{SHLINK_SERVER_URL}/{short_code}/qr-code')
    if response.status_code == 200:
        return response.content, None
    else:
        return None, 'Error when generating QR code.'

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if ALLOWED_TELEGRAM_IDS is not None and user_id not in ALLOWED_TELEGRAM_IDS:
        await update.message.reply_text('You do not have access to this bot.')
        return
    url = update.message.text
    short_url, short_code = shorten_url(url)
    if short_url.startswith('Error'):
        await update.message.reply_text(short_url)
        return
    if SEND_QR_CODE:
        qr_code_bytes, error_message = generate_qr_code(short_code)
        if error_message:
            await update.message.reply_text(short_url)
            await update.message.reply_text(error_message)
        else:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=qr_code_bytes, caption=short_url)
    else:
        await update.message.reply_text(short_url)

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == '__main__':
    main()