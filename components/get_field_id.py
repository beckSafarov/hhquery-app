import streamlit as st
from configs import pro_roles_full

def get_field_id():
  it_field_labels = [field['label'] for field in pro_roles_full]

  selected_label = st.selectbox("Select field to see stats for", it_field_labels) 

  selected_field_id = next(field['id'] for field in pro_roles_full if field['label'] == selected_label)

  return selected_field_id
