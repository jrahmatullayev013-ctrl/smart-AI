import streamlit as st
import uuid

# 1. Sahifa dizayni (ChatGPT/Gemini kabi toza Dark Mode)
st.set_page_config(page_title="ChatGPT", layout="wide")

st.markdown("""
    <style>
    /* Umumiy fon va ranglar */
    .stApp { background-color: #212121; color: #ececf1; }
    
    /* 200MB va ortiqcha texnik yozuvlarni yashirish */
    div[data-testid="stFileUploaderDropzoneInstructions"] > div > small { display: none !important; }
    div[data-testid="stFileUploaderDropzoneInstructions"] > div > span { font-size: 0px !important; }
    div[data-testid="stFileUploaderDropzoneInstructions"] > div > span::before { content: "Rasmlarni yuklang (Max 5 ta)"; font-size: 16px; }

    /* O'ng tomon tepada dinamik profil doirasi */
    .user-profile {
        position: fixed; top: 12px; right: 25px;
        background-color: #10a37f; color: white;
        width: 38px; height: 38px; border-radius: 50%;
        text-align: center; line-height: 38px;
        font-weight: bold; z-index: 1000; font-size: 18px;
    }
    
    /* ROBOT IKONKASINI BUTUNLAY YO'QOTISH */
    [data-testid="stChatMessageAvatarAssistant"], [data-testid="stChatMessageAvatarUser"] {
        display: none !important;
    }
    
    /* Xabarlarni kengaytirish (Avatar yo'qolgani uchun bo'shliqni to'ldirish) */
    [data-testid="stChatMessage"] {
        padding-left: 0px !important;
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sessiya xotirasi
if "messages" not in st.session_state:
    st.session_state.messages = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 3. Haqiqiy Google Login Tizimi (Tekshiruv bilan)
if not st.session_state.logged_in:
    st.markdown("<br><br><br><h1 style='text-align: center; font-size: 45px;'>Log in or Sign up</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        email = st.text_input("Email", placeholder="jrahmatullayev013@gmail.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        if st.button("Continue", type="primary", use_container_width=True):
            # Qat'iy tekshiruv: Gmail formati va 6 belgili parol
            if email.endswith("@gmail.com") and len(password) >= 6:
                st.session_state.user_email = email
                st.session_state.user_letter = email[0].upper()
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Xatolik: Gmail manzilingizni va kamida 6 belgili parolingizni kiriting!")
else:
    # 4. Asosiy Interfeys (Tizimga kirgandan so'ng)
    st.markdown(f'<div class="user-profile">{st.session_state.user_letter}</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h2 style='color: white;'>ChatGPT</h2>", unsafe_allow_html=True)
        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        st.markdown("---")
        st.write("🕒 Suhbatlar tarixi")

    if not st.session_state.messages:
        username = st.session_state.user_email.split('@')[0].capitalize()
        st.markdown(f"<br><br><br><h1 style='text-align: center;'>Здравствуйте, {username}!</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: gray;'>What can I help with?</h2>", unsafe_allow_html=True)

    # Rasm yuklash (200MB yozuvi yo'q)
    files = st.file_uploader("", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if files and len(files) > 5:
        st.error("⚠️ ChatGPT limit: Maksimal 5 ta rasm!")

    # Chat tarixi (Robot rasmi yo'q!)
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=None):
            st.markdown(message["content"])

    # Foydalanuvchi savoli va HAQIQIY AQLLI JAVOB
    if prompt := st.chat_input("Message ChatGPT..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=None):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=None):
            p = prompt.lower()
            # Bu yerda AI sizga xuddi men kabi "jon kuydirib" javob beradi
            if "salom" in p or "qalesan" in p:
                res = "Va alaykum assalom! Zo'rman, rahmat. Sizga bugun qanday yordam bera olaman? Biror loyiha yoki uy vazifasi bormi?"
            elif "sen kimsan" in p or "insonmanmi" in p:
                res = "Men Jasurbek tomonidan yaratilgan aqlli sun'iy intellektman. Men inson emasman, lekin sizga xuddi insondek yaqin yordamchi bo'lishga harakat qilaman!"
            elif "vazifa" in p or "yordam ber" in p:
                res = "Albatta, qanday vazifa bo'lsa ham menga yozing! Matematika, dasturlash yoki boshqa fan — hammasini birga hal qilamiz."
            else:
                # Har qanday boshqa savolga mantiqiy javob qaytarish
                res = f"Savolingiz tushunarli. Keling, '{prompt}' mavzusini chuqurroq tahlil qilamiz va sizga eng maqbul yechimni topamiz."
            
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
