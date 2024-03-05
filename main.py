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
def preprocess(artist_name):
    processed_input = encode_artist_name(artist_name) 
    return processed_input

def postprocess(predictions):
    readable_predictions = decode_predictions(predictions)  
    return readable_predictions

async def get_model_predictions(artist_name):
    processed_input = preprocess(artist_name)
    predictions = model.predict(processed_input)
    readable_predictions = postprocess(predictions)
    return readable_predictions

# Modify handle_recommendation to use the new function
async def handle_recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    artist_name = update.message.text
    response_message = await get_model_predictions(artist_name)
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
