import csv
import math
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from tensorflow.keras.models import load_model
import joblib

model = load_model('music_recommendation_model.h5')
userRates = joblib.load('userRates.pkl')

TOKEN = ''
BOT_USERNAME: Final = '@MusicRecommendationAituBot'
def ReadFile(filename="music.csv"):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        mentions = dict()

        for line in reader:
            user = line[6]
            product = line[23] 
            user_terms_index = 24 

            try:
                rate = float(line[0])  # 'artist.familiarity' as rating
                user_terms = line[user_terms_index]
            except ValueError:
                continue 

            if user not in mentions:
                mentions[user] = {"ratings": dict(), "terms": user_terms}
            mentions[user]["ratings"][product] = rate

    return mentions
async def handle_recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    artist_name = update.message.text

    if artist_name in userRates:
        response_message = makeRecommendation(artist_name, userRates, 15, 15)
    else:
        response_message = "No data found for artist '{artist_name}'."

    await update.message.reply_text(response_message)
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! Send me an artist name to get recommendations.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Send an artist name to get music recommendations.')

# Error Handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# Main Function
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_recommendation))
    app.add_error_handler(error)

    app.run_polling()
