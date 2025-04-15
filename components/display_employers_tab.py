import streamlit as st #type:ignore
from utils.plots import plot_vbar, plot_hbar
from utils.get_text import get_translated_text as t


def display_top_employers_with_vacancies(employer_df):
    if len(employer_df) < 1:
        return st.write(t("error_messages.emps_vacs"))
    caption = t("chart_captions.top_employers_vacancies")
    labels = {
        "employer_name": t("chart_labels.emps_most_vacancies.employer_name"),
        "y": t("chart_labels.emps_most_vacancies.y"),
    }
    emp_vacs = plot_vbar(
        employer_df, caption, labels, group_by="employer_name", id="id"
    )
    st.plotly_chart(emp_vacs)

def display_top_employers_by_avg_salary(employer_df,salary_df):
    if len(salary_df) < 1 or len(employer_df) < 1:
        return st.write(t("error_messages.top_emps_sals"))
    merged = salary_df.merge(
        employer_df, how="inner", left_on="employer_id", right_on="id"
    )
    caption = t("chart_captions.top_paying_employers")
    labels = {
        "x": t("chart_labels.emps_top_avg_salary.x"),
        "y": t("chart_labels.emps_top_avg_salary.y"),
    }
    emp_sals = plot_hbar(
        merged,
        "employer_name",
        "average",
        caption,
        labels,
        top_count=10,
        aggregation_method="mean",
    )
    st.plotly_chart(emp_sals)

def display_employers_tab():
  employer_df = st.session_state.employer_df
  salary_df = st.session_state.salary_df
  display_top_employers_with_vacancies(employer_df)
  display_top_employers_by_avg_salary(employer_df,salary_df)
