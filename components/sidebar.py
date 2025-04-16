import streamlit as st  # type:ignore
from data.index import countries as country_ids, currencies, roles as roles_with_ids
from utils.get_text import get_translated_text as t
from utils.utils import find_key_by_value, find_index_by_prop
from components.create_settings_menu import create_settings_menu


def country_radios():
    countries = t("countries")
    country_names = list(countries.values())

    select_country_text = t("sidebar_filter_labels.select_country")
    selected_country_name = st.sidebar.radio(
        select_country_text, country_names, index=len(countries) - 1
    )
    selected_country_key = find_key_by_value(countries, selected_country_name)

    country_id = next(
        (
            country["id"]
            for country in country_ids
            if country["code"] == selected_country_key
        ),
        None,
    )

    if country_id:
        st.session_state.country = {"id": None, "key": ""}
        st.session_state.country["id"] = country_id
        st.session_state.country["key"] = selected_country_key
    return country_id


def role_radios():
    if "role" not in st.session_state:
        st.session_state.role = {"id": None, "key": "", "last_index": 0}

    roles = t("roles")  # get roles data based on the current language
    role_labels = list(roles.values())
    text_select_role = t(
        "sidebar_filter_labels.select_role"
    )  # text that says: "Select role" in different languages
    selected_role_label = st.sidebar.radio(
        text_select_role, role_labels, st.session_state.role["last_index"]
    )
    selected_role_key = find_key_by_value(roles, selected_role_label)

    role_id = next(
        (role["id"] for role in roles_with_ids if role["name"] == selected_role_key),
        None,
    )
    role_index = find_index_by_prop(roles_with_ids, "name", selected_role_key)

    if role_id:
        st.session_state.role["id"] = role_id
        st.session_state.role["key"] = selected_role_key
        st.session_state.role["last_index"] = role_index
    return role_id


def currency_radios():
    if "currency" not in st.session_state:
        st.session_state.selected_currency = "usd"
    select_currency_text = t("sidebar_filter_labels.select_currency")
    currency_labels = [field["name"].upper() for field in currencies]
    selected_label = st.sidebar.radio(select_currency_text, currency_labels)
    selected_curr_name = next(
        field["name"] for field in currencies if field["name"].upper() == selected_label
    )
    if selected_curr_name:
        st.session_state.selected_currency = selected_curr_name
    return selected_curr_name


def build_sidebar():
    """sidebar in the side, mostly for filtering

    Returns:
        country_id: id of the selected country
    """

    create_settings_menu()
    title = t("sidebar_filter_labels.title")
    st.sidebar.title(title)
    country_radios()
    role_radios()
    currency_radios()
