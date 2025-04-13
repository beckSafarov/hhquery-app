import streamlit as st #type: ignore
from configs import general_page_configs as gpc

st.set_page_config(
    layout= gpc['layout'],  # Makes the container wider
    page_title=gpc['page_title'],  # Optional: Sets the browser tab title
    page_icon=gpc['page_icon'],  # Optional: Sets the browser tab icon
    initial_sidebar_state=gpc['initial_sidebar_state']  # Optional: Controls initial sidebar state
)

from components.display_jobs_tab import display_jobs_tab
from components.display_employers_tab import display_employers_tab
from components.basic_stats import display_main_stats
from components.sidebar import build_sidebar
from utils.get_vacancy_tables import get_vacancy_tables
from utils.api_methods import get_all_vacancies

st.title("HH Query -- Some Stats about job openings")




def main():
    #sidebar and values selected from sidebar filters
    build_sidebar()
    
    country = st.session_state.country
    role = st.session_state.role
    if country and role:
        selected_country_name = country['name']
        selected_role_label = role['label']
    
    st.header(f"{selected_role_label} jobs in {selected_country_name}")

    jobs = get_all_vacancies(country,role)
        
    get_vacancy_tables(jobs)


    #Main Stats in big letters, such as average maximum and minimum salary, number of vacancies
    display_main_stats()

    tab1, tab2 = st.tabs(["Jobs", "Employers"])


    with tab1:
        display_jobs_tab()
    with tab2:
        display_employers_tab()

main()