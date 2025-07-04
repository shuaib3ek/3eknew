
import streamlit as st
from apps import course_outline_app
from apps.trainer_profile_formatter import app as trainer_app

st.set_page_config(page_title="3EK Unified App", layout="wide")
st.sidebar.title("📘 3EK Unified App")

app_choice = st.sidebar.radio("Choose a module:", [
    "📄 Course Outline Generator",
    "🧑‍🏫 Trainer Profile Formatter"
])

if app_choice == "📄 Course Outline Generator":
    course_outline_app.run()
elif app_choice == "🧑‍🏫 Trainer Profile Formatter":
    trainer_app.run()
