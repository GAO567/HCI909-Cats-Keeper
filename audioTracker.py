import mediapipe as mp
import numpy as np
import sounddevice as sd
import telebot
from random import choice


#telebot, change id if you want to receive messages from your bot
BOT_TOKEN = '6662534510:AAGocIvjIHkuhHuCgEVM6eqRJPutFQDhnK0'
CHAT_ID = '5761848029'

bot = telebot.TeleBot(BOT_TOKEN)
nonmeow_counter = 0
meow_time_counter = 0
meow_state = False

catswords_1 = ["Open the door, please",
            "I want to enter you bedroom",
            "Let me out of the bedroom",
            "Human, door",
            "I need your help",
            "Open please"]

catswords_2 = []

def get_words():
    global catswords_1, catswords_2

    if not catswords_1:
        catswords_1 = catswords_2
        catswords_2 = []
        
    random_word = choice(catswords_1)
    catswords_2 += [random_word]
    catswords_1.remove(random_word)
    print(catswords_1)
    print(catswords_2)

    return random_word


AudioData = mp.tasks.components.containers.AudioData


# Define the AudioClassifier, AudioClassifierOptions, etc.
AudioClassifier = mp.tasks.audio.AudioClassifier
AudioClassifierOptions = mp.tasks.audio.AudioClassifierOptions
AudioClassifierResult = mp.tasks.audio.AudioClassifierResult
AudioRunningMode = mp.tasks.audio.RunningMode
BaseOptions = mp.tasks.BaseOptions

desired_buffer_ms = 1000


def calculate_blocksize(sample_rate, buffer_ms):
    return int((sample_rate / 1000) * buffer_ms)

def audio_callback(indata, frames, time, status):
    # Convert the input data to a NumPy array
    audio_data = np.array(indata)

    # Normalize the audio data and create an AudioData object
    audio_data = AudioData.create_from_array(
        audio_data.astype(float) / np.iinfo(np.int16).max, sample_rate)

    # Perform asynchronous audio classification with a timestamp
    classifier.classify_async(audio_data, timestamp_ms=int(time.inputBufferAdcTime * 975))


# Define the print_result function
def print_result(result: AudioClassifierResult, timestamp_ms: int):
    global meow_state
    global meow_time_counter
    global nonmeow_counter

    meow_time_counter += 1

    if result.classifications[0].categories[0].score > 0.5:
        print("Cat detected, open the door!")
        nonmeow_counter = 0
        if (meow_state == False):
            bot.send_message(CHAT_ID, get_words())
            print("Sent a message")
            meow_state = True
            meow_time_counter = 0
    else:
        print("Cat not detected")
        if (meow_state == True):
            nonmeow_counter += 1
            if (nonmeow_counter > 10):
                meow_state = False
                nonmeow_counter = 0
                print('finished meowing, reset the state')
            if (meow_time_counter > 20):
                bot.send_message(CHAT_ID, "I repeat: " + get_words())
                meow_time_counter = 0
                print("meowing for too long, sending a new message")
    



#options for the audio classifier
options = AudioClassifierOptions(
    base_options=BaseOptions(model_asset_path='classifier.tflite'),
    running_mode=AudioRunningMode.AUDIO_STREAM,
    max_results=5,
    category_allowlist=['Cat'],
    result_callback=print_result)

# Create an AudioClassifier object
with AudioClassifier.create_from_options(options) as classifier:
    sample_rate = sd.query_devices(None, 'input')['default_samplerate']
    blocksize = calculate_blocksize(sample_rate, desired_buffer_ms)

    with sd.InputStream(callback=audio_callback, channels=1, dtype=np.int16, samplerate=sample_rate, blocksize=blocksize):
        print("Audio stream is running. Press Ctrl+C to stop.")

        try:
            sd.sleep(86400)  # Run the audio stream for a day
        except KeyboardInterrupt:
            print("\nAudio stream stopped.")
            
