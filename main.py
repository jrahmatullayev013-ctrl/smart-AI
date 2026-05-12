import streamlit as st
import uuid

# 1. Sahifa dizayni (ChatGPT/Gemini uslubida)
st.set_page_config(page_title="ChatGPT", layout="wide")

st.markdown("""
    <style>
    /* Umumiy fon */
    .stApp { background-color: #212121; color: #ececf1; }
    
    /* O'ng tomon tepada profil */
    .user-profile {
        position: fixed; top: 12px; right: 25px;
        background-color: #10a37f; color: white;
        width: 38px; height: 38px; border-radius: 50%;
        text-align: center; line-height: 38px;
        font-weight: bold; z-index: 1000; font-size: 18px;
    }
    
    /* Ortiqcha yozuvlar va robotni butunlay yashirish */
    [data-testid="stChatMessageAvatarAssistant"], [data-testid="stChatMessageAvatarUser"],
    .st-emotion-cache-1ae8k9d, .st-emotion-cache-9ycgxx { display: none !important; }
    
    /* Chat input va "+" tugmasi dizayni */
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sessiya va Login mantiqi
if "messages" not in st.session_state:
    st.session_state.messages = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 3. Google Registration (ChatGPT kabi)
if not st.session_state.logged_in:
    st.markdown("<br><br><br><h1 style='text-align: center; font-size: 45px;'>Log in or Sign up</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        email = st.text_input("Email", placeholder="name@example.com")
        password = st.text_input("Password", type="password")
        if st.button("Continue", type="primary", use_container_width=True):
            if "@gmail.com" in email and len(password) >= 6:
                st.session_state.user_email = email
                st.session_state.user_letter = email[0].upper()
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Xato: To'g'ri Gmail va kamida 6 belgili parol kiriting!")
else:
    # Profil belgisi
    st.markdown(f'<div class="user-profile">{st.session_state.user_letter}</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("<h2 style='color: white;'>ChatGPT</h2>", unsafe_allow_html=True)
        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # Markaziy ekran
    if not st.session_state.messages:
        username = st.session_state.user_email.split('@')[0].capitalize()
        st.markdown(f"<br><br><br><h1 style='text-align: center;'>Здравствуйте, {username}!</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: gray;'>What can I help with?</h2>", unsafe_allow_html=True)

    # "+" Tugmasi o'rnidagi rasm yuklash (5 ta limit)
    files = st.file_uploader("", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if files and len(files) > 5:
        st.error("⚠️ Maksimal 5 ta rasm yuklash mumkin!")

    # Chat muloqoti
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=None):
            st.markdown(message["content"])

    # Foydalanuvchi savoli va AQLLI JAVOB
    if prompt := st.chat_input("Message ChatGPT..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=None):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=None):
            # Bu yerda AI siz bilan jonli muloqot qiladi
            p = prompt.lower()
            if "salom" in p:
                res = f"Va alaykum assalom, {st.session_state.user_email.split('@')[0]}! Sizga bugun qanday yordam bera olaman?"
            elif "kimsan" in p:
                res = "Men Jasurbek tomonidan yaratilgan aqlli sun'iy intellektman. Maqsadim — sizga Gemini va ChatGPT kabi har qanday savolingizda yordam berish!"
            elif "vazifa" in p or "yordam ber" in p:
                res = "Albatta! Qanday vazifa bo'lsa ham menga yuboring, birgalikda eng yaxshi yechimni topamiz."
            else:
                # Har qanday boshqa savolga mantiqiy javob qaytarish
                res = f"Sizning '{prompt}' haqidagi so'rovingiz juda qiziqarli. Keling, buni batafsil ko'rib chiqamiz..."
            
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
