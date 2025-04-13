import streamlit as st #type:ignore
from datetime import datetime
import currencyapicom #type:ignore
from configs import CACHE_DURATION,CURRENCY_API_CLIENT_ID
client = currencyapicom.Client(CURRENCY_API_CLIENT_ID)

@st.cache_data(ttl=CACHE_DURATION)
def fetch_exchange_rate():
    """Fetch the latest passed currency to USD exchange rate"""
    try:
        exchanges = client.latest()
        return exchanges['data'], datetime.now()
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None,None

# Get the cached exchange rate
exchanges, last_updated = fetch_exchange_rate()

def convert_around_usd(amount, currency, direction='to'):
   """convert to usd from currency or to currency from usd

    Args:
        amount (int): amount of money to convert
        currency (string): currency to convert to USD or from USD
        direction (str, optional): values: 'to' and 'from. Defaults to 'to'.

    Returns:
        int: converted value
    """  
   value_to_usd = exchanges[currency.upper()]['value']
   total = amount / value_to_usd if direction == 'to' else amount * value_to_usd
   return round(total,2)


def exchange_currencies(amount, from_curr, to_curr):
  from_curr_usd_value = convert_around_usd(amount, from_curr, 'to')
  to_curr_usd_equivalent = convert_around_usd(from_curr_usd_value, to_curr, 'from')
  return round(to_curr_usd_equivalent, 2)
