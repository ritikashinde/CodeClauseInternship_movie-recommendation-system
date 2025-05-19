import streamlit as st
import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
import pickle

movies = pd.read_csv('movies.csv')
# UI
st.title("Movie Recommendation System")

user_id = st.number_input("Enter your User ID (1–943):", min_value=1, max_value=943, step=1)

# Mood-based filter input
mood = st.selectbox("What's your mood today?", ["Any", "Happy", "Sad", "Romantic", "Adventurous", "Thriller"])

if st.button("Recommend"):
    recommended = movies.sample(10)
    
    if mood != "Any":
        mood_map = {
            "Happy": "Comedy",
            "Sad": "Drama",
            "Romantic": "Romance",
            "Adventurous": "Adventure",
            "Thriller": "Thriller"
        }
        genre = mood_map[mood]
        recommended = recommended[recommended['genres'].str.contains(genre, case=False)]

    st.write("🎯 Recommended Movies:")
    for title in recommended['title'].values:
        st.markdown(f"- {title}")
        
import speech_recognition as sr

if st.button("🎤 Use Voice Input"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        st.write(f"You said: {text}")
        # You can then use this as input
    except:
        st.error("Sorry, I couldn't understand.")
st.markdown("ℹ️ **Why these movies?**")
st.caption("These are based on your past ratings and similar user preferences.")
import json
from datetime import datetime

def save_history(user_id, movies_list):
    try:
        with open('user_history.json', 'r') as f:
            history = json.load(f)
    except:
        history = {}

    if str(user_id) not in history:
        history[str(user_id)] = []

    history[str(user_id)].append({
        "time": datetime.now().isoformat(),
        "movies": movies_list
    })

    with open('user_history.json', 'w') as f:
        json.dump(history, f)

# Call this inside the recommendation button block
save_history(user_id, recommended['title'].tolist())
