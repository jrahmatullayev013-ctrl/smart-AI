import streamlit as st
import requests

# Streamlit Secrets bo'limidan maxfiy tokenni xavfsiz o'qib olamiz
HF_TOKEN = st.secrets["HF_TOKEN"]

API_URL = "https://api-inference.huggingface.co/models/Mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def get_ai_answer(user_input):
    """Hugging Face orqali har qanday savolga erkin va aqlli javob berish"""
    try:
        payload = {"inputs": f"<s>[INST] {user_input} [/INST]"}
        response = requests.post(API_URL, headers=headers, json=payload)
        output = response.json()
        
        if isinstance(output, list) and len(output) > 0:
            full_text = output[0].get('generated_text', '')
            answer = full_text.split('[/INST]')[-1].strip()
            return answer
        return "Kechirasiz, muloqotda xatolik bo'ldi."
    except Exception as e:
        return f"Mening miyamda texnik nosozlik: {str(e)}"
