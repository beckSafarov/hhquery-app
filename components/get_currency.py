import streamlit as st
from data import currencies

def currency_checkboxes():
  st.session_state.selected_currency = 'usd'
  currency_labels = [field['label'] for field in currencies]
  selected_label = st.sidebar.radio("Select the currency:", currency_labels)
  selected_curr_name = next(field['name'] for field in currencies if field['label'] == selected_label)
  if(selected_curr_name):
    st.session_state.selected_currency = selected_curr_name
  return selected_curr_name
