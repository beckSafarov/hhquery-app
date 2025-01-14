import pandas as pd
import requests 
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import streamlit as st

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


def getJobsPerPage(session, page=1, role_id=10):
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

def getAllJobs(role_id):
    # Create a session for all requests
    session = create_session()
    
    # Create a progress bar
    progress_text = "Fetching jobs..."
    progress_bar = st.progress(0)

    print(progress_text)
    
    # Get first page and initialize variables
    json_data = getJobsPerPage(session, 1, role_id)
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
            
            more_jobs = getJobsPerPage(session, i + 1)
            if more_jobs:
                jobs.extend(more_jobs['items'])
            else:
                st.warning(f"Failed to fetch page {i + 1}")
            
            # Add a small delay to be nice to the API
            time.sleep(0.2)  # Increased delay slightly
    
    # Clear the progress bar
    progress_bar.empty()
    st.success(f"Successfully fetched {len(jobs)} jobs")
    return jobs

def getVacancyTables(jobs):
    # Step 1: Create the main table
    main_df = []
    salary_df = []
    employer_df = []

    # Step 2: Iterate through each row
    for idx, row in enumerate(jobs, start=1):
        # Main table
        main_df.append({
            'id': row['id'],
            'premium': row['premium'],
            'name': row['name'],
            'created_at': row['created_at'],
            'area': row['area']['name'],
            'url': row['url'],
            'internship': row['internship'],
            'schedule': row['schedule']['id'],
            'employment_form': row['employment_form']['id'],
            'working_hours': row['working_hours'][0]['id'],
            # 'work_format': row['work_format'][0]['id'] 
            'work_format': row.get('work_format', [])[0].get('id') if len(row['work_format']) > 0 else None,
            'salary_id':  idx if row['salary'] is not None else 0,       # Foreign key to salary table
            'employer_id': idx,     # Foreign key to employer table
            'experience_id': row['experience']['id']    # Foreign key to experience table
        })
        
        # Salary table
        if row['salary'] is not None:
            salary = row.get('salary', {})
            salary_df.append({
                'salary_id': idx,
                'from': salary.get('from'),
                'to': salary.get('to'),
                'currency': salary.get('currency'),
                'gross': salary.get('gross')
            })
        
        # Employer table
        employer = row.get('employer', {})
        employer_df.append({
            'employer_id': idx,
            'id': employer.get('id'),
            'name': employer.get('name')
        })
        

    # Step 3: Convert to DataFrames
    main_df = pd.DataFrame(main_df)
    salary_df = pd.DataFrame(salary_df)
    employer_df = pd.DataFrame(employer_df)

    return {"main":main_df, "salary":salary_df, "employer":employer_df}