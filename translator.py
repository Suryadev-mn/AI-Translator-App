from deep_translator import GoogleTranslator
from langdetect import detect


def translate_text(text, source_lang, target_lang):
    """
    Translates text from source_lang to target_lang.
    If source_lang is 'auto', the language is detected automatically.
    """

    try:
        # Check if the input is empty
        if not text.strip():
            return "", "Please enter some text."

        # Detect language automatically if needed
        if source_lang == "auto":
            source_lang = detect(text)

        # Perform translation
        translated = GoogleTranslator(
            source=source_lang,
            target=target_lang
        ).translate(text)

        return translated, None

    except Exception as e:
        return None, str(e)