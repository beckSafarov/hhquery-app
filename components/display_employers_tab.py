import streamlit as st
from plots import plot_vbar



def display_employers_tab(jobs_df, employer_df):
  st.header("Employers")
  st.subheader("Top Employers with vacancies")
  st.write(plot_vbar(employer_df))