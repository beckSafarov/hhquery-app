import streamlit as st  # type: ignore
from configs import general_page_configs as gpc

st.set_page_config(
    layout=gpc["layout"],  # Makes the container wider
    page_title=gpc["page_title"],  # Optional: Sets the browser tab title
    page_icon=gpc["page_icon"],  # Optional: Sets the browser tab icon
    initial_sidebar_state=gpc[
        "initial_sidebar_state"
    ],  # Optional: Controls initial sidebar state
)

from components.build_jobs_tab import build_jobs_tab
from components.build_employers_tab import build_employers_tab
from components.build_basic_stats import build_basic_stats
from components.build_sidebar import build_sidebar
from components.build_filter_badges import build_filter_budges
from utils.get_vacancy_tables import get_vacancy_tables
from utils.api_methods import get_all_vacancies
from utils.get_translated_text import get_translated_text as t

lang = "en"

page_text = {
    "title": t("page_title"),
    "jobs": t("tabs.jobs"),
    "employers": t("tabs.employers"),
}

default_country = {"id": 97, "code": "UZ"}
default_role = {"id": 156, "name": "bi-analyst"}

st.title(page_text["title"])


def main():
    # sidebar and values selected from sidebar filters
    build_sidebar()
    country_id = default_country["id"]
    role_id = default_role["id"]
    if "country" in st.session_state and "role" in st.session_state:
        country_id = st.session_state.country["id"]
        role_id = st.session_state.role["id"]

    jobs = get_all_vacancies(country_id, role_id)

    build_filter_budges()

    get_vacancy_tables(jobs)

    # Main Stats in big letters, such as average maximum and minimum salary, number of vacancies
    build_basic_stats()

    tab1, tab2 = st.tabs([page_text["jobs"], page_text["employers"]])

    with tab1:
        build_jobs_tab()
    with tab2:
        build_employers_tab()


main()
