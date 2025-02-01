import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def calculate(salary_df, main_df):
  salary_df_sals = salary_df[salary_df.notna()]
  overall_vacancies = len(main_df)
  
  if len(salary_df_sals) == 0: 
    return {
      "average_from":"Unknown",
      "average_to":"Unknown",
      "overall_vacancies":overall_vacancies
    }
  average_to = round(salary_df_sals["to"].mean())
  average_from = round(salary_df_sals["from"].mean())

  return  {
    "average_from":average_to,
    "average_to":average_from,
    "overall_vacancies":overall_vacancies
  }

def plot(cards):
  col1, col2, col3 = st.columns(3)
  cols = [col1, col2, col3]
  # Style and display stats
  for i, col in enumerate(cols):
     with col:
      st.markdown(f"""
      <div style="text-align: center;">
          <h1 style="color: #4CAF50; font-size: 40px;">{cards[i]['value']}</h1>
          <h3>{cards[i]['label']}</h3>
      </div>
      """, unsafe_allow_html=True)

  # with col1:
  #     st.markdown(f"""
  #     <div style="text-align: center;">
  #         <h1 style="color: #4CAF50; font-size: 40px;">{cards[0]['value']}</h1>
  #         <h3>Average Salary</h3>
  #     </div>
  #     """, unsafe_allow_html=True)

  # with col2:
  #     st.markdown(f"""
  #     <div style="text-align: center;">
  #         <h1 style="color: #2196F3; font-size: 40px;">{num_vacancies}</h1>
  #         <h3>Vacancies</h3>
  #     </div>
  #     """, unsafe_allow_html=True)

  # with col3:
  #     st.markdown(f"""
  #     <div style="text-align: center;">
  #         <h1 style="color: #FF5722; font-size: 40px;">{top_skill}</h1>
  #         <h3>Top Skill</h3>
  #     </div>
  #     """, unsafe_allow_html=True)


def display_main_stats(salary_df, main_df):
  calculated_values = calculate(salary_df, main_df)
  plot([
     {"label":"Average Minimum Salary", "value":calculated_values['average_to']},
     {"label":"Average Maximum Salary", "value":calculated_values['average_from']},
     {"label":"Overall Vacancies", "value":calculated_values['overall_vacancies']},
  ])