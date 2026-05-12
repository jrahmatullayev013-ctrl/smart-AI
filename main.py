import streamlit as st
import uuid

# 1. Sahifa dizayni (ChatGPT Dark Mode uslubida)
st.set_page_config(page_title="ChatGPT", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #212121; color: #ececf1; }
    
    /* O'ng tomon tepada dinamik profil doirasi */
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

# 2. Sessiya xotirasini boshqarish
if "messages" not in st.session_state:
    st.session_state.messages = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 3. Kirish va Ro'yxatdan o'tish oynasi (ChatGPT kabi)
if not st.session_state.logged_in:
    st.markdown("<br><br><br><h1 style='text-align: center; font-size: 45px;'>Log in or Sign up</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Smarter responses, 5 image uploads, and more.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        email = st.text_input("Email manzilingiz", placeholder="name@example.com")
        password = st.text_input("Parol", type="password", placeholder="kamida 6 belgili")
        
        if st.button("Continue", type="primary", use_container_width=True):
            if email and len(password) >= 6:
                st.session_state.user_email = email
                st.session_state.user_letter = email[0].upper()
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Iltimos, email va parolni to'g'ri kiriting!")
        
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

    # Markaziy ekran - Boshlang'ich yozuv
    if not st.session_state.messages:
        st.markdown("<br><br><br><h1 style='text-align: center; font-size: 45px;'>What can I help with?</h1>", unsafe_allow_html=True)

    # Rasm yuklash (5 ta qat'iy limit)
    files = st.file_uploader("", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if files and len(files) > 5:
        st.error("⚠️ ChatGPT limit: Faqat 5 tagacha rasm yuklash mumkin!")

    # Chat tarixini chiqarish (Robot rasmi yo'q)
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=None):
            st.markdown(message["content"])

    # Foydalanuvchi kiritish joyi
    if prompt := st.chat_input("Message ChatGPT..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=None):
            st.markdown(prompt)

        # AI javob berish mantiqi (Haqiqiy muloqot)
        with st.chat_message("assistant", avatar=None):
            p = prompt.lower()
            if "salom" in p:
                res = "Va alaykum assalom! Sizga bugun qanday yordam bera olaman?"
            elif "isming nima" in p:
                res = "Mening ismim Jasurbek AI. Sizga yordam berish uchun yaratilganman."
            elif "rahmat" in p:
                res = "Arziydi! Har doim xizmatingizdaman."
            else:
                res = f"Tushunarlik. '{prompt}' bo'yicha savolingizni ko'rib chiqyapman. Men sizga Gemini kabi aqlli javob berishga tayyorman."
            
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
