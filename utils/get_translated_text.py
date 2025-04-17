# In your Python code
import json
import streamlit as st #type:ignore

# @st.cache_resource
def load_translations():
    with open("./data/translations.json", "r", encoding="utf-8") as f:
        return json.load(f)

translations = load_translations()

def get_text(path: str, lang: str = "en") -> str:
    keys = path.split(".")
    result = translations.get(lang, {})

    for key in keys:
        if isinstance(result, dict) and key in result:
            result = result[key]
        else:
            return path  # fallback: return key path if translation not found

    return result

def get_translated_text(keyword):
    if "language" in st.session_state:
        return get_text(keyword, st.session_state.language)
    return get_text(keyword)
