from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext,CallbackQueryHandler
from core.tools.data_base import create_user,create_bot
from dotenv import load_dotenv
import os

load_dotenv()
def choose_bot_type(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    bot_type = query.data

    # Check which bot type was chosen and proceed accordingly
    if bot_type == "generic_male":
        create_user(query.message.chat_id, bot_id="generic_male", language=context.user_data["chosen_language"])
        query.edit_message_text(text="You've created a generic male bot. Enjoy!")
        print("end")
        bot_id = create_bot("casual", "male", "european", 30, "brown", "straight", "brown", "normal", None,
                   "normal", "extroverted", "teacher", "languages", "casual", "best friends")
    
    elif bot_type == "generic_female":
        create_user(query.message.chat_id, bot_id="generic_female", language=context.user_data["chosen_language"])
        query.edit_message_text(text="You've created a generic female bot. Enjoy!")
        print("end")
        bot_id = create_bot("casual", "female", "european", 30, "brown", "straight", "brown", "normal", "normal",
                   "normal", "extroverted", "teacher", "languages", "casual", "best friends")
    
    user_id = update.message.chat_id
    #bot_data = context.user_data["bot_data"]
    #create_user(user_id, bot_id=None, language=context.user_data["chosen_language"], **bot_data)
    update_user(chat_id, bot_id=None, language=None, level=None, weaknesses=None, strengths=None, modes=None, current_mode=None, sentiments=None)
    update.message.reply_text("Your bot has been created! Enjoy your experience.")
    """elif bot_type == "custom_bot":
        context.user_data["bot_data"] = {}  # Start with empty attributes
        prompt_custom_bot(query, context)
        print("end")
    """
def prompt_custom_bot(query, context):
    # Ask the user to set custom attributes one by one, starting with "style"
    query.edit_message_text(text="Let's start setting up your custom bot!")
    query.message.reply_text("Please choose a style for your bot:")
    # Further prompts to configure each attribute would follow in similar style.

def set_style(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chosen_style = query.data

    # Save the chosen style
    context.user_data["bot_data"]["style"] = chosen_style
    query.answer()
    query.edit_message_text(text=f"Style set to: {chosen_style}")
    
    # Continue prompting the user for the next attribute (e.g., gender)
    query.message.reply_text("Please choose a gender for your bot:")



# Define callback function to handle language choice
def choose_language(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chosen_language = query.data
    print("something")
    # Confirm language choice to the user
    query.answer()
    query.edit_message_text(text=f"Great! You've selected {chosen_language}.")

    # Save the chosen language to context to use later in bot setup
    context.user_data["chosen_language"] = chosen_language

    # Prompt user to choose between a generic or custom bot
    keyboard = [
        [InlineKeyboardButton("Generic Male Bot", callback_data="generic_male")],
        [InlineKeyboardButton("Generic Female Bot", callback_data="generic_female")]
        #[InlineKeyboardButton("Create Custom Bot", callback_data="custom_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text("Do you want a generic male/female bot or create a custom bot?", reply_markup=reply_markup)
    update_user(chat_id, bot_id=None, language=chosen_language, level=None, weaknesses=None, strengths=None, modes=None, current_mode=None, sentiments=None)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot!')
    # Create inline keyboard with language options
    languages = os.getenv("LANGUAGES").split(",")
    keyboard = [[InlineKeyboardButton(lang, callback_data=lang)] for lang in languages]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the keyboard to the user
    update.message.reply_text('Select a language:', reply_markup=reply_markup)
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot!')
    # Create inline keyboard with language options
    languages = os.getenv("LANGUAGES").split(",")
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
    dp.add_handler(CallbackQueryHandler(choose_bot_type, pattern="^generic_|^custom_bot"))
    dp.add_handler(CallbackQueryHandler(set_style, pattern="^style_"))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()