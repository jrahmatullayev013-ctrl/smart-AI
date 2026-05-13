import streamlit as st
from brain import get_ai_answer  # brain.py faylini ulaymiz [cite: 363]

# Sahifa sozlamalari (ChatGPT/Gemini uslubida)
st.set_page_config(page_title="Jasurbek AI", layout="centered")

# Robot rasmini va ortiqcha texnik yozuvlarni olib tashlash (CSS) [cite: 322, 323, 354]
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stChatMessage [data-testid="stChatMessageAvatar"] {display: none;}
    .stFileUploader section {padding: 0; background-color: transparent;}
    </style>
    """, unsafe_allow_html=True)

# 1. Google Login (Simulyatsiya) [cite: 311, 356]
if 'user' not in st.session_state:
    st.title("Log in to Jasurbek AI")
    email = st.text_input("Email (Gmail)")
    password = st.text_input("Password", type="password")
    
    if st.button("Continue"):
        if "@gmail.com" in email and len(password) >= 6:
            st.session_state['user'] = email
            st.rerun()
        else:
            st.error("Xato: Faqat @gmail.com va kamida 6 belgili parol kiriting!")
else:
    # 2. Asosiy Interfeys
    user_email = st.session_state['user']
    first_letter = user_email[0].upper()
    
    # O'ng tepada profil (email harfi) [cite: 231, 285]
    col1, col2 = st.columns([8, 1])
    with col2:
        st.markdown(f"<h2 style='background-color:green; border-radius:50%; text-align:center; color:white;'>{first_letter}</h2>", unsafe_allow_html=True)

    st.title("How can I help you today?") # ChatGPT style fon [cite: 236]

    # 3. Rasm yuklash (5 ta limit) [cite: 211, 234, 414]
    uploaded_files = st.file_uploader("Rasmlarni yuklang (+)", accept_multiple_files=True, type=['png', 'jpg'])
    if uploaded_files and len(uploaded_files) > 5:
        st.error("Xato: Faqat 5 tagacha rasm yuklash mumkin!")
    
    # 4. Chat mantiqi [cite: 271, 336]
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Xabar yozing..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # "Miya"dan javob olish 
        response = get_ai_answer(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
