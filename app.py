

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import json
import pickle
import random
import numpy as np

from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import nltk

app = Flask(__name__)

lemmatizer = WordNetLemmatizer()

with open(
    'intents.json',
    'r',
    encoding='utf-8'
) as file:

    intents = json.load(file)

words = pickle.load(
    open('words.pkl','rb')
)

classes = pickle.load(
    open('classes.pkl','rb')
)

model = load_model(
    'chatbot_model.h5',compile=False
)


def clean(sentence):

    sentence_words = nltk.word_tokenize(
        sentence
    )

    sentence_words = [
        lemmatizer.lemmatize(
            word.lower()
        )
        for word in sentence_words
    ]

    return sentence_words

def bag_of_words(sentence):

    sentence_words = clean(sentence)

    bag = [0] * len(words)

    for w in sentence_words:

        for i, word in enumerate(words):

            if word == w:
                bag[i] = 1

    return np.array(bag)

def predict_class(sentence):

    bow = bag_of_words(sentence)

    result = model.predict(
        np.array([bow]),
        verbose=0
    )[0]

    max_prob = np.max(result)

    if max_prob < 0.70:
        return None

    return classes[np.argmax(result)]

def get_response(tag):

    if tag is None:
        return (
            "Sorry, I didn't understand that. Can you please rephrase?"
        )
    
    for intent in intents['intents']:

        if intent['tag'] == tag:
            return random.choice(
                intent['responses']
            )
        
    return "No response found !"    

@app.route('/')

def home():

    return render_template(
        'index.html'
    )

@app.route('/chat', methods=['POST'])

def chat():

    message = request.json['message']

    tag = predict_class(message)

    response = get_response(tag)

    return jsonify({
        "response": response
    })

if __name__ == "__main__":

    app.run(debug=True,use_reloader=False)