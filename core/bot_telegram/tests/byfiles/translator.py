from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment

class Translator:
    @staticmethod
    def translate_text(text: str, source_lang: str, target_lang: str) -> str:
        return GoogleTranslator(source=source_lang, target=target_lang).translate(text)

    @staticmethod
    def text_to_speech(text: str, filename: str = "output.mp3", language: str = "en") -> None:
        tts = gTTS(text=text, lang=language, slow=False, tld="co.uk")
        tts.save(filename)

    @staticmethod
    def transcribe_audio(audio_file: str) -> tuple[str | None, str]:
        recognizer = sr.Recognizer()
        
        # Convert audio to wav
        audio = AudioSegment.from_file(audio_file)
        converted_file = "converted_audio.wav"
        audio.export(converted_file, format="wav")
        
        with sr.AudioFile(converted_file) as source:
            audio_data = recognizer.record(source)
            
        try:
            russian_text = recognizer.recognize_google(audio_data, language="ru-RU")
            english_translation = Translator.translate_text(russian_text, 'ru', 'en')
            return russian_text, english_translation
        except sr.UnknownValueError:
            return None, "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return None, f"Error: {e}"