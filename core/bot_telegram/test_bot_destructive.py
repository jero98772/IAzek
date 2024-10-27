import random
import time
from datetime import timedelta
import webuiapi

from llama_cpp import Llama
import schedule
import time
from openai import OpenAI
from gtts import gTTS
import os
import json
import subprocess

import os
import speech_recognition as sr
from pydub import AudioSegment
from telegram import Update, Bot




def handle_voice_or_audio(update: Update, context: CallbackContext) -> None:
    """Handle both voice and audio messages: transcribe and translate them."""
    bot: Bot = context.bot

    # Check if it's a voice message or regular audio file
    if update.message.voice:
        logger.info("Voice message received")
        file = update.message.voice.get_file()  # Get the voice message file
    elif update.message.audio:
        logger.info("Audio file received")
        file = update.message.audio.get_file()  # Get the audio file
    else:
        logger.info("No voice or audio detected")
        return

    file_path = file.download()  # Download the audio file

    # Process the audio: transcribe and translate
    original_text, translated_text = transcribe_and_translate(file_path)

    # Send the original Russian text and the English translation back to the user
    if original_text:
        response = f"**Original Russian:**\n{original_text}\n\n**Translation (English):**\n{translated_text}"
    else:
        response = translated_text  # In case of transcription error

    # Send the response
    update.message.reply_text(response)

    # Clean up the audio file
    os.remove(file_path)

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
# Define stable diffusion positive prompt

# Example: reuse your existing OpenAI setup

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

mode="normal"
cloths=["pencil dress"]
stable_difussion_positive_promt="woman secretary"
pictures=True

# Initialize Llama model
"""
llm = Llama(
    model_path="./mixtral-8x7b-v0.1.Q6_K.gguf",
    n_ctx=2048,
    n_threads=24,
    n_gpu_layers=35,
    use_gpu=True,
    temperature=0.5,
    max_tokens=50,
)

def webTranslate(text,source,destiny):
    language_code_to_name = {"de":"deu","en":"eng","es":"spa","ru":"rus","fr":"fra","pt":"pot"}
    from seamless_communication.models.inference import Translator
    import torch 
    translator = Translator(
            "seamlessM4T_large",
            "vocoder_36langs",
            torch.device("cuda:0")
    )
    translated_text, _, _ = translator.predict(text, "t2tt", language_code_to_name[destiny], src_lang=language_code_to_name[source])
    return translated_text
"""
def read_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)
messages=read_from_json("mesajes.json")

# Initialize WebUI API for Stable Diffusion
api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)

# Initial chat messages
# Function to generate chat response

def text_to_female_voice(text, filename="output.mp3", language="en"):
    # Create a gTTS object
    tts = gTTS(text=text, lang=language, slow=False, tld="co.uk")

    # Save the audio file
    tts.save(filename)
def chat_answerlocal(llm, messages):
    response = llm.create_chat_completion(messages=messages)["choices"][0]["message"]["content"]
    return response
def chat_answer(messages):
    completion = client.chat.completions.create(
      model="TheBloke/dolphin-2.2.1-mistral-7B-GGUF",
      messages=messages,
      temperature=1.1,
    )
    #response = llm.create_chat_completion(messages=messages)["choices"][0]["message"]["content"]
    return completion.choices[0].message.content

def get_image_prompt(llm, prompt):
    response = llm.create_chat_completion(messages=[{"role": "prompt engienier", "content": "create a positive image promt for stable difussion"},{"role": "user", "content": prompt}])["choices"][0]["message"]["content"]
    return response

# Function to generate image with Stable Diffusion
def generate_image(prompt):
    result = api.txt2img(prompt=prompt,
                    negative_prompt="(deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation ",
                    seed=random.randint(0,10000),
                    steps=25,
                    sampler_index='DDIM',
                    enable_hr=True,
                    hr_scale=2,
                    hr_upscaler=webuiapi.HiResUpscaler.Latent,
                    hr_second_pass_steps=20,
                    hr_resize_x=524,
                    hr_resize_y=524,
                    denoising_strength=0.4,
                    cfg_scale=7,)
    image_path = 'generated_image.png'
    result.image.save(image_path)
    return image_path

# Schedule a message to be sent periodically (daily to weekly)


def schedule_messages(update,context):
    # Define the interval for sending messages (randomly chosen between 1 to 7 days)
    interval_days = 0#random.randint(1, 7)
    initial_delay = 3#random.randint(0, 86400)  # Random initial delay in seconds (up to 24 hours)
    
    # Schedule the job
    job_context = context.bot.get_me().id  # Using bot ID as context to send message
    schedule.every(2).seconds.do(answer_msg,[update,context], context=job_context)
    
    # Run the scheduler in a separate thread
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start command handler
def start(update, context):
    update.message.reply_text('Hello! I am your Telegram bot.')
    # Uncomment the following line to start scheduling messages
    #schedule_messages(update,context)

# Start command handler
def photo(update, context):
    message = update.message.text
    #image_path = generate_image(message)
    #context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(image_path, 'rb'))

def reconfig(update, context):
    global mode,cloths,stable_difussion_positive_promt
    message = update.message.text
    cloths=["pencil dress"]
    stable_difussion_positive_promt="woman secretary"
    mode="normal"

"""
def command(update, context):
    command = update.message.text
    if command=="pinggy":
    elif command=="website":
"""

def modef(update, context):
    global mode,cloths,stable_difussion_positive_promt,pictures
    message = update.message.text
    print(message)
    if message=="/mode normal":
        mode="normal"
        pictures=True

    elif message=="/mode ru":
        mode="ru"

    elif message=="/mode de":
        mode="de"
    if message=="/mode np":
        pictures=False
    else:
        pictures=True
    if mode=="normal" or mode=="de" or mode=="ru":
        cloths=["pencil"]
        stable_difussion_positive_promt="woman secretary"


    print(mode)

    #image_path = generate_image(stable_difussion_positive_promt+random.choice(cloths))
    #context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(image_path, 'rb'))

def do_translations_text(message,mode):
    if mode=="de":
        message=webTranslate(message,"de","en")
    elif mode=="ru":
        message=webTranslate(message,"ru","en")
    else:
        message=message
    return message

def do_translations_audio(answer,mode):
    if mode=="de":
        answer=webTranslate(answer,"en","de")
        text_to_female_voice(answer,language="de")
    elif mode=="ru":
        answer=webTranslate(answer,"en","ru")
        text_to_female_voice(answer,language="ru")
    else:
        text_to_female_voice(answer)
    return answer
def send_scheduled_message(context: CallbackContext):
    global chat_id
    chat_id = context.job.context
    messages.append({"role": "user", "content": "Hello  👋"})
    message = chat_answer(messages)

    context.bot.send_message(chat_id=chat_id, text=message)

# Automatically schedule messages when the bot starts
def schedule_message_on_start(job_queue: CallbackContext, chat_id):
    
    # Define the time interval (between 0 hour and 12 days)
    interval = random.randint(0, 21600)#6400)  # Interval in seconds

    # Add a job to the queue that repeats every `interval` seconds
    job_queue.run_repeating(send_scheduled_message, interval=interval, first=0, context=chat_id)

def is_time_in_interval(date_str, interval_start=8, interval_end=24):
    # Convert the string to a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    
    # Get the time part of the datetime object
    time_obj = date_obj.time()
    
    # Define the interval start and end times
    start_time = time(interval_start)  # e.g., 8:00 AM
    end_time = time(0) if interval_end == 24 else time(interval_end)  # e.g., 12:00 AM (midnight)
    
    # Check if the time is within the interval
    if start_time <= time_obj < end_time:
        return True
    return False

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
def set_chat_id(update, context):
    global chat_id
    chat_id = update.message.chat_id
    update.message.reply_text(f"Your Chat ID is: {chat_id}")
    #print(f"Chat ID: {chat_id}")


