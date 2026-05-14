import google.generativeai as genai

# Sizning Google Gemini API kalitingiz
API_KEY = "AlzaSyAk8NKPaGwHKN44w7q3hbgSTUTTtVaLB0o"
genai.configure(api_key=API_KEY)

# Gemini 1.5 Flash modelini (haqiqiy LLM) ishga tushiramiz
model = genai.GenerativeModel('gemini-1.5-flash')
chat_session = model.start_chat(history=[])

def get_ai_answer(user_input):
    """Google Gemini orqali har qanday savolga aqlli va erkin javob berish"""
    try:
        response = chat_session.send_message(user_input)
        return response.text
    except Exception as e:
        return f"Kechirasiz, muloqotda xatolik bo'ldi. Xato: {str(e)}"
