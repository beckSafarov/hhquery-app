import streamlit as st #type:ignore
from data.index import currencies,languages
from utils.get_text import get_translated_text as t

def create_settings_menu():
    with st.sidebar.expander(t("display_settings.title"), expanded=False):
        # Language selection
        language_labels = [lang['label'] for lang in languages]

        if "language" not in st.session_state:
            st.session_state.language = "en"
            st.session_state.selected_language = language_labels[0]

        def change_language():
            st.session_state.language = next((lang['id'] for lang in languages if lang['label']== st.session_state.selected_language))

        st.selectbox(
            "Language / Язык",
            language_labels,
            index=0,
            on_change=change_language,
            key="selected_language",
        )

        # Currency selection
        currencies_list = [curr['name'].upper() for curr in currencies]

        option = st.selectbox(
            "Currency",
            currencies_list,
            index=0,
        )
        st.session_state.selected_currency = option.lower()
