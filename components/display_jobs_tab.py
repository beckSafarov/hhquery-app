import streamlit as st
from plots import plot_pie,plot_hbar


def display_vacs_by_title_section(df):
  col1, col2 = st.columns(2)

  with col1:
    st.subheader("Vacancies List")
    role_counts = df['name'].value_counts().reset_index()
    role_counts.index = role_counts.index + 1
    st.dataframe(role_counts,  use_container_width=True,
      hide_index=False)
  with col2:
    st.subheader("Positions with most vacancies")
    plot_hbar(df,'name','name','Top Job Titles by Number of Vacancies',{'x':'Number of vacancies','y':'Job Title'})


def display_work_reqs_section(df):
  col1, col2 = st.columns(2)
  with col1:
    st.subheader("Companies providing Internship")
    intern_plot = plot_pie(df['internship'], 'Proportions of Internships')
    st.plotly_chart(intern_plot)
  with col2:
    st.subheader("Experience requirements among companies")
    exp_plot = plot_pie(df['experience_id'], 'Distribution of experience')
    st.plotly_chart(exp_plot)

def display_work_formats_section(df):
  col1, col2 = st.columns(2)
  with col1:
    st.subheader("Work Formats per companies")
    work_formats = plot_pie(df['work_format'], 'Distribution of work format')
    st.plotly_chart(work_formats)
  with col2:
    st.subheader("Work Hours for companies")
    print(df.columns)
    work_hours = plot_pie(df['working_hours'], 'Distribution of working hours among companies')
    st.plotly_chart(work_hours)

def display_jobs_tab(jobs_df, salary_df):
  
  display_vacs_by_title_section(jobs_df)
  
  st.header("Jobs")

  display_work_reqs_section(jobs_df)
  display_work_formats_section(jobs_df)
  # st.subheader("Companies providing Internship")
  # plot_pie(jobs_df['internship'], 'Proportions of Internships')
  
  
  # st.subheader("Experience requirements among companies")
  # plot_pie(jobs_df['experience_id'], 'Distribution of experience')