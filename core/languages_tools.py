from deep_translator import GoogleTranslator 
import speech_recognition as sr

def Web_Translate(txt,writeIn,translateTo):
    """
    webTranslate(txt,writeIn,translateTo )
      - txt           -text to trasnlate
      - writeIn       -in which language is it written
      - translateTo   -language to be translated
    rember language prefix
    en -> english
    es -> spanish 
    ...
    """
    translatedTxt = GoogleTranslator(source=writeIn, target=translateTo).translate(txt)
    return translatedTxt


def Transcribe_and_Translate(audio_file: str,language="ru": str):
    """Transcribe Russian audio to text and translate to English."""
    recognizer = sr.Recognizer()

    # Convert the audio file to .wav format
    audio = AudioSegment.from_file(audio_file)
    converted_file = "converted_audio.wav"
    audio.export(converted_file, format="wav")

    # Load the audio for transcription
    with sr.AudioFile(converted_file) as source:
        audio_data = recognizer.record(source)

    # Transcribe the Russian audio to text
    try:
        new_text = recognizer.recognize_google(audio_data, language=language+"-"language.upper())
        # Use webTranslate function to translate the transcribed language text to English
        english_translation = webTranslate(new_text, language, 'en')
        return new_text, english_translation
    except sr.UnknownValueError:
        return None, "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        return None, f"Error: {e}"