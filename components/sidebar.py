import streamlit as st #type:ignore
from data.index import pro_roles_full
from components.get_currency import currency_checkboxes

def build_sidebar():
  # Create the sidebar navigation
  st.sidebar.title("IT Roles")

  # Define your IT roles
  role_labels = list(map(lambda item: item['label'], pro_roles_full))

  # Create radio buttons in the sidebar
  selected_label = st.sidebar.radio("Select a role:", role_labels)
  role_id = next((role['id'] for role in pro_roles_full if role['label'] == selected_label), None)
  
  selected_currency = currency_checkboxes()
  
  return selected_label,role_id,selected_currency