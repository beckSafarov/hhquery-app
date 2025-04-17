import streamlit as st #type:ignore
import pandas as pd #type:ignore
from utils.plots import (
    plot_pie,
    plot_hbar,
    plot_stacked_vbar,
)
from utils.get_text import get_translated_text as t
from utils.get_salaries_converted import get_salaries_converted

def get_title_and_salaries_df(df,salary_df):
  merged = pd.merge(df, salary_df, left_on='id',right_on='job_id',how='left')
  merged = merged.fillna(0)[['id','name','from','to']]
  merged['from'] = merged['from'].astype('float')
  merged['to'] = merged['to'].astype('float')
  return merged

def get_sum_salaries_per_title(merged_df):
    sum_salaries = merged_df.groupby("name")[["from", "to"]].sum()
    return sum_salaries.replace(0.00, "-")


def get_roles_by_salaries_df(jobs_df, salary_df, role_counts_df):
    merged_df = get_title_and_salaries_df(jobs_df, salary_df)
    sum_salaries = get_sum_salaries_per_title(merged_df)
    merged_roles_df = pd.merge(role_counts_df, sum_salaries, on="name", how="left")
    return merged_roles_df[
        (merged_roles_df["from"] != "-") & (merged_roles_df["to"] != "-")
    ]


def display_vacs_by_title_section(df, salary_df, currency):
    """display vacancies by job title and top salaries

    Args:
        df (dataframe): jobs dataframe, containing job titles
        salary_df (dataframe): salaries dataframe containing 'from' and 'to' columns for salary range

    Returns:
        void: visualizations
    """

    if len(df) < 1:
        return st.write(t("error_messages.vacs_title"))

    role_counts = df["name"].value_counts().reset_index()
    role_counts.index = role_counts.index + 1
    role_counts_df = pd.DataFrame(role_counts)

    if len(df) < 1 or len(salary_df) < 1:
        st.dataframe(
            df[
                [
                    "name",
                    "area",
                    "url",
                    "internship",
                    "schedule",
                    "employment_form",
                    "working_hours",
                    "experience_id",
                ]
            ],
            use_container_width=True,
            hide_index=False,
        )
        return

    col1, col2 = st.columns(2)
    with col1:
        merged_role_counts = get_roles_by_salaries_df(df, salary_df, role_counts_df)
        caption = t("chart_captions.top_titles_by_salary")
        labels = {
            "name": t("chart_labels.top_titles_by_salary.name"),
            "salary": f'{t("chart_labels.top_titles_by_salary.salary")} ({currency.upper()})',
        }
        legend_title = t("chart_legends.top_titles_by_salary.title")
        range_columns = ["from", "to"]
        range_columns_translated = t("chart_legends.top_titles_by_salary.labels")
        plot_top_sals = plot_stacked_vbar(
            merged_role_counts,
            "name",
            range_columns,
            range_columns_translated,
            labels,
            caption,
            legend_title,
        )
        st.plotly_chart(plot_top_sals)
    with col2:
        caption = t("chart_captions.top_titles_by_number")
        labels = t("chart_labels.top_titles_by_number")
        pos_plot = plot_hbar(df, "name", "name", caption, labels)
        st.plotly_chart(pos_plot)


def display_work_reqs_section(df):
    col1, col2 = st.columns(2)
    if len(df) < 1:
        return st.write(t("error_messages.job_requirements"))
    with col1:
        internship_labels_map = {
            True: t("chart_labels.internship.true"),
            False: t("chart_labels.internship.false"),
        }
        captions = t("chart_captions.company_internships")
        intern_plot = plot_pie(df["internship"], captions, internship_labels_map)
        st.plotly_chart(intern_plot)
    with col2:
        experience_labels_map = t("chart_labels.experience")
        captions = t("chart_captions.experience_requirements")
        exp_plot = plot_pie(df["experience_id"], captions, experience_labels_map)
        st.plotly_chart(exp_plot)


# @st.cache_data(ttl=3600)
def build_work_pie(df, prop: str):
  df_selected = df[prop]
  labels_map = t(f'chart_labels.{prop}')
  captions = t(f'chart_captions.{prop}')
  plot = plot_pie(df_selected, captions,labels_map)
  st.plotly_chart(plot)


def display_work_formats_section(df):
    col1, col2 = st.columns(2)
    if len(df) < 1:
        return st.write(t("error_messages.work_formats"))
    with col1:
        build_work_pie(df, "work_formats")
    with col2:
        build_work_pie(df, "working_hours")


def display_jobs_tab():
    jobs_df = st.session_state.jobs_df
    salary_df_raw = st.session_state.salary_df
    currency = "usd"
    if "currency" in st.session_state:
        currency = st.session_state.currency
    salary_df = get_salaries_converted(salary_df_raw, currency)
    display_vacs_by_title_section(jobs_df, salary_df, currency)
    if len(jobs_df) > 1 or len(salary_df) >= 1:
        display_work_reqs_section(jobs_df)
        display_work_formats_section(jobs_df)
