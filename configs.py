from dotenv import load_dotenv  # type:ignore
import os
load_dotenv()

API = 'https://api.hh.ru/vacancies'
CACHE_DURATION = 86400
CURRENCY_API_CLIENT_ID = os.getenv("CURRENCY_API_CLIENT_ID")

general_page_configs = {
    "layout": "wide",
    "page_title": "IT Job Trends",
    "page_icon": "📊",
    "initial_sidebar_state": "expanded",
}
