import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from api_methods import get_all_vacancies, get_vacancies_by_page, getVacancyTables
from basic_stats import display_main_stats
from plots import plot_intern_dist,plot_employers_dist
from configs import pro_roles_full
from components.get_field_id import get_field_id

st.title("HH Query -- Some Stats about job openings")

selected_field_id = get_field_id()

with st.spinner('Loading jobs'):
  jobs = get_all_vacancies(selected_field_id)


main_df, salary_df, employer_df = getVacancyTables(jobs).values()

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