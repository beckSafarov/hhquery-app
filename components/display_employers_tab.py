import streamlit as st #type:ignore
from utils.plots import plot_vbar,plot_hbar
from data.plot_labels import emps_avg_salary,emps_most_vacancy
from utils.get_text import get_translated_text as t


def display_top_employers_with_vacancies(employer_df):
  if len(employer_df) < 1:
    return st.write('No Stats found for top employers by vacancies')
  caption = t('chart_captions.top_employers_vacancies')
  print(f'caption top emps with vacs: {caption}')
  emp_vacs = plot_vbar(employer_df, caption, emps_most_vacancy,group_by='employer_name',id='id')
  st.plotly_chart(emp_vacs)

def display_top_employers_by_avg_salary(employer_df,salary_df):
  if len(salary_df) < 1 or len(employer_df) < 1:
    return st.write('No Stats found for top employers by average salaries')
  merged = salary_df.merge(employer_df,how='inner',left_on='employer_id',right_on='id')
  caption = t('chart_captions.top_paying_employers')
  print(f'caption top paying employers: {caption}')
  emp_sals = plot_hbar(merged,'employer_name','average',caption,emps_avg_salary,top_count=10,aggregation_method='mean',)
  st.plotly_chart(emp_sals)

def display_employers_tab():
  employer_df = st.session_state.employer_df
  salary_df = st.session_state.salary_df
  display_top_employers_with_vacancies(employer_df)
  display_top_employers_by_avg_salary(employer_df,salary_df)