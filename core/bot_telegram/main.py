from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext,CallbackQueryHandler
from core.tools.data_base import create_user,create_bot
from dotenv import load_dotenv
import os

load_dotenv()

# Define callback function to handle language choice
def choose_language(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chosen_language = query.data

    # Confirm language choice to the user
    query.answer()
    query.edit_message_text(text=f"Great! You've selected {chosen_language}.")

    # Create user profile with chosen language and default parameters
    user_id = query.message.chat_id
    create_user(user_id, bot_id=None, language=chosen_language, level=1, weaknesses=[], strengths=[])

    # Inform the user that the setup is complete
    query.message.reply_text(f"You are all set to start learning {chosen_language}!")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot!')
    # Create inline keyboard with language options

    keyboard = [[InlineKeyboardButton(lang, callback_data=lang)] for lang in languages]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the keyboard to the user
    update.message.reply_text('Select a language :', reply_markup=reply_markup)

# Define callback function to handle language c
# Echo message handler
def echo(update, context):
    pass

def main():

    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
    updater = Updater("7027699964:AAElgsjwqRUP7CU0NWWdbItgyLoIAkxzJT0", use_context=True)

    dp = updater.dispatcher
    #print("chat id",chat_id)
    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CallbackQueryHandler(choose_language))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()