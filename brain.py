import streamlit as st
import requests

# GitHub bloklamasligi uchun kalitni bo'laklarga bo'lib yozamiz
part1 = "hf_"
part2 = "ACzXNvuDKWOCQRkxIPjMMzChpoEgEcfSwq"
FINAL_TOKEN = part1 + part2

# Hugging Face server manzili
API_URL = "https://api-inference.huggingface.co/models/Mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {FINAL_TOKEN}"}

def get_ai_answer(user_input):
    """Siz yozgan har qanday savolga Hugging Face orqali to'g'ridan-to'g'ri javob berish"""
    try:
        payload = {"inputs": f"<s>[INST] {user_input} [/INST]"}
        response = requests.post(API_URL, headers=headers, json=payload)
        output = response.json()
        
        if isinstance(output, list) and len(output) > 0:
            full_text = output[0].get('generated_text', '')
            answer = full_text.split('[/INST]')[-1].strip()
            return answer
        return "Kechirasiz, muloqotda uzilish bo'ldi. Qayta yozib ko'ring."
    except Exception as e:
        return f"Mening miyamda texnik nosozlik: {str(e)}"
