from dotenv import load_dotenv #type:ignore
from utils.get_text import get_text
import os
load_dotenv()
import streamlit as st #type: ignore

lang = 'en'

API = 'https://api.hh.ru/vacancies'
CACHE_DURATION = 86400
CURRENCY_API_CLIENT_ID = os.getenv("CURRENCY_API_CLIENT_ID")

general_page_configs = {
  "layout":"wide",
  "page_title":get_text('tab_title'),
  "page_icon":"📊",
  "initial_sidebar_state":"expanded"
}