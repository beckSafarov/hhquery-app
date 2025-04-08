import pandas as pd
import streamlit as st
from utils.plots import plot_vbar,plot_hbar
emp_labels = {'x':'Company Name', 'y':"Vacancies"}

def display_employers_tab(employer_df,salary_df):
  st.header("Employers")
  st.subheader("Top Employers with vacancies")

  emp_vacs = plot_vbar(employer_df, 'Top Employers with vacancies', emp_labels,group_by='employer_name',id='id')
  st.plotly_chart(emp_vacs)
  
  st.subheader("Employers by average salary")
  merged = salary_df.merge(employer_df,how='inner',left_on='employer_id',right_on='id')

  emp_sals = plot_hbar(merged,'employer_name','average','Highest Paying Employers',emp_labels,top_count=10,aggregation_method='mean',)
  
  st.plotly_chart(emp_sals)


"""
 job_id,employer_id,employer_name,salary_id,salary_avg
"""