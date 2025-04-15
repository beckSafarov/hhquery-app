import requests  # type: ignore
import time
from requests.adapters import HTTPAdapter # type: ignore
from urllib3.util.retry import Retry # type: ignore
import streamlit as st # type: ignore
import asyncio
import aiohttp # type: ignore
from utils.get_text import get_translated_error as te
from configs import API


def create_session():
    """Create a session with retry strategy"""
    session = requests.Session()
    
    # Configure retry strategy
    retries = Retry(
        total=5,  # number of retries
        backoff_factor=1,  # wait 1, 2, 4, 8, 16 seconds between retries
        status_forcelist=[500, 502, 503, 504],  # retry on these status codes
    )
    
    # Add timeout to all requests
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    return session


def get_vacancies_by_page(session, page=1, role_id=10,country_id=97):
    url = f'{API}?area={country_id}&professional_role={role_id}'
    url = url if page <= 1 else url + f'&page={page}'
    try:
        # Add timeout parameter (10 seconds)
        response = session.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        return response.json()

    except requests.exceptions.Timeout:
        st.error(te("request_timeout", page))
        return None
    except requests.exceptions.RequestException as e:
        st.error(te("error_fetching", page, str(e)))
        return None

@st.cache_data(ttl=3600) 
def get_all_vacancies(country,role):
    # Create a session for all requests
    session = create_session()
    if country and role:
        role_id = role['id']
        country_id = country['id']

    # Create a progress bar
    progress_text = "Fetching jobs..."
    progress_bar = st.progress(0)

    print(progress_text)

    # Get first page and initialize variables
    json_data = get_vacancies_by_page(session, 1, role_id,country_id)
    if not json_data:
        st.error(te("fetch_failure"))
        return []

    pages = json_data['pages']
    overall_jobs = json_data['found']
    jobs = json_data['items']

    print(f"Total jobs found: {overall_jobs}")
    print(f"Total pages to fetch: {pages}")

    # Fetch remaining pages
    if pages > 1:
        for i in range(1, pages):
            # Update progress bar
            progress_bar.progress((i + 1) / pages)

            more_jobs = get_vacancies_by_page(session, i + 1)
            if more_jobs:
                jobs.extend(more_jobs['items'])
            else:
                st.warning(te("fetch_page_number", i + 1))

            # Add a small delay to be nice to the API
            time.sleep(0.2)  # Increased delay slightly

    # Clear the progress bar
    progress_bar.empty()
    return jobs

# New functions for lazy loading vacancy details
async def fetch_vacancy_details(session, url):
    """Fetch details for a single vacancy"""
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                return await response.json()
            return None
    except Exception as e:
        return None

async def fetch_all_vacancy_details(urls, progress_bar=None):
    """Fetch details for all vacancies asynchronously"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(urls):
            tasks.append(fetch_vacancy_details(session, url))
            if progress_bar is not None:
                progress_bar.progress((i + 1) / len(urls))
            # Add small delay to be nice to the API
            await asyncio.sleep(0.1)
        
        return await asyncio.gather(*tasks)
