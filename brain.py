import requests

# Siz yuborgan Hugging Face Access Token
HF_TOKEN = "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"
# Mistral modeli - aqlli va erkin muloqot qiladi
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def get_ai_answer(user_input):
    """Hugging Face orqali har qanday savolga javob berish"""
    payload = {
        "inputs": f"<s>[INST] {user_input} [/INST]",
        "parameters": {"max_new_tokens": 500, "temperature": 0.7}
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        output = response.json()
        if isinstance(output, list) and len(output) > 0:
            full_text = output[0].get('generated_text', '')
            answer = full_text.split('[/INST]')[-1].strip()
            return answer
        return "Kechirasiz, muloqotda xatolik bo'ldi."
    except:
        return 
