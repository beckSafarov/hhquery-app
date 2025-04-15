import streamlit as st #type:ignore
import pandas as pd #type:ignore
from utils.plots import plot_pie,plot_hbar
import numpy as np #type:ignore
from st_aggrid import AgGrid, GridOptionsBuilder #type:ignore
from utils.get_text import get_translated_text as t


def get_title_and_salaries_df(df,salary_df):
  merged = pd.merge(df, salary_df, left_on='id',right_on='job_id',how='left')
  merged = merged.fillna(0)[['id','name','from','to']]
  merged['from'] = merged['from'].astype('float')
  merged['to'] = merged['to'].astype('float')
  return merged

def get_sum_salaries_per_title(merged_df):
  sum_salaries = merged_df.groupby('name')[['from', 'to']].sum()
  return sum_salaries.replace(0.00,'-')

def build_advanced_grid_table(df):
  gb_advanced = GridOptionsBuilder.from_dataframe(df)
  gb_advanced.configure_column("name", filter="agTextColumnFilter")
  gb_advanced.configure_column(
    "from", 
    filter="agNumberColumnFilter",
    type=["numericColumn"],  # Ensures numeric behavior
    valueFormatter="data.from === null || isNaN(data.from) ? 'N/A' : data.from"  # Custom display for NaN
  )
  gb_advanced.configure_column(
    "to", 
    filter="agNumberColumnFilter",
    type=["numericColumn"],
    valueFormatter="data.to === null || isNaN(data.to) ? 'N/A' : data.to"
  )
  gb_advanced.configure_column("count", filter="agNumberColumnFilter",type=["numericColumn"])
  gb_advanced.configure_grid_options(enable_quick_filter=True)
  gb_advanced.configure_selection('multiple', use_checkbox=False, groupSelectsChildren=True)
  gridOptions_advanced = gb_advanced.build()
  AgGrid(
    df,
    gridOptions=gridOptions_advanced,
    data_return_mode='AS_INPUT',
    update_mode='MODEL_CHANGED',
    fit_columns_on_grid_load=True,
    allow_unsafe_jscode=True,  # Set it to True to allow jsfunction to be injected
    enable_enterprise_modules=False,
    #height=350,
    #width='100%',
    reload_data=True
  )


def display_vacs_by_title_section(df,salary_df):
    col1, col2 = st.columns(2)
    if len(df) < 1:
        return st.write(t("error_messages.vacs_title"))
    with col1:
        role_counts = df["name"].value_counts().reset_index()
        role_counts.index = role_counts.index + 1
        role_counts_df = pd.DataFrame(role_counts)
        if len(salary_df) < 1:
            st.dataframe(role_counts, use_container_width=True, hide_index=False)
        else:
            merged_df = get_title_and_salaries_df(df,salary_df)
            sum_salaries = get_sum_salaries_per_title(merged_df)
            merged_role_counts = pd.merge(role_counts_df,sum_salaries,on='name',how='left')
            build_advanced_grid_table(merged_role_counts)

    with col2:
        caption = t('chart_captions.top_titles_by_vacancies')
        top_titles_by_vacs_labels = t('chart_labels.top_titles')
        pos_plot=plot_hbar(df,'name','name',caption,top_titles_by_vacs_labels)
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
  salary_df = st.session_state.salary_df
  display_vacs_by_title_section(jobs_df,salary_df)
  display_work_reqs_section(jobs_df)
  display_work_formats_section(jobs_df)
