from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot!')

# Echo message handler
def echo(update, context):
    global chat_id,pictures
    chat_id=update.effective_chat.id

    message = update.message.text
    messages.append({"role": "user", "content": message})
    message=do_translations_text(message,mode)  

    print(mode)
    answer = str(chat_answer(messages))
    messages.append({"role": "assistant", "content": answer})
    answer=do_translations_audio(answer,mode)

    print(answer)

    print(pictures)

    update.message.reply_text(answer)
    save_to_json(messages,"mesajes.json")
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open('output.mp3', 'rb'))
    print(update.effective_chat.id)


def main():

    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
    updater = Updater("7027699964:AAElgsjwqRUP7CU0NWWdbItgyLoIAkxzJT0", use_context=True)

    dp = updater.dispatcher
    #print("chat id",chat_id)
    dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("photo", photo))
    dp.add_handler(CommandHandler("mode", modef))
    #dp.add_handler(CommandHandler("command", command))
    dp.add_handler(CommandHandler("reconfig", reconfig))
    dp.add_handler(CommandHandler("set_chat_id", set_chat_id))  # New command to get chat ID
    try:
        schedule_message_on_start(updater.job_queue, chat_id)
    except:
        pass

    dp.add_handler(MessageHandler(Filters.voice | Filters.audio, handle_voice_or_audio))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()


print("w")