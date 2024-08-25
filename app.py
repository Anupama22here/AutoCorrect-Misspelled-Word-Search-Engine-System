import string
import re
import numpy as np
from collections import Counter
import streamlit as st

# Custom CSS 
st.markdown(
    """
    <style>
    body {
        background-color: #1A3636; 
        color: #ffffff; 
    }
    .stApp {
        background-color: #1A3636; 
        color: #ffffff;
    }
    .emoji {
        font-size: 48px;
        margin-right: 10px;
    }
    .title-text {
        font-size: 42px;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        margin-bottom: 30px; 
    }
    .stTextInput input {
        background-color: #677D6A; 
        color: #ffffff;
        border: 2px solid #1A3636;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton>button {
        background-color: #40534C;
        color: #000000;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #ffdab9; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title-text">📝 AutoCorrect Misspelled Word Search Engine System 🔍</div>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)  

# Importing data
def read_corpus(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        words = []
        for line in lines:
            words += re.findall(r'\w+', line.lower())
    return words
corpus = read_corpus(r'D:\anupama\ml projects\autocorrection_prediction\big.txt')
vocab_set = set(corpus)
word_count = Counter(corpus)
total_word_count = float(sum(word_count.values()))
word_probabilities = {word: word_count[word] / total_word_count for word in word_count.keys()}

# Defining the functions
def split(word):
    return [(word[:i], word[i:]) for i in range(len(word) + 1)]

def delete(word):
    return [left + right[1:] for left, right in split(word) if right]

def swap(word):
    return [left + right[1] + right[0] + right[2:] for left, right in split(word) if len(right) > 1]

def replace(word):
    return [left + center + right[1:] for left, right in split(word) if right for center in string.ascii_lowercase]

def insert(word):
    return [left + center + right for left, right in split(word) for center in string.ascii_lowercase]

def level_one_edits(word):
    return set(delete(word) + swap(word) + replace(word) + insert(word))

def level_two_edits(word):
    return set(e2 for e1 in level_one_edits(word) for e2 in level_one_edits(e1))

def correct_spelling(word, vocab_set, word_probabilities):
    if word in vocab_set:
        return f"{word} is already correctly spelled"
    
    # Getting all suggestions
    suggestions = level_one_edits(word) or level_two_edits(word) or [word]
    best_guesses = [w for w in suggestions if w in vocab_set]
    if not best_guesses:
        return f"Sorry, no suggestions found for {word}"
    
    suggestions_with_probabilities = [(w, word_probabilities[w]) for w in best_guesses]
    suggestions_with_probabilities.sort(key=lambda x: x[1], reverse=True)
    
    return f"Suggestions for {word}: " + ', '.join([f"{w} ({prob:.2%})" for w, prob in suggestions_with_probabilities[:10]])

# Streamlit app
# Capturing user input
input_word = st.text_input('🔍 Enter a word to check for spelling:', '')

# Button to trigger spelling correction
if st.button('Check'):
    if input_word:  
        result = correct_spelling(input_word, vocab_set, word_probabilities)
        st.write(result)
    else:
        st.write("⚠️ Please enter a word to check.")
