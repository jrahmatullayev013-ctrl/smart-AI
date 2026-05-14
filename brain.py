import google.generativeai as genai

# Sizning API kalitingiz (Skrinshotdan olindi)
API_KEY = "AlzaSyAk8NKPaGwHKN44w7q3hbgSTUTTtVaLB0o"
genai.configure(api_key=API_KEY)

# Gemini 1.5 Flash modelini sozlash
model = genai.GenerativeModel('gemini-1.5-flash')
chat_session = model.start_chat(history=[])

def get_ai_answer(user_input):
    """Google Gemini orqali har qanday savolga aqlli javob berish"""
    try:
        # AI-dan javob so'rash
        response = chat_session.send_message(user_input)
        return response.text
    except Exception as e:
        # Agar xato bo'lsa, xatolikni qaytarish
        return f"Kechirasiz, muloqotda kichik xatolik bo'ldi. Xato: {str(e)}"
