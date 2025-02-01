import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd



def plot_pie(df, title):
  fig, ax = plt.subplots(figsize=(8, 8))

  work_schedule_dist = df.value_counts()
  ax.pie(
      work_schedule_dist,
      autopct='%1.1f%%',
      startangle=90,
      colors=['#FF9999', '#66B3FF', '#99FF99'],
      labels=work_schedule_dist.index
  )

  plt.title(title)
  st.pyplot(fig)



def plot_vbar(df, group_by='name', id='id'):
  top_actors_count = 10
  actor_counts = df.groupby(group_by)[id].count().sort_values(ascending=False)

  top_actors = actor_counts.head(top_actors_count)

  fig = px.bar(top_actors, x=top_actors.index, y=top_actors.values)

  st.plotly_chart(fig, use_container_width=True)


def plot_hbar(df, group_by, id,title,labels):
  top_actors_count = 10
  actor_counts = df.groupby(group_by)[id].count().sort_values(ascending=False)

  top_actors = actor_counts.head(top_actors_count).sort_values()

  fig = px.bar(
      x=top_actors,
      y=[title[:40] + '...' if len(title) > 40 else title for title in top_actors.index],
      orientation='h',
      title=title,
      labels=labels
  )

  st.plotly_chart(fig, use_container_width=True)
