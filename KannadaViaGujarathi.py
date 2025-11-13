import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from aksharamukha.transliterate import process as aksharamukha_process
from gtts import gTTS
from io import BytesIO
import pandas as pd

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(
    page_title="Gujarati → Kannada Learning",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------ HIDE STREAMLIT UI ------------------ #
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ------------------ AUDIO GENERATOR ------------------ #
def make_audio(text, lang="kn"):
    fp = BytesIO()
    tts = gTTS(text=text, lang=lang)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()

# ------------------ PAGE TITLE ------------------ #
st.title("📝 Learn Kannada using Gujarati Script")
st.subheader("ગુજરાતી ના અક્ષરો થી કન્નડ શીખો")

text = st.text_area("Enter Gujarati text here:", height=120)

if st.button("Translate"):
    if text.strip():
        try:
            # FULL SENTENCE PROCESSING -----------------------------

            # Gujarati → Kannada sentence
            kannada = GoogleTranslator(source="gu", target="kn").translate(text)

            # Kannada → Gujarati script
            kannada_in_gujarati = aksharamukha_process("Kannada", "Gujarati", kannada)

            # Kannada → English phonetics
            kannada_english = transliterate(kannada, sanscript.KANNADA, sanscript.ITRANS)

            # Kannada audio (sentence)
            audio_sentence = make_audio(kannada)

            # ---------------- OUTPUT ---------------- #
            st.markdown("## 🔹 Translation Results")

            st.markdown(f"**Gujarati Input:**  \n:blue[{text}]")
            st.markdown(f"**Kannada Translation:**  \n:green[{kannada}]")
            st.markdown(f"**Kannada in Gujarati Script:**  \n:orange[{kannada_in_gujarati}]")
            st.markdown(f"**English Phonetics:**  \n`{kannada_english}`")

            st.markdown("### 🔊 Kannada Audio (Sentence)")
            st.audio(audio_sentence, format="audio/mp3")
            st.download_button("Download Sentence Audio", audio_sentence, "sentence.mp3")

            # WORD-BY-WORD FLASHCARDS -------------------------------

            st.markdown("---")
            st.markdown("## 🃏 Flashcards (Word-by-Word)")

            guj_words = text.split()
            kan_words = kannada.split()

            # Prevent mismatch
            limit = min(len(guj_words), len(kan_words))

            for i in range(limit):
                gw = guj_words[i]
                kw = kan_words[i]

                # Kannada → Gujarati script (word)
                kw_gu = aksharamukha_process("Kannada", "Gujarati", kw)

                # Phonetic (word)
                kw_ph = transliterate(kw, sanscript.KANNADA, sanscript.ITRANS)

                # Audio (word)
                kw_audio = make_audio(kw)

                with st.expander(f"Word {i+1}: {gw}", expanded=False):
                    st.write("**Gujarati word:**", gw)
                    st.write("**Kannada word:**", kw)
                    st.write("**Kannada in Gujarati script:**", kw_gu)
                    st.write("**Phonetics:**", kw_ph)

                    st.audio(kw_audio, format="audio/mp3")
                    st.download_button(
                        f"Download Audio (Word {i+1})",
                        kw_audio,
                        f"word_{i+1}.mp3"
                    )

        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.warning("Please enter Gujarati text.")
