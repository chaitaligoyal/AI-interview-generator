import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
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

uploaded_file = st.file_uploader(
    "Upload Resume File(PDF)",
    type = ["pdf"]
)

resume_text = ""

if uploaded_file is not None:
    pdf_reader = PdfReader(uploaded_file)

    for page in pdf_reader.pages:
        resume_text += page.extract_text()

if st.button("Generate Questions"):

    if uploaded_file is None:
        st.warning("Please upload a resume.")

    prompt = f"""
    You are an expert technical interviewer.

    Review the resume and generate:

    1.Technical interview Questions and Answers
    2.HR interview Questions and Answers

    Also categorize technical and HR questions separately.
    Give proper spacing and formatting.

    Candidate Role: {role}
    Skills: {skills}
    Experience Level: {level}

    Resume Content: {resume_text}

    """

if st.button("Review my Resume"):

    if uploaded_file is None:
        st.warning("Please upload a resume.")

    prompt = f"""
    As an expert technical interviewer.

    Review the resume and generate:

    1.Candidate strengths
    2.Potential additions to resume to make it better
    3.Resume score (1 to 10) with 10 being the best quality resume

    Candidate Role: {role}
    Skills: {skills}
    Experience Level: {level}

    Resume Content: {resume_text}

    Format the response using:
    - clear headings
    - bullet points
    - proper spacing

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