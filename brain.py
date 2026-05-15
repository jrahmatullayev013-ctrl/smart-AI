import google.generativeai as genai
import streamlit as st

# Kalitni kod ichiga yozmaymiz, uni Streamlit sozlamalaridan (Secrets) olamiz
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except KeyError:
    st.error("Xatolik: GEMINI_API_KEY topilmadi. Streamlit sozlamalarini tekshiring.")

model = genai.GenerativeModel('gemini-1.5-flash')
chat_session = model.start_chat(history=[])

def get_ai_answer(user_input):
    """Google Gemini orqali aqlli javob berish"""
    try:
        response = chat_session.send_message(user_input)
        return response.text
    except Exception as e:
        return f"Muloqotda uzilish bo'ldi. Xato: {str(e)}"
