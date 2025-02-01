import streamlit as st
from plots import plot_pie,plot_hbar






def display_jobs_tab(main_df, salary_df):
  
  col1, col2 = st.columns(2)

  st.header("Jobs")
  # plot_vbar(main_df,'name','name')
  with col1:
    st.subheader("Vacancies List")
    role_counts = main_df['name'].value_counts().reset_index()
    role_counts.index = role_counts.index + 1
    st.dataframe(role_counts,  use_container_width=True,
      hide_index=False)
  with col2:
    st.subheader("Positions with most vacancies")
    plot_hbar(main_df,'name','name','Top Job Titles by Number of Vacancies',{'x':'Number of vacancies','y':'Job Title'})
  


  st.subheader("Companies providing Internship")
  plot_pie(main_df['internship'], 'Proportions of Internships')
  
  st.subheader("Work Formats per companies")
  plot_pie(main_df['work_format'], 'Distribution of work format')
  
  st.subheader("Work Hours for companies")
  plot_pie(main_df['working_hours'], 'Distribution of working hours among companies')
  
  st.subheader("Experience requirements among companies")
  plot_pie(main_df['experience_id'], 'Distribution of experience')