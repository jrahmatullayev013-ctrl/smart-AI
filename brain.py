import streamlit as st
import google.generativeai as genai

# Streamlit Secrets'dan kalitni xavfsiz o'qib olamiz
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

def get_ai_answer(user_question):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_question)
        return response.text
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"
