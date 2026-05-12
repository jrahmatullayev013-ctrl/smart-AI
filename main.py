import streamlit as st
import uuid
from brain import get_ai_answer  # Yangi "miya" faylini ulaymiz

# 1. Sahifa dizayni (ChatGPT/Gemini kabi toza Dark Mode)
st.set_page_config(page_title="ChatGPT", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #212121; color: #ececf1; }
    div[data-testid="stFileUploaderDropzoneInstructions"] > div > small { display: none !important; }
    div[data-testid="stFileUploaderDropzoneInstructions"] > div > span { font-size: 0px !important; }
    div[data-testid="stFileUploaderDropzoneInstructions"] > div > span::before { content: "+"; font-size: 30px; color: #10a37f; }
    .user-profile {
        position: fixed; top: 12px; right: 25px;
        background-color: #10a37f; color: white;
        width: 38px; height: 38px; border-radius: 50%;
        text-align: center; line-height: 38px;
        font-weight: bold; z-index: 1000; font-size: 18px;
    }
    [data-testid="stChatMessageAvatarAssistant"], [data-testid="stChatMessageAvatarUser"] { display: none !important; }
    [data-testid="stChatMessage"] { padding-left: 0px !important; background-color: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<br><br><br><h1 style='text-align: center; font-size: 45px;'>Log in or Sign up</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        email = st.text_input("Email", placeholder="name@gmail.com")
        password = st.text_input("Password", type="password")
        if st.button("Continue", type="primary", use_container_width=True):
            if email.endswith("@gmail.com") and len(password) >= 6:
                st.session_state.user_email = email
                st.session_state.user_letter = email[0].upper()
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Xato: Gmail va 6 belgili parol kiriting!")
else:
    st.markdown(f'<div class="user-profile">{st.session_state.user_letter}</div>', unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("<h2 style='color: white;'>ChatGPT</h2>", unsafe_allow_html=True)
        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    if not st.session_state.messages:
        username = st.session_state.user_email.split('@')[0].capitalize()
        st.markdown(f"<br><br><br><h1 style='text-align: center;'>Здравствуйте, {username}!</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: gray;'>What can I help with?</h2>", unsafe_allow_html=True)

    files = st.file_uploader("", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=None):
            st.markdown(message["content"])

    if prompt := st.chat_input("Message ChatGPT..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=None):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=None):
            # Endi javobni brain.py faylidan olamiz
            response = get_ai_answer(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
