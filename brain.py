import requests
import streamlit as st

# Tokenni bevosita yozmaymiz, uni Streamlit sozlamalaridan (Secrets) olamiz
HF_TOKEN = st.secrets["HF_TOKEN"]
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def get_ai_answer(user_input):
    payload = {
        "inputs": f"<s>[INST] {user_input} [/INST]",
        "parameters": {"max_new_tokens": 500, "temperature": 0.7}
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        # Agar model hali yuklanayotgan bo'lsa
        if response.status_code == 503:
            return "Model yuklanmoqda, iltimos 30 soniya kuting... ⏳"
        
        output = response.json()
        if isinstance(output, list) and len(output) > 0:
            return output[0].get('generated_text', '').split('[/INST]')[-1].strip()
        return "AI hozircha javob bera olmadi."
    except Exception as e:
        return f"Texnik nosozlik: {str(e)}"
