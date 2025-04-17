import streamlit as st #type:ignore
from utils.currency_exchange import exchange_currencies

@st.cache_data(ttl=3600)
def get_salaries_converted(df, currency:str='usd'):
    if len(df) < 1:
        return df

    df_copy = df.copy()
    # where stated currency not equal to current currency, convert
    mask = df_copy["currency"] != currency.upper()
    for index, row in df_copy[mask].iterrows():
        row_curr = row["currency"]

        df_copy.loc[index, "from"] = exchange_currencies(
            row["from"], row_curr, currency, 0
        )
        df_copy.loc[index, "to"] = exchange_currencies(row["to"], row_curr, currency, 0)
        df_copy.loc[index, "average"] = exchange_currencies(
            row["average"], row_curr, currency, 0
        )
        df_copy.loc[index, "currency"] = currency.upper()
    return df_copy
