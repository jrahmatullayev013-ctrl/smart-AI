import google.generativeai as genai

API_KEY = "AlzaSyAk8NKPaGwHKN44w7q3hbgSTUTTtVaLB0o"
genai.configure(api_key=API_KEY)

def get_ai_answer(user_input):
    """Barcha savolga aqlli javob berish"""
    try:
        # AI-dan javob so'raymiz
        response = chat_session.send_message(user_input)
        return response.text
    except Exception as e:
        # Agar kalitda yoki ulanishda xato bo'lsa, aniq xatoni ko'rsatadi
        return f"Kechirasiz, muloqotda xatolik bo'ldi. Xato: {str(e)}"
