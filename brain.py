import requests
import streamlit as st

# Bu model API kalit talab qilmasligi mumkin yoki ochiq bazadan foydalanadi
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"

def get_ai_answer(user_input):
    """Hugging Face orqali har qanday savolga aqlli javob berish"""
    payload = {"inputs": f"<s>[INST] {user_input} [/INST]"}
    try:
        response = requests.post(API_URL, json=payload)
        output = response.json()
        
        if isinstance(output, list) and len(output) > 0:
            full_text = output[0].get('generated_text', '')
            # Faqat javob qismini ajratib olish
            answer = full_text.split('[/INST]')[-1].strip()
            return answer
        return "AI hozircha ma'lumot topa olmadi."
    except Exception as e:
        return f"Muloqotda uzilish bo'ldi: {str(e)}"
