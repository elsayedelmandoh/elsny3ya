import json 
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from fuzzywuzzy import fuzz

import colorama 
colorama.init()
from colorama import Fore, Style, Back

import random
import pickle

with open("intents.json") as file:
    data = json.load(file)


def chat():
    # load trained model
    model = keras.models.load_model('chat_model')

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    max_len = 20

    while True:
        
        inp = input(Fore.LIGHTBLUE_EX + "You: " + Style.RESET_ALL)
        if inp.lower() == "quit":
            break
        
        print(Fore.LIGHTBLUE_EX + "You:" + Style.RESET_ALL, inp)  # Display user input

        best_similarity = -1
        best_response = None

        for intent in data['intents']:
            for idx, pattern in enumerate(intent['patterns']):
                if idx < len(intent['responses']):
                    similarity = fuzz.partial_ratio(inp.lower(), pattern.lower())
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_response = intent['responses'][idx]

        if best_similarity > 70 and best_response:  # Set a threshold for similarity
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL, best_response)
        else:
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL, "I'm sorry, I don't understand.")
            
print(Fore.YELLOW + "Start messaging with the bot (type quit to stop)!" + Style.RESET_ALL)
chat()