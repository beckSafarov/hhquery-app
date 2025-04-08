import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def plot_pie(df, title):
    # Create pie chart using plotly express
    fig = px.pie(
        values=df.value_counts().values,
        names=df.value_counts().index,
        title=title
    )
    
    # Set consistent size and layout for all pie charts
    fig.update_layout(
        width=450,  # Set fixed width
        height=450,  # Set fixed height
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05
        ),
        title_x=0.5  # Center the title
    )
    
    # Optional: Customize colors if needed
    fig.update_traces(
        marker=dict(colors=['#FF9999', '#66B3FF', '#99FF99']),
        textposition='inside',
        textinfo='percent+label'
    )
    
    return fig


def plot_vbar(df, title,labels, group_by, id):
  top_actors_count = 10
  actor_counts = df.groupby(group_by)[id].count().sort_values(ascending=False)

  top_actors = actor_counts.head(top_actors_count)

  fig = px.bar(top_actors, x=top_actors.index, y=top_actors.values, title=title,labels=labels)

  return fig


def plot_hbar(df, group_by, id,title,labels,top_count=8,aggregation_method='count'):
  actor_counts = getattr(df.groupby(group_by)[id], aggregation_method)().sort_values(ascending=False)

  top_actors = actor_counts.head(top_count).sort_values()

  fig = px.bar(
      x=top_actors,
      y=[title[:40] + '...' if len(title) > 40 else title for title in top_actors.index],
      orientation='h',
      title=title,
      labels=labels
  )

  return fig
