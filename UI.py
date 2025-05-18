import streamlit as st
import pandas as pd
import pickle
import random
import speech_recognition as sr

# Load model and movie data
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    movies = pd.read_csv("movies.csv")
    return model, movies

model, movies = load_model()

# Mood to genres mapping
mood_genres = {
    "Happy": ["Comedy", "Adventure", "Family"],
    "Sad": ["Drama", "Romance"],
    "Excited": ["Action", "Thriller", "Sci-Fi"],
    "Relaxed": ["Animation", "Fantasy", "Musical"],
    "Curious": ["Documentary", "Mystery"],
}

# Voice input function
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.warning("Sorry, couldn't understand.")
        except sr.RequestError:
            st.error("Speech service down.")
    return ""

# App UI
st.title("🎬 Movie Recommendation System")
st.write("Get personalized movie suggestions based on your **mood** or **voice input**!")

# Mood input
mood = st.selectbox("Select your mood", list(mood_genres.keys()))

# Voice input (optional)
use_voice = st.checkbox("Use voice to say a movie you liked")
voice_input = ""
if use_voice:
    if st.button("Record"):
        voice_input = get_voice_input()
        st.write(f"You said: *{voice_input}*")

# Random user_id for simulation
user_id = random.randint(1, 944)

# Filter movies by genre (basic match)
def filter_movies_by_mood(mood, movies_df):
    genre_keywords = mood_genres[mood]
    return movies_df[movies_df['title'].str.contains('|'.join(genre_keywords), case=False, na=False)]

filtered_movies = filter_movies_by_mood(mood, movies)

# Recommend top N
def recommend_movies(user_id, movie_df, model, top_n=5):
    recommendations = []
    for _, row in movie_df.iterrows():
        movie_id = row['movie_id']
        title = row['title']
        pred_rating = model.predict(user_id, movie_id).est
        recommendations.append((title, pred_rating))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:top_n]

if st.button("Get Recommendations"):
    recs = recommend_movies(user_id, filtered_movies, model)
    st.subheader("🎥 Recommended Movies:")
    for title, rating in recs:
        st.markdown(f"**{title}** — ⭐ Estimated rating: {round(rating, 2)}")

    if voice_input:
        st.write(f"Recommendations are similar to: *{voice_input}*")

