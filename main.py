import streamlit as st
from brain import get_ai_answer  # Miya faylini ulaymiz

# Sahifa sozlamalari (Dizayn ChatGPT/Gemini kabi toza bo'lishi uchun)
st.set_page_config(page_title="Jasurbek AI", layout="centered")

# Robot rasmini va ortiqcha yozuvlarni yo'qotish uchun CSS
st.markdown("""
    <style>
    [data-testid="stChatMessageAvatarUser"] { display: none !important; }
    [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    .stDeployButton { display:none; }
    footer { visibility: hidden; }
    [data-testid="stFileUploader"] section div { display: none; } /* 200MB yozuvini yashirish */
    </style>
""", unsafe_allow_html=True)

# 1. Kirish Tizimi (Universal Google Login simulyatsiyasi)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Log in")
    email = st.text_input("Email manzilingiz")
    password = st.text_input("Parol", type="password")
    
    if st.button("Kirish"):
        if "@gmail.com" in email and len(password) >= 6:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
        else:
            st.error("Xato! Faqat Gmail va kamida 6 belgili parol kiriting.")
else:
    # 2. Asosiy Interfeys (Siz xohlagan "+" va Profil bilan)
    col1, col2 = st.columns([8, 1])
    with col1:
        st.title("How can I help you today?")
    with col2:
        # Profil: Emailning birinchi harfi
        st.write(f"### :green[{st.session_state.user_email[0].upper()}]")

    # Rasm yuklash (Maksimal 5 ta rasm cheklovi bilan)
    uploaded_files = st.file_uploader("Rasmlarni yuklang (+)", accept_multiple_files=True, type=['png', 'jpg'])
    if uploaded_files and len(uploaded_files) > 5:
        st.error("Maksimal 5 ta rasm yuklash mumkin!")
    
    # Chat muloqoti
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Kabar yozing..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Javobni brain.py faylidagi funksiyadan olamiz
            response = get_ai_answer(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
