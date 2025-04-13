import streamlit as st #type:ignore
from utils.plots import plot_vbar,plot_hbar
from data.plot_labels import emps_avg_salary,emps_most_vacancy

def display_top_employers_with_vacancies(employer_df):
  st.subheader("Top Employers with vacancies")
  if len(employer_df) < 1:
    return st.write('No Stats found for top employers by vacancies')
  emp_vacs = plot_vbar(employer_df, 'Top Employers with vacancies', emps_most_vacancy,group_by='employer_name',id='id')
  st.plotly_chart(emp_vacs)

def display_top_employers_by_avg_salary(employer_df,salary_df):
  st.subheader("Employers by average salary")
  if len(salary_df) < 1 or len(employer_df) < 1:
    return st.write('No Stats found for top employers by average salaries')
  merged = salary_df.merge(employer_df,how='inner',left_on='employer_id',right_on='id')
  emp_sals = plot_hbar(merged,'employer_name','average','Highest Paying Employers',emps_avg_salary,top_count=10,aggregation_method='mean',)
  st.plotly_chart(emp_sals)

def display_employers_tab():
  employer_df = st.session_state.employer_df
  salary_df = st.session_state.salary_df
  st.header("Employers")
  display_top_employers_with_vacancies(employer_df)
  display_top_employers_by_avg_salary(employer_df,salary_df)