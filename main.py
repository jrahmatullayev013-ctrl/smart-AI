import streamlit as st
import uuid
import json
import os

# 1. Dizayn sozlamalari (ChatGPT va Gemini uslubida)
st.set_page_config(page_title="Jasurbek AI", layout="wide")

# Dark mode uslubini kuchaytirish
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; height: 50px; font-weight: bold; }
    .chat-container { max-width: 800px; margin: auto; }
    </style>
    """, unsafe_allow_html=True)

# 2. Ma'lumotlar bazasi
DB_FILE = 'ai_database.json'
def yuklash():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return {"users": {}}

def saqlash(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f, indent=4)

if 'data' not in st.session_state:
    st.session_state.data = yuklash()

# 3. Kirish jarayoni (ChatGPT skrinshotingizdagi kabi)
if 'user_name' not in st.session_state:
    st.markdown("<br><br><br><h1 style='text-align: center; font-size: 50px;'>What are you working on?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Log in to get smarter responses and upload files.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Continue with Google", type="primary"):
            st.session_state.user_name = f"Google_User_{str(uuid.uuid4())[:6]}"
            st.rerun()
        st.markdown("<p style='text-align: center;'>OR</p>", unsafe_allow_html=True)
        email = st.text_input("", placeholder="Email address")
        if st.button("Continue"):
            if email:
                st.session_state.user_name = email
                st.rerun()

else:
    # 4. Asosiy Chat Interfeysi (Gemini va ChatGPT uyg'unligi)
    u_name = st.session_state.user_name
    
    # Chap menyu (Tugmalarsiz, toza dizayn)
    with st.sidebar:
        st.markdown("<h2 style='color: #4285F4;'>ChatGPT</h2>", unsafe_allow_html=True)
        st.button("New chat", use_container_width=True)
        st.markdown("---")
        st.caption("Suhbatlar tarixi")
        st.markdown("<div style='position: fixed; bottom: 20px;'>Settings<br>Help</div>", unsafe_allow_html=True)

    # Markaziy chat maydoni
    st.markdown("<h3 style='text-align: center;'>ChatGPT</h3>", unsafe_allow_html=True)
    
    # Rasm yuklash cheklovi (Max 5 ta)
    files = st.file_uploader("", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    
    if files:
        if len(files) > 5:
            st.error("⚠️ ChatGPT limit: You can only upload up to 5 images.")
        else:
            st.success(f"{len(files)} files uploaded successfully.")

    # Chat xabarlari
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Foydalanuvchi savoli
    prompt = st.chat_input("Ask anything")
    
    if prompt:
        # Admin rejimi
        if prompt == "admin_on":
            st.success("Admin mode active.")
            st.rerun()

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # AI javobi (Robot rasmi yo'q, toza matn)
        with st.chat_message("assistant", avatar=None):
            response = f"Men sizning '{prompt}' haqidagi so'rovingizni tahlil qilyapman. Men sizga Gemini kabi aqlli javob berishga tayyorman."
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
