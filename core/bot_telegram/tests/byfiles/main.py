from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import logging
from config import Config
from chat_manager import ChatManager
from translator import Translator
from image_generator import ImageGenerator
from bot_handlers import BotHandlers

def main():
    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Initialize components
    config = Config()
    chat_manager = ChatManager(config.base_url, config.api_key)
    translator = Translator()
    image_generator = ImageGenerator(config.webui_host, config.webui_port)
    
    # Initialize bot handlers
    handlers = BotHandlers(config, chat_manager, translator, image_generator)
    
    # Create application
    application = ApplicationBuilder().token(config.telegram_token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(MessageHandler(
        filters.VOICE | filters.AUDIO, 
        handlers.handle_voice_or_audio
    ))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handlers.handle_message
    ))
    
    # Start bot
    application.run_polling()

if __name__ == '__main__':
    main()
