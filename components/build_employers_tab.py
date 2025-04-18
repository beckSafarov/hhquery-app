import streamlit as st #type:ignore
from utils.plots import plot_vbar, plot_hbar
from utils.get_translated_text import get_translated_text as t
from utils.get_salaries_converted import get_salaries_converted

def display_top_employers_with_vacancies(employer_df):
    if len(employer_df) < 1:
        return st.write(t("error_messages.emps_vacs"))
    elif len(employer_df) == 1:
        return st.dataframe(
            employer_df[["employer_name"]], use_container_width=True, hide_index=False
        )
    caption = t("chart_captions.top_employers_vacancies")
    labels = {
        "employer_name": t("chart_labels.emps_most_vacancies.employer_name"),
        "y": t("chart_labels.emps_most_vacancies.y"),
    }
    plot_vbar(
        employer_df, caption, labels, group_by="employer_name", id="id"
    )


def display_top_employers_by_avg_salary(employer_df, salary_df, currency):
    if len(salary_df) < 1 or len(employer_df) < 1:
        return
    merged = salary_df.merge(
        employer_df, how="inner", left_on="employer_id", right_on="id"
    )
    caption = t("chart_captions.top_paying_employers")
    labels = {
        "x": f'{t("chart_labels.emps_top_avg_salary.x")} ({currency.upper()})',
        "y": f'{t("chart_labels.emps_top_avg_salary.y")} ',
    }
    plot_hbar(
        merged,
        "employer_name",
        "average",
        caption,
        labels,
        top_count=10,
        aggregation_method="mean",
    )


def build_employers_tab():
    employer_df = st.session_state.employer_df
    salary_df_raw = st.session_state.salary_df
    currency = "usd"
    if "currency" in st.session_state:
        currency = st.session_state.currency
    salary_df = get_salaries_converted(salary_df_raw, currency)
    display_top_employers_with_vacancies(employer_df)
    display_top_employers_by_avg_salary(employer_df, salary_df, currency)
