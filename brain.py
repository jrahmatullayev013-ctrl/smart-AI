import google.generativeai as genai

# Google Gemini API kalitingiz (Aynan siz olgan kalit joylashtirildi)
API_KEY = "AlzaSyAk8NKPaGwHKN44w7q3hbgSTUTTtVaLB0o"
genai.configure(api_key=API_KEY)

# Gemini 1.5 Flash - eng aqlli va tezkor modelni ulaymiz [cite: 428]
model = genai.GenerativeModel('gemini-1.5-flash')

# Suhbat tarixi (xotira) uchun chat sessiyasini boshlaymiz [cite: 400, 428]
chat_session = model.start_chat(history=[])

def get_ai_answer(user_input):
    """Google Gemini orqali har qanday savolga men kabi aqlli javob berish"""
    try:
        # AI-dan javob so'raymiz [cite: 428]
        response = chat_session.send_message(user_input)
        return response.text
    except Exception as e:
        # Agar kalitda yoki ulanishda xato bo'lsa, xatoni ko'rsatadi
        return f"Kechirasiz, muloqotda xatolik bo'ldi. Xato: {str(e)}"
