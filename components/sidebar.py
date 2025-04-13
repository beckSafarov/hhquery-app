import streamlit as st #type:ignore
from data.index import pro_roles_full,countries,currencies


def country_radios():
  country_names = list(map(lambda item: item['name'], countries))
  selected_country_name = st.sidebar.radio("Select a country:", country_names,index=len(countries)-1)
  country_id = next((country['id'] for country in countries if country['name'] == selected_country_name), None)
  if country_id:
    st.session_state.country = {'id': None, 'name': ''}
    st.session_state.country['id'] = country_id
    st.session_state.country['name'] = selected_country_name
  return country_id
  
def role_radios():
  role_labels = list(map(lambda item: item['label'], pro_roles_full))
  selected_label = st.sidebar.radio("Select a role:", role_labels)
  role_id = next((role['id'] for role in pro_roles_full if role['label'] == selected_label), None)
  if role_id:
    st.session_state.role = {'id': None, 'label':''}
    st.session_state.role['id'] = role_id
    st.session_state.role['label'] = selected_label
  return selected_label,role_id

def currency_radios():
  st.session_state.selected_currency = 'usd'
  currency_labels = [field['name'].upper() for field in currencies]
  selected_label = st.sidebar.radio("Select the currency:", currency_labels)
  selected_curr_name = next(field['name'] for field in currencies if field['name'].upper() == selected_label)
  if(selected_curr_name):
    st.session_state.selected_currency = selected_curr_name
  return selected_curr_name


def build_sidebar():
  """sidebar in the side, mostly for filtering

  Returns:
      country_id: id of the selected country
  """  
  st.sidebar.title("🛠️ Filters")
  country_id = country_radios()
  selected_label, role_id = role_radios()
  selected_currency = currency_radios()
  return country_id,selected_label,role_id,selected_currency