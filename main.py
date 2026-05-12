import streamlit as st
import uuid
import json
import os

# 1. Ma'lumotlar bazasini yuklash
DB_FILE = 'ai_database.json'
def yuklash():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return {"users": {}}

def saqlash(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f, indent=4)

# Sahifa dizayni (Gemini Dark Mode)
st.set_page_config(page_title="Gemini", layout="wide")

if 'data' not in st.session_state:
    st.session_state.data = yuklash()

# 2. Chap menyu (Sidebar) - Faqat kerakli funksiyalar
with st.sidebar:
    st.markdown("<h2 style='color: #4285F4;'>Gemini</h2>", unsafe_allow_html=True)
    st.button("➕ Yangi suhbat", use_container_width=True)
    st.markdown("---")
    st.write("🕒 Tarix")
    st.caption("Bugungi so'rovlar...")
    st.markdown("---")
    st.write("⚙️ Sozlamalar")
    st.write("❓ Yordam")

# 3. Kirish jarayoni
if 'user_name' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>Sizga qanday yordam bera olaman?</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Google bilan kirish", type="primary", use_container_width=True):
            st.session_state.user_name = f"Google_User_{str(uuid.uuid4())[:4]}"
            st.session_state.is_google = True
            st.rerun()
    with col2:
        if st.button("Mehmon bo'lib davom etish", use_container_width=True):
            st.session_state.user_name = f"Guest_{str(uuid.uuid4())[:4]}"
            st.session_state.is_google = False
            st.rerun()
else:
    u_name = st.session_state.user_name
    if u_name not in st.session_state.data['users']:
        # Faqat Google foydalanuvchilari uchun ID yaratiladi
        user_id = f"ID-{str(uuid.uuid4())[:6].upper()}" if st.session_state.is_google else "No ID"
        st.session_state.data['users'][u_name] = {"id": user_id, "premium": False, "images": 0}
        saqlash(st.session_state.data)

    user_info = st.session_state.data['users'][u_name]

    # 4. Rasm yuklash va chat mantiqi
    st.markdown(f"<h3 style='color: #1a73e8;'>Salom, {u_name}!</h3>", unsafe_allow_html=True)
    
    # Rasm yuklash cheklovi (Max 5 ta)
    uploaded_files = st.file_uploader("Rasm yuklang (Maksimal 5 ta)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
    
    if uploaded_files:
        if len(uploaded_files) > 5:
            st.error("Xato: Faqat 5 tagacha rasm yuklash mumkin!")
        else:
            st.success(f"{len(uploaded_files)} ta rasm qabul qilindi.")

    # Chat
    chat_input = st.chat_input("Bu yerga yozing...")
    
    if chat_input:
        # Yashirin admin funksiyasi
        if chat_input == "admin_on":
            st.session_state.data['users'][u_name]['premium'] = True
            saqlash(st.session_state.data)
            st.success("✅ Premium rejim faollashdi!")
            st.rerun()

        with st.chat_message("user"):
            st.write(chat_input)
        
        with st.chat_message("assistant"):
            st.write("Men sizning so'rovingizni tahlil qilyapman...")
