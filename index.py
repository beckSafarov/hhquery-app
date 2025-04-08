import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.api_methods import get_all_vacancies
from configs import general_page_configs as gpc
from components.display_jobs_tab import display_jobs_tab
from components.display_employers_tab import display_employers_tab
from components.basic_stats import display_main_stats
from components.get_field_id import get_field_id
from components.get_currency import get_currency,handle_currency
from utils.get_vacancy_tables import get_vacancy_tables
from utils.currency_exchange import convert_usd_to_uzs

st.set_page_config(
    layout= gpc['layout'],  # Makes the container wider
    page_title=gpc['page_title'],  # Optional: Sets the browser tab title
    page_icon=gpc['page_icon'],  # Optional: Sets the browser tab icon
    initial_sidebar_state=gpc['initial_sidebar_state']  # Optional: Controls initial sidebar state
)

st.title("HH Query -- Some Stats about job openings")



selected_field_id = get_field_id()

selected_currency = get_currency()

jobs = get_all_vacancies(selected_field_id)
    
jobs_df, salary_df, employer_df = get_vacancy_tables(jobs).values()


#Main Stats
display_main_stats(salary_df,jobs_df)

tab1, tab2 = st.tabs(["Jobs", "Employers"])


with tab1:
    display_jobs_tab(jobs_df, salary_df)
with tab2:
    display_employers_tab(employer_df, salary_df)