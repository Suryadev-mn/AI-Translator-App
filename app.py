import streamlit as st
from gtts import gTTS
import os
from translator import translate_text
from languages import LANGUAGES

# ----------------------------
# Page Configuration
# ----------------------------

st.set_page_config(
    page_title="LinguaAI",
    page_icon="🌍",
    layout="wide"
)
# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.title("🌍 LinguaAI")

st.sidebar.markdown("""
### Features
- 🌐 Auto Language Detection
- 🔄 Translate Between Languages
- 📥 Download Translation
- 📜 Translation History
- 🔊 Text-to-Speech

---
AI-Powered Language Translation Platform
""")
# ----------------------------
# Session State
# ----------------------------

if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------------
# Custom CSS
# ----------------------------

st.markdown("""
<style>

.stApp{
    background:#0E1117;
    color:white;
}

h1{
    text-align:center;
    color:#4CAF50;
}

div.stButton > button{
    width:100%;
    height:55px;
    border-radius:12px;
    background:#4CAF50;
    color:black;
    font-size:18px;
    font-weight:bold;
    border:none;
}

div.stButton > button:hover{
    background:#45a049;
}

textarea{
    font-size:17px !important;
}

hr{
    border:1px solid #333;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------

st.title("🌍 LinguaAI")

st.markdown(
    "<p style='text-align:center;'>Translate text between multiple languages instantly.</p>",
    unsafe_allow_html=True
)

st.markdown("---")

# ----------------------------
# Text Input
# ----------------------------

text = st.text_area(
    "Enter Text",
    height=220,
    placeholder="Type or paste your text here..."
)

# ----------------------------
# Language Selection
# ----------------------------

col1, col2 = st.columns(2)

with col1:
    source_language = st.selectbox(
        "Source Language",
        list(LANGUAGES.keys())
    )

with col2:
    target_language = st.selectbox(
        "Target Language",
        list(LANGUAGES.keys()),
        index=1
    )

    if st.button("🔄 Swap Languages"):

        source_language, target_language = (
            target_language,
            source_language
    )

st.markdown("---")

# ----------------------------
# Translate
# ----------------------------

if st.button("🚀 Translate"):

    with st.spinner("Translating..."):

        translated_text, error = translate_text(
            text,
            LANGUAGES[source_language],
            LANGUAGES[target_language]
        )
    if error:
        st.error(error)

    else:

        st.session_state.history.append({
            "Source": source_language,
            "Target": target_language,
            "Original": text,
            "Translated": translated_text
        })

        st.success("Translation Completed Successfully!")

        st.text_area(
            "Translated Text",
            translated_text,
            height=220
        )
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Input Characters",
                len(text)
            )

        with col2:
            st.metric(
                "Output Characters",
                len(translated_text)
            )

        tts = gTTS(text=translated_text, lang=LANGUAGES[target_language])

        tts.save("translation.mp3")

        audio_file = open("translation.mp3", "rb")

        st.audio(audio_file.read())

        st.download_button(
            label="📥 Download Translation",
            data=translated_text,
            file_name="translation.txt",
            mime="text/plain"
        )

        st.caption(f"Characters: {len(text)}")
        st.markdown("---")
st.subheader("📜 Translation History")

if st.session_state.history:

    for item in reversed(st.session_state.history):

        with st.expander(
            f"{item['Source']} ➜ {item['Target']}"
        ):

            st.write("**Original:**")
            st.write(item["Original"])

            st.write("**Translated:**")
            st.write(item["Translated"])

else:
    st.info("No translations yet.")
    st.markdown("---")

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#6c757d; font-size:14px; padding:10px;">
        <strong>LinguaAI</strong><br>
        AI-Powered Language Translation Platform<br><br>
        © 2026 Suryadev M N. All Rights Reserved.
    </div>
    """,
    unsafe_allow_html=True
)