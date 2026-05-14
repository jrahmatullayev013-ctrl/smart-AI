import google.generativeai as genai

# Siz yuborgan yangi va haqiqiy API kalit
API_KEY = "AIzaSyBr4lx82LSqb0Qhj7iP0noduOzvZJh2Rtc"
genai.configure(api_key=API_KEY)

# Gemini 1.5 Flash - eng aqlli va tezkor LLM modelini ulaymiz
model = genai.GenerativeModel('gemini-1.5-flash')

# Suhbat tarixi (xotira) uchun chat sessiyasini boshlaymiz
chat_session = model.start_chat(history=[])

def get_ai_answer(user_input):
    """Google Gemini orqali har qanday savolga men kabi aqlli javob berish"""
    try:
        # AI-dan javob so'raymiz
        response = chat_session.send_message(user_input)
        return response.text
    except Exception as e:
        # Agar kalitda yoki ulanishda xato bo'lsa, xatoni aniq ko'rsatadi
        return f"Kechirasiz, muloqotda xatolik bo'ldi. Xato: {str(e)}"
