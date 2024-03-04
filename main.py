import logging
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = 'Where token?????? :) (token -> in my tg saves)'

def start(update, context):
    update.message.reply_text('Send me an artist name to get recommendations.')

def handle_message(update, context):
    artist_name = update.message.text
    try:
        response = requests.post('http://127.0.0.1:5000/recommend', json={'artist_name': artist_name})
        if response.status_code == 200:
            update.message.reply_text(response.json().get('results', 'No recommendations found.'))
        else:
            update.message.reply_text(f"Error getting recommendations. Status code: {response.status_code}")
            logging.error(f"Error response: {response.text}")
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        update.message.reply_text("Failed to get recommendations.")
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
