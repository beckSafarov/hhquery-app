import streamlit as st #type:ignore
from data.index import currencies,languages

def create_settings_menu():
    with st.sidebar.expander("⚙️ Display Settings", expanded=False):
        # Language selection
        language_labels = [lang['label'] for lang in languages]
        
        if "language" not in st.session_state:
            st.session_state.language = "en"
            
        def change_language():
            st.session_state.language = next((lang['id'] for lang in languages if lang['label']== st.session_state.selected_language))
            
        st.selectbox(
            "Language / Язык / Til",
            language_labels,
            index=0,
            on_change=change_language,
            key="selected_language"
        )
        
        # Currency selection
        currencies_list = [curr['name'].upper() for curr in currencies]
        
        option = st.selectbox(
            "Currency",
            currencies_list,
            index=0,
        )
        st.session_state.selected_currency = option.lower()