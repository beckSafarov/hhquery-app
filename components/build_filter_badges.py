import streamlit as st #type:ignore
import streamlit_shadcn_ui as ui  # type:ignore
from utils.get_translated_text import get_translated_text as t
from data.data import countries,roles,currencies

def get_country_badge():
    country_key = st.session_state.country["key"]
    country_label = t("countries")[country_key]
    country_flag = next((c['emoji'] for c in countries if c['code'] == country_key))
    return f'{country_flag} {country_label}'

def get_role_badge():
    role_key = st.session_state.role["key"]
    role_label = t("roles")[role_key]
    role_emoji = next((role["emoji"] for role in roles if role["name"] == role_key))
    return f'{role_emoji} {role_label}'

def get_currency_badge():
    currency_key = st.session_state.selected_currency
    currency_symbol = next((curr['symbol'] for curr in currencies if curr['name'] == currency_key))
    return f'{currency_symbol} {currency_key.upper()}'

def build_filter_budges():
    session_state = st.session_state
    country_badge = ''
    role_badge = ''
    currency_badge = 'USD'

    if 'country' in session_state:
        country_badge = get_country_badge()
    
    if 'role' in session_state:
        role_badge = get_role_badge()
    
    if 'selected_currency' in session_state:
        currency_badge = get_currency_badge()

    ui.badges(
        badge_list=[
            (f"{t('badges.country')}: {country_badge}", "default"),
            (f"{t('badges.role')}: {role_badge}", "destructive"),
            (f"{t('badges.currency')}: {currency_badge}", "secondary"),
        ],
        class_name="flex gap-2",
        key="badges1",
    )
