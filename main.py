import streamlit as st
import uuid

# 1. Sahifa dizayni (To'liq ChatGPT Dark Mode)
st.set_page_config(page_title="ChatGPT", layout="wide")

# CSS orqali dizaynni ChatGPT bilan 1-ga-1 qilish
st.markdown("""
    <style>
    .stApp { background-color: #212121; color: #ececf1; }
    
    /* O'ng tomon tepada dinamik profil */
    .user-profile {
        position: fixed; top: 12px; right: 25px;
        background-color: #10a37f; color: white;
        width: 38px; height: 38px; border-radius: 50%;
        text-align: center; line-height: 38px;
        font-weight: bold; z-index: 1000; font-size: 18px;
    }
    
    .stChatInput { border-radius: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sessiya xotirasi
if "messages" not in st.session_state:
    st.session_state.messages = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 3. Ro'yxatdan o'tish va Kirish (Registration)
if not st.session_state.logged_in:
    st.markdown("<br><br><br><h1 style='text-align: center; font-size: 45px;'>Log in or Sign up</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Smarter responses, image uploads, and more.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        email = st.text_input("Email manzilingiz", placeholder="name@example.com")
        password = st.text_input("Parol", type="password", placeholder="••••••••")
        
        if st.button("Continue", type="primary", use_container_width=True):
            if email and len(password) >= 6:
                st.session_state.user_email = email
                st.session_state.user_letter = email[0].upper() # Emailning 1-harfini olish
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Iltimos, email va kamida 6 belgili parol kiriting!")
        
        st.markdown("<p style='text-align: center;'>OR</p>", unsafe_allow_html=True)
        st.button("Continue with Google", use_container_width=True)

# 4. Asosiy Interfeys (Tizimga kirgandan so'ng)
else:
    # Profil belgisini email harfi bilan chiqarish
    st.markdown(f'<div class="user-profile">{st.session_state.user_letter}</div>', unsafe_allow_html=True)

    # Sidebar (Chap menyu)
    with st.sidebar:
        st.markdown("<h2 style='color: white;'>ChatGPT</h2>", unsafe_allow_html=True)
        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        st.markdown("---")
        st.write("🕒 Suhbatlar tarixi")
        st.markdown("<div style='position: fixed; bottom: 20px;'>⚙️ Settings<br>❓ Help</div>", unsafe_allow_html=True)

    # Markaziy qism
    if not st.session_state.messages:
        st.markdown("<br><br><br><h1 style='text-align: center; font-size: 45px;'>What can I help with?</h1>", unsafe_allow_html=True)

    # Rasm yuklash (Qat'iy 5 ta limit)
    files = st.file_uploader("", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if files and len(files) > 5:
        st.error("⚠️ ChatGPT limit: Faqat 5 tagacha rasm yuklash mumkin!") [cite: 194, 207, 216]

    # Chat xabarlari (Robot rasmi yo'q!)
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=None): [cite: 232]
            st.markdown(message["content"])

    # Foydalanuvchi savoli
    if prompt := st.chat_input("Message ChatGPT..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=None):
            st.markdown(prompt)

        # AI aqlli javobi (Muloqot mantiqi)
        with st.chat_message("assistant", avatar=None):
            if "salom" in prompt.lower():
                response = f"Salom! Men sizning aqlli yordamchingizman. Sizga bugun qanday yordam bera olaman?" [cite: 230]
            elif "rahmat" in prompt.lower():
                response = "Arziydi! Har doim xizmatingizdaman."
            else:
                response = f"Tushunarli. '{prompt}' bo'yicha ma'lumotlarni tahlil qilyapman. Buni qanday davom ettiramiz?"
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
