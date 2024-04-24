import speech_recognition as sr
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pyautogui    
import time
import numpy as np
import pdb
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# Filter requirements.
order = 6
fs = 30.0       # sample rate, Hz
cutoff = 3.667  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)
# Define the positions of the Tic Tac Toe grid
grid_positions = {
    'didi': (775, 397),  
    'nani': (958, 404),
    'mami': (1141, 409),
    'dadi': (789, 575),
    'chacha': (956, 565),
    'papa': (1156, 576),
    'dada': (778, 752),
    'chachi': (958, 752),
    'mama': (1132, 750)
}

# Function to click on a grid position
def click_position(position):
    x, y = grid_positions[position]
    # Simulate mouse click
    pyautogui.moveTo(x, y)
    pyautogui.click(x, y)
    time.sleep(0.5)  # Adjust this delay as needed

# Function to listen for voice commands
def voice_command_listener():
    recognizer = sr.Recognizer()
    device_index = sr.Microphone.list_microphone_names().index('Headset Microphone (Realtek(R) ')
    mic = sr.Microphone(device_index=device_index)
    # pdb.set_trace()
    print(mic)
    # print(sr.Microphone.list_microphone_names())
    with mic as source:
        
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print("Command I'm here:", command)
            return command
        except sr.UnknownValueError:
            print("Couldn't understand the audio")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")
    return None

# Main loop
if __name__ == "__main__":
    while True:
        command = voice_command_listener()
        if command:
            closest_match = process.extractOne(command, grid_positions.keys(), scorer=fuzz.partial_ratio)
            if closest_match[1] > 80:  # Threshold for similarity score
                click_position(closest_match[0])
            else:
                print("No matching command found. Please try again.")
        else:
            print("No command recognized. Please try again.")