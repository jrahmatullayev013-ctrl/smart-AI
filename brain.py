import streamlit as st
import requests

# Streamlit Secrets (Maxfiy quti) bo'limidan tokenni xavfsiz o'qib olamiz
HF_TOKEN = st.secrets["HF_TOKEN"]

# Hugging Face orqali ishlaydigan aqlli sun'iy intellekt modeli manzili
API_URL = "https://api-inference.huggingface.co/models/Mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def get_ai_answer(user_input):
    """Foydalanuvchi bergan har qanday erkin savolga Hugging Face orqali javob qaytarish"""
    try:
        payload = {"inputs": f"<s>[INST] {user_input} [/INST]"}
        response = requests.post(API_URL, headers=headers, json=payload)
        output = response.json()
        
        if isinstance(output, list) and len(output) > 0:
            full_text = output[0].get('generated_text', '')
            # Faqat sun'iy intellekt qaytargan sof javobni ajratib olamiz
            answer = full_text.split('[/INST]')[-1].strip()
            return answer
        
        return "Kechirasiz, muloqotda uzilish bo'ldi. Iltimos, qaytadan urinib ko'ring."
        
    except Exception as e:
        # Agar tizimda kutilmagan texnik nosozlik yuz bersa
        return f"Mening miyamda texnik nosozlik yuz berdi: {str(e)}"
