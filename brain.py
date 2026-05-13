import google.generativeai as genai

# Skrinshotingizdagi API kalitni o'zim joyladim
API_KEY = "AlzaSyAk8NKPaGwHKN44w7q3hbgSTUTTtVaLB0o"
genai.configure(api_key=API_KEY)

# Gemini 1.5 Flash - eng aqlli va tezkor model
model = genai.GenerativeModel('gemini-1.5-flash')

# Suhbat tarixi (xotira) uchun chat sessiyasini boshlaymiz
chat_session = model.start_chat(history=[])

def get_ai_answer(user_input):
    """Har qanday savolga Google Gemini orqali aqlli javob berish"""
    try:
        # AI-dan javob so'raymiz
        response = chat_session.send_message(user_input)
        return response.text
    except Exception as e:
        # Xatolik bo'lsa (masalan, internet uzilsa)
        return "Kechirasiz, muloqotda kichik xatolik bo'ldi. Iltimos, qaytadan urinib ko'ring."
