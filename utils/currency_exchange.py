import streamlit as st #type:ignore
from datetime import datetime
import currencyapicom #type:ignore
client = currencyapicom.Client('cur_live_8y6M52TI3twEEifAJOpvG5DR3uKfVSanqcfQ8203')
CACHE_DURATION = 86400

@st.cache_data(ttl=CACHE_DURATION)
def fetch_exchange_rate():
    """Fetch the latest UZS to USD exchange rate"""
    try:
        exchanges = client.latest()
        uzs_rate = exchanges['data']['UZS']['value']
        return uzs_rate, datetime.now()
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None,None

# Get the cached exchange rate
rate, last_updated = fetch_exchange_rate()
    
def convert_usd_to_uzs(amount_usd, should_round=True):
    """Convert USD amount to UZS using cached exchange rate"""
    total = amount_usd * rate
    rounded_total = round(total,2)
    return rounded_total if should_round == True else total
  

def convert_uzs_to_usd(amount_uzs, should_round=True):
    """Convert UZS amount to USD using cached exchange rate"""
    total = amount_uzs / rate
    rounded_total = round(total,2)
    return rounded_total if should_round == True else total

def exchange_currencies(amount, from_curr, to_curr):
  if from_curr == 'usd' and to_curr == 'uzs':
    return convert_usd_to_uzs(amount)
  else:
    return convert_uzs_to_usd(amount)
