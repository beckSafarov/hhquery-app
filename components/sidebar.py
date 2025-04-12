import streamlit as st #type:ignore
from data.index import pro_roles_full,countries
from components.get_currency import currency_checkboxes

def build_sidebar():
  # Create the sidebar navigation
  st.sidebar.title("🛠️ Filters")
  
  # Select country
  country_labels = list(map(lambda item: item['name'], countries))

  # Create radio buttons in the sidebar
  selected_country_label = st.sidebar.radio("Select a country:", country_labels)
  country_id = next((country['id'] for country in countries if country['name'] == selected_country_label), None)
  
  

  # Define your IT roles
  role_labels = list(map(lambda item: item['label'], pro_roles_full))

  # Create radio buttons in the sidebar
  selected_label = st.sidebar.radio("Select a role:", role_labels,index=len(countries)-1)
  role_id = next((role['id'] for role in pro_roles_full if role['label'] == selected_label), None)
  
  selected_currency = currency_checkboxes()
  
  return country_id,selected_label,role_id,selected_currency