import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

st.title("AI Interview Question Generator")

role = st.text_input("Enter Role")
skills = st.text_input("Enter Skills")

level = st.selectbox(
    "Experience Level",
    ["Beginner", "Intermediate", "Advanced"]
)

if st.button("Generate Questions"):

    prompt = f"""
    Generate interview questions for:

    Role: {role}
    Skills: {skills}
    Level: {level}

    Also provide medium answers.
    """

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(str(e))