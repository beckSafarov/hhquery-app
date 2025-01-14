import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from methods import getAllJobs, getJobsPerPage, getVacancyTables
from basic_stats import display_main_stats
from analysis import plot_intern_dist,plot_employers_dist
from configs import pro_roles_full

st.title("HH Query -- Some Stats about job openings")

it_field_labels = []
for field in pro_roles_full:
  it_field_labels.append(field['label'])

selected_label = st.selectbox("Select field to see stats for", it_field_labels) 

for field in pro_roles_full:
  if field['label'] == selected_label:
    selected_field_id = field['id']




with st.spinner('Loading jobs'):
  jobs = getAllJobs(selected_field_id)



vacancyTables = getVacancyTables(jobs)
main_df = vacancyTables['main']
salary_df = vacancyTables['salary']
employer_df = vacancyTables['employer']

# Sample data
display_main_stats(salary_df,main_df)


st.subheader("Main Info on Vacancies")
st.write(main_df)
st.subheader("Salary Stats of Vacancies")
st.write(salary_df)
st.subheader("Employer Info on Vacancies")
st.write(employer_df)

# Analysis
st.subheader("Top Employers with vacancies")
st.write(plot_employers_dist(employer_df))


st.subheader("Companies providing Internship")
plot_intern_dist(main_df['internship'])

# [X] internship opportunities 
# [-] work schedule distribution
# [-] work format distribution
# [-] work title distribution 
# [-] experience distribution 
# [-] employers with the most vacancies 
# [-] individual job

#most required skills among all the vacancies 

# employer_values = employer_df.value_counts(normalize=True)
# st.write(employer_values)