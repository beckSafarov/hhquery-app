import streamlit as st #type:ignore
from data.index import country_ids,currencies,pro_roles
from utils.get_text import get_translated_text as t
from utils.utils import find_key_by_value
from components.create_settings_menu import create_settings_menu


def country_radios():
  countries = t('countries')
  country_names = list(countries.values())
  
  
  select_country_text =  t('sidebar_filter_labels.select_country')
  selected_country_name = st.sidebar.radio(select_country_text, country_names,index=len(countries)-1)
  selected_country_key = find_key_by_value(countries,selected_country_name)
  
  
  country_id = next((country['id'] for country in country_ids if country['code'] == selected_country_key), None)
  
  if country_id:
    st.session_state.country = {'id': None, 'name': ''}
    st.session_state.country['id'] = country_id
    st.session_state.country['name'] = selected_country_name
  return country_id
  
def role_radios():
  roles = t('roles')
  role_labels = list(roles.values())
  select_role_text = t('sidebar_filter_labels.select_role')
  selected_label = st.sidebar.radio(select_role_text, role_labels)
  selected_label_key = find_key_by_value(roles,selected_label)
  
  role_id = next((role['id'] for role in pro_roles if role['name'] == selected_label_key), None)
  
  if role_id:
    st.session_state.role = {'id': None, 'label':''}
    st.session_state.role['id'] = role_id
    st.session_state.role['label'] = selected_label
  return selected_label,role_id

def currency_radios():
  st.session_state.selected_currency = 'usd'
  select_currency_text = t('sidebar_filter_labels.select_currency')
  currency_labels = [field['name'].upper() for field in currencies]
  selected_label = st.sidebar.radio(select_currency_text, currency_labels)
  selected_curr_name = next(field['name'] for field in currencies if field['name'].upper() == selected_label)
  if(selected_curr_name):
    st.session_state.selected_currency = selected_curr_name
  return selected_curr_name


def build_sidebar():
  """sidebar in the side, mostly for filtering

  Returns:
      country_id: id of the selected country
  """
  

  title = t('sidebar_filter_labels.title')
  st.sidebar.title(title)
  country_id = country_radios()
  selected_label, role_id = role_radios()
  selected_currency = currency_radios()
  create_settings_menu()
  return country_id,selected_label,role_id,selected_currency