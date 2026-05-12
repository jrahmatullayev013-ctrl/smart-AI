import streamlit as st
import uuid
import json
import os

# 1. Ma'lumotlar bazasi (Streamlit-da fayl saqlash)
DB_FILE = 'ai_database.json'

def yuklash():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return {"users": {}}

def saqlash(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f, indent=4)

# Sahifa sozlamalari (Dizayn Gemini uslubida)
st.set_page_config(page_title="Jasurbek AI", page_icon="╰(*°*)╯")

if 'data' not in st.session_state:
    st.session_state.data = yuklash()

# 2. Interfeys (Minimalistik va professional)
st.markdown("<h1 style='text-align: center; color: #1a73e8;'>╰(*°Jasurbek AI°*)╯</h1>", unsafe_allow_html=True)

if 'user_name' not in st.session_state:
    st.write("Xush kelibsiz! Qanday kirishni xohlaysiz?")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Google orqali kirish", type="primary", use_container_width=True):
            st.session_state.user_name = f"Google_User_{str(uuid.uuid4())[:4]}"
            st.rerun()
            
    with col2:
        if st.button("Mehmon (Guest)", use_container_width=True):
            st.session_state.user_name = f"Guest_{str(uuid.uuid4())[:4]}"
            st.rerun()
else:
    # Foydalanuvchi ma'lumotlarini bazaga qo'shish
    u_name = st.session_state.user_name
    if u_name not in st.session_state.data['users']:
        yangi_id = f"ID-{str(uuid.uuid4())[:6].upper()}"
        st.session_state.data['users'][u_name] = {"id": yangi_id, "premium": False}
        saqlash(st.session_state.data)

    user_info = st.session_state.data['users'][u_name]
    
    # Yon panel (Sidebar)
    with st.sidebar:
        st.write(f"👤 **Foydalanuvchi:** {u_name}")
        st.write(f"🔑 **ID (Pasport):** {user_info['id']}")
        status = "🌟 Premium" if user_info['premium'] else "🆓 Oddiy"
        st.write(f"📊 **Status:** {status}")
        if not user_info['premium']:
            st.info("Premium versiya: $15/oy")

    # Chat interfeysi
    chat_input = st.chat_input("Xabaringizni yozing...")
    
    if chat_input:
        # Yashirin Admin kodi
        if chat_input == "admin_on":
            st.session_state.data['users'][u_name]['premium'] = True
            saqlash(st.session_state.data)
            st.success("✅ ADMIN: Premium muvaffaqiyatli yoqildi!")
            st.rerun()
        
        with st.chat_message("user"):
            st.write(chat_input)
        
        with st.chat_message("assistant"):
            if user_info['premium']:
                st.write(f"🌟 Salom {u_name}! Men sizning Premium yordamchingizman. Qanday yordam bera olaman?")
            else:
                st.write(f"👋 Salom! Siz oddiy versiyadan foydalanyapsiz. To'liq imkoniyatlar uchun Premiumga o'ting.")
