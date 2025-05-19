import streamlit as st
import pandas as pd
import speech_recognition as sr
import json
from datetime import datetime

movies = pd.read_csv('movies.csv')

st.title("Movie Recommendation System")

user_id = st.number_input("Enter your User ID (1–943):", min_value=1, max_value=943, step=1)

mood = st.selectbox("What's your mood today?", ["Any", "Happy", "Sad", "Romantic", "Adventurous", "Thriller"])

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

mood_map = {
    "Happy": "Comedy",
    "Sad": "Drama",
    "Romantic": "Romance",
    "Adventurous": "Adventure",
    "Thriller": "Thriller"
}

if st.button("Recommend"):
    filtered_movies = movies
    if mood != "Any":
        genre = mood_map[mood]
        filtered_movies = movies[movies['genres'].str.contains(genre, case=False)]

    if len(filtered_movies) == 0:
        st.warning("No movies found for this mood. Showing random movies instead.")
        recommended = movies.sample(10)
    else:
        recommended = filtered_movies.sample(min(10, len(filtered_movies)))

    st.write("Recommended Movies:")
    for title in recommended['title'].values:
        st.markdown(f"- {title}")

    
    save_history(user_id, recommended['title'].tolist())

if st.button("Use Voice Input"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        st.write(f"You said: {text}")
    except Exception as e:
        st.error("Sorry, I couldn't understand.")

st.markdown("**Why these movies?**")
st.caption("These are based on your past ratings and similar user preferences.")
