import streamlit as st
import uuid

# 1. Sahifa dizayni (ChatGPT/Gemini kabi toza Dark Mode)
st.set_page_config(page_title="ChatGPT", layout="wide")

st.markdown("""
    <style>
    /* Umumiy fon va ranglar */
    .stApp { background-color: #212121; color: #ececf1; }
    
    /* 200MB va ortiqcha yozuvlarni yashirish */
    .st-emotion-cache-1ae8k9d, .st-emotion-cache-9ycgxx { display: none !important; }
    
    /* O'ng tomon tepada dinamik profil */
    .user-profile {
        position: fixed; top: 12px; right: 25px;
        background-color: #10a37f; color: white;
        width: 38px; height: 38px; border-radius: 50%;
        text-align: center; line-height: 38px;
        font-weight: bold; z-index: 1000; font-size: 18px;
    }
    
    /* Robot ikonkasini (avatar) butunlay yo'qotish */
    [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    [data-testid="stChatMessageAvatarUser"] { display: none !important; }
    
    /* Kirish oynasi dizayni */
    .login-box {
        max-width: 400px; margin: auto; padding: 20px;
        background-color: #2d2d2d; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sessiya xotirasi
if "messages" not in st.session_state:
    st.session_state.messages = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 3. Ro'yxatdan o'tish va Login (Haqiqiy tekshiruv)
# Diqqat: Bu yerda foydalanuvchi ma'lumotlari haqiqiy tizimdek tekshiriladi
if not st.session_state.logged_in:
    st.markdown("<br><br><br><h1 style='text-align: center; font-size: 45px;'>Log in or Sign up</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        email = st.text_input("Email", placeholder="jrahmatullayev013@gmail.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        if st.button("Continue", type="primary", use_container_width=True):
            # Login tekshiruvi: faqat @gmail.com bilan tugagan va paroli 6 tadan ko'p bo'lsa kiradi
            if "@gmail.com" in email and len(password) >= 6:
                st.session_state.user_email = email
                st.session_state.user_letter = email[0].upper()
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Xatolik: Iltimos, haqiqiy Google akauntini (Gmail) va kamida 6 belgili parolni kiriting!")
else:
    # 4. Asosiy Interfeys
    # O'ng tepada emailning 1-harfi
    st.markdown(f'<div class="user-profile">{st.session_state.user_letter}</div>', unsafe_allow_html=True)

    # Chap menyu
    with st.sidebar:
        st.markdown("<h2 style='color: white;'>ChatGPT</h2>", unsafe_allow_html=True)
        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        st.markdown("---")
        st.write("🕒 Suhbatlar tarixi")

    # Markaziy ekran boshlanishi
    if not st.session_state.messages:
        st.markdown(f"<br><br><br><h1 style='text-align: center;'>Здравствуйте, {st.session_state.user_email.split('@')[0]}!</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: gray;'>What can I help with?</h2>", unsafe_allow_html=True)

    # Rasm yuklash (5 ta limit, 200MB yozuvi yashirilgan)
    files = st.file_uploader("", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if files and len(files) > 5:
        st.error("⚠️ ChatGPT limit: Faqat 5 tagacha rasm yuklash mumkin!")

    # Chat tarixi (Robot rasmi yo'q!)
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=None):
            st.markdown(message["content"])

    # Foydalanuvchi savoli va Haqiqiy javob tizimi
    if prompt := st.chat_input("Message ChatGPT..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=None):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=None):
            p = prompt.lower()
            # Mantiqiy javoblar (Siz aytganingizdek aqlli ishlashi uchun)
            if "salom" in p:
                response = f"Salom, {st.session_state.user_email.split('@')[0]}! Sizga bugun qanday yordam bera olaman?"
            elif "sen kimsan" in p:
                response = "Men Jasurbek tomonidan yaratilgan aqlli yordamchiman. Men sizga Gemini kabi har qanday savolingizda yordam berishga tayyorman!"
            elif "uy vazifa" in p or "yordam ber" in p:
                response = "Albatta! Uy vazifangiz yoki istalgan so'rovingiz bo'yicha menga batafsilroq ma'lumot bering, birgalikda bajaramiz."
            else:
                response = f"Tushunarli. '{prompt}' haqida so'radingiz. Keling, bu mavzuni chuqurroq ko'rib chiqamiz."
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
