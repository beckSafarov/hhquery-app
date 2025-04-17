import plotly.express as px #type:ignore
import streamlit as st  # type:ignore
from st_aggrid import AgGrid, GridOptionsBuilder  # type:ignore
from utils.utils import truncate as trunc

def plot_pie(df, title, labels_map=None):
    # Create pie chart using plotly express
    value_counts = df.value_counts()

    names = value_counts.index.to_series().map(labels_map) if labels_map is not None else value_counts.index
    fig = px.pie(
        values=value_counts.values,
        names=names,
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
        title_x=0 # Center the title
    )

    # Optional: Customize colors if needed
    fig.update_traces(
        marker=dict(colors=['#FF9999', '#66B3FF', '#99FF99']),
        textposition='inside',
        textinfo='percent+label'
    )
    st.plotly_chart(fig)


def plot_stacked_vbar(
    df,
    group_by: str,
    value_vars: list,
    value_translated_vars: dict,
    labels: dict,
    title: str = "Top IT Job Titles by Salary Range",
    var_name: str = "Salary Range",
    top_sort_column: str = "to",
):
    import pandas as pd  # type:ignore

    # Step 1: Sort by highest 'to' salary and select top N (e.g., top 10)
    top_roles = df.sort_values(by=top_sort_column, ascending=False).head(10)
    coordinates = list(labels.keys())

    # Step 2: Melt the dataframe to long format for stacked bar
    df_melted = top_roles.melt(
        id_vars=group_by,
        value_vars=value_vars,
        var_name=var_name,
        value_name=coordinates[1],
    )

    # Step 3: Truncate long job titles
    df_melted[group_by] = df_melted[group_by].apply(lambda word: trunc(word))

    # Step 4: Map 'from' and 'to' to foreign equivalents
    df_melted[var_name] = df_melted[var_name].map(value_translated_vars)

    # Step 5: Sort names for better visual order (by 'to' salary)
    df_melted[group_by] = pd.Categorical(
        df_melted[group_by], categories=top_roles[group_by].tolist(), ordered=True
    )

    # Step 6: Plot

    fig = px.bar(
        df_melted,
        x=coordinates[0],
        y=coordinates[1],
        color=var_name,
        barmode="stack",
        title=title,
        labels=labels,
        height=500,
    )

    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)


def plot_vbar(df, title,labels, group_by, id):
    top_actors_count = 10
    actor_counts = df.groupby(group_by)[id].count().sort_values(ascending=False)

    top_actors = actor_counts.head(top_actors_count)
    fig = px.bar(
        top_actors, x=top_actors.index, y=top_actors.values, title=title, labels=labels
    )

    st.plotly_chart(fig)


def plot_hbar(df, group_by, id,title,labels,top_count=8,aggregation_method='count'):
    actor_counts = getattr(df.groupby(group_by)[id], aggregation_method)().sort_values(
        ascending=False
    )

    top_actors = actor_counts.head(top_count).sort_values()

    fig = px.bar(
        x=top_actors,
        y=[
            title[:40] + "..." if len(title) > 40 else title
            for title in top_actors.index
        ],
        orientation="h",
        title=title,
        labels=labels,
    )

    st.plotly_chart(fig)


def build_advanced_grid_table(df):
    gb_advanced = GridOptionsBuilder.from_dataframe(df)
    gb_advanced.configure_column("name", filter="agTextColumnFilter")
    gb_advanced.configure_column(
        "from",
        filter="agNumberColumnFilter",
        type=["numericColumn"],  # Ensures numeric behavior
        valueFormatter="data.from === null || isNaN(data.from) ? 'N/A' : data.from",  # Custom display for NaN
    )
    gb_advanced.configure_column(
        "to",
        filter="agNumberColumnFilter",
        type=["numericColumn"],
        valueFormatter="data.to === null || isNaN(data.to) ? 'N/A' : data.to",
    )
    gb_advanced.configure_column(
        "count", filter="agNumberColumnFilter", type=["numericColumn"]
    )
    gb_advanced.configure_grid_options(enable_quick_filter=True)
    gb_advanced.configure_selection(
        "multiple", use_checkbox=False, groupSelectsChildren=True
    )
    gridOptions_advanced = gb_advanced.build()
    AgGrid(
        df,
        gridOptions=gridOptions_advanced,
        data_return_mode="AS_INPUT",
        update_mode="MODEL_CHANGED",
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,  # Set it to True to allow jsfunction to be injected
        enable_enterprise_modules=False,
        # height=350,
        # width='100%',
        reload_data=True,
    )
