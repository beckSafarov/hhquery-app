import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import pandas as pd


def plot_intern_dist(df):
  fig, ax = plt.subplots(figsize=(5, 5))

  # Create the pie chart
  internship_distribution = df.value_counts()
  ax.pie(
      internship_distribution,
      autopct='%1.1f%%',
      startangle=90,
      colors=['#FF9999', '#66B3FF', '#99FF99'],
      labels=internship_distribution.index
  )

  # Add title
  plt.title('Proportions of Internships')

  # Display the plot in Streamlit
  st.pyplot(fig)

def plot_employers_dist(df):
  top_employers_to_pick = 8
  # First get the employer counts sorted by number of vacancies
  employer_counts = df.groupby('name')['id'].count().sort_values(ascending=False)

  # Take top 15 employers
  top_employers = employer_counts.head(top_employers_to_pick)

  # Sum up the rest as "Others"
  others = pd.Series({'Others': employer_counts[top_employers_to_pick:].sum()})

  # Combine top employers with Others
  final_distribution = pd.concat([top_employers, others])

  # Create an interactive pie chart with Plotly
  fig = px.pie(
      values=final_distribution.values,
      names=final_distribution.index,
      title='Distribution of Vacancies by Employer',
  )

  # Update layout for better readability
  fig.update_traces(textposition='inside', textinfo='percent+label')
  fig.update_layout(
      showlegend=True,
      legend=dict(
          yanchor="top",
          y=0.99,
          xanchor="left",
          x=1.05
      )
  )

  # Display in Streamlit
  st.plotly_chart(fig, use_container_width=True)