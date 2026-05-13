def get_ai_answer(user_input):
    """Foydalanuvchi savoliga qarab aqlli javob qaytarish"""
    text = user_input.lower().strip()
    
    # Savol-javoblar bazasi
    if "salom" in text:
        return "Va alaykum assalom! Sizga qanday yordam bera olaman?"
    
    elif "ronaldo kim" in text or "ronaldo haqida" in text:
        return "Krishtianu Ronaldu — Portugaliyalik futbol afsonasi, ko'plab 'Oltin to'p' sohibi va tarixdagi eng kuchli hujumchilardan biri."
    
    elif "sen kimsan" in text or "isming nima" in text:
        return "Men Jasurbek tomonidan yaratilgan aqlli yordamchiman. Sizga Gemini kabi aqlli javob berishga harakat qilaman."
    
    elif "nima qila olasan" in text:
        return "Men savollarga javob berishim, rasmlarni tahlil qilishim (limit bilan) va siz bilan suhbatlashishim mumkin."
    
    else:
        return "Bu juda qiziqarli savol! Men hozircha bu haqda o'rganyapman, lekin sizga yordam berishga harakat qilaman."
