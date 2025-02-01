import pandas as pd
import requests 
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import streamlit as st
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

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


def get_vacancies_by_page(session, page=1, role_id=10):
    url = f'https://api.hh.ru/vacancies?area=97&professional_role={role_id}'
    url = url if page <= 1 else url + f'&page={page}'
    try:
        # Add timeout parameter (10 seconds)
        response = session.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        return response.json()
    
    except requests.exceptions.Timeout:
        st.error(f"Request timeout for page {page}. The server took too long to respond.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching page {page}: {str(e)}")
        return None

@st.cache_data(ttl=3600) 
def get_all_vacancies(role_id):
    # Create a session for all requests
    session = create_session()
    
    # Create a progress bar
    progress_text = "Fetching jobs..."
    progress_bar = st.progress(0)

    print(progress_text)
    
    # Get first page and initialize variables
    json_data = get_vacancies_by_page(session, 1, role_id)
    if not json_data:
        st.write("Failed to fetch initial data")
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
                st.warning(f"Failed to fetch page {i + 1}")
            
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