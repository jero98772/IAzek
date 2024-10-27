import logging
from telegram import Update
from telegram.ext import CallbackContext
import os
from typing import Optional

class BotHandlers:
    def __init__(self, config: 'Config', chat_manager: 'ChatManager', 
                 translator: 'Translator', image_generator: Optional['ImageGenerator'] = None):
        self.config = config
        self.chat_manager = chat_manager
        self.translator = translator
        self.image_generator = image_generator
        self.logger = logging.getLogger(__name__)

    async def start(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text('Hello! I am your Telegram bot.')

    async def handle_voice_or_audio(self, update: Update, context: CallbackContext) -> None:
        if update.message.voice:
            self.logger.info("Voice message received")
            file = await update.message.voice.get_file()
        elif update.message.audio:
            self.logger.info("Audio file received")
            file = await update.message.audio.get_file()
        else:
            self.logger.info("No voice or audio detected")
            return

        file_path = await file.download()
        original_text, translated_text = self.translator.transcribe_audio(file_path)

        if original_text:
            response = f"**Original Russian:**\n{original_text}\n\n**Translation (English):**\n{translated_text}"
        else:
            response = translated_text

        await update.message.reply_text(response)
        os.remove(file_path)

    async def handle_message(self, update: Update, context: CallbackContext) -> None:
        message = update.message.text
        translated_message = self.translator.translate_text(
            message, 
            source_lang=self.config.mode if self.config.mode in ['de', 'ru'] else 'en',
            target_lang='en'
        )

        response = self.chat_manager.get_response(translated_message)
        
        translated_response = self.translator.translate_text(
            response,
            source_lang='en',
            target_lang=self.config.mode if self.config.mode in ['de', 'ru'] else 'en'
        )

        self.translator.text_to_speech(
            translated_response,
            language=self.config.mode if self.config.mode in ['de', 'ru'] else 'en'
        )

        await update.message.reply_text(translated_response)
        await context.bot.send_audio(
            chat_id=update.effective_chat.id,
            audio=open('output.mp3', 'rb')
        )