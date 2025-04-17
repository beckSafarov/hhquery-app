import streamlit as st  # type:ignore
from data.data import currencies
from utils.currency_exchange import exchange_currencies
from utils.get_translated_text import get_translated_text as t
import math


def get_avg_in_currency(df, def_currency):
    total_from = 0
    total_to = 0
    list_len = len(df)
    for _, row in df.iterrows():
        currency = row["currency"].lower()
        curr_from = row["from"] if math.isnan(row["from"]) == False else 0
        curr_to = row["to"]
        if def_currency == currency:
            total_from += curr_from
            total_to += curr_to
        else:
            total_from += exchange_currencies(curr_from, currency, def_currency)
            total_to += exchange_currencies(
                curr_to, currency, st.session_state.selected_currency
            )

    avg_from = round(total_from / list_len, 2)
    avg_to = round(total_to / list_len, 2)
    return avg_from, avg_to


def format_large_number(number):
    if len(str(number)) < 1:
        return number
    return f"{number:,}"


def calculate(salary_df, jobs_df):
    salary_df_sals = salary_df[salary_df.notna()]
    overall_vacancies = len(jobs_df)

    if len(salary_df_sals) == 0:
        return {
            "average_from": "Unknown",
            "average_to": "Unknown",
            "overall_vacancies": overall_vacancies,
        }

    average_from, average_to = get_avg_in_currency(
        salary_df, st.session_state.selected_currency
    )

    return {
        "average_from": average_to,
        "average_to": average_from,
        "overall_vacancies": overall_vacancies,
    }


def plot(cards):
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    default_currency = st.session_state.selected_currency
    currency_symbol = next(
        (curr["symbol"] for curr in currencies if curr["name"] == default_currency)
    )

    # Style and display stats
    for i, col in enumerate(cols):
        bare_value = cards[i]["value"]
        value = (
            format_large_number(bare_value) if bare_value != "Unknown" else bare_value
        )
        label = cards[i]["label"]["text"]
        show_symbol = cards[i]["label"]["show_symbol"]
        preceding_text = currency_symbol if show_symbol and value != "Unknown" else ""
        font_size = 40 if len(str(value)) < 10 else 30

        with col:
            st.markdown(
                f"""
      <div style="text-align: center;">
          <h1 style="color: #4CAF50; font-size: {font_size}px;">{preceding_text} {value}</h1>
          <h3>{label}</h3>
      </div>
      """,
                unsafe_allow_html=True,
            )


def build_basic_stats():
    salary_df = st.session_state.salary_df
    jobs_df = st.session_state.jobs_df
    calculated_values = calculate(salary_df, jobs_df)

    plot(
        [
            {
                "label": {"text": t("basic_stats.avg_min_salary"), "show_symbol": True},
                "value": calculated_values["average_to"],
            },
            {
                "label": {"text": t("basic_stats.avg_max_salary"), "show_symbol": True},
                "value": calculated_values["average_from"],
            },
            {
                "label": {
                    "text": t("basic_stats.overall_vacancies"),
                    "show_symbol": False,
                },
                "value": calculated_values["overall_vacancies"],
            },
        ]
    )
