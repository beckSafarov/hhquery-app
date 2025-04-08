import pandas as pd

def get_avg_sal(min, max):
    if min is not None and max is not None:
        return (min + max)/2
    elif min is not None or max is not None:
        return min if min is not None else max
    else: 
        return 0
    
def clean_salary_df(df):
    if len(df) < 1:
        return df
    # put 'from' value when 'to' is NaN
    df.loc[(df['to'].isna()) & (~df['from'].isna()), 'to'] = df['from']

    # Drop rows where both 'to' and 'from' are NaN
    df_cleaned = df.drop(df[(df['to'].isna()) & (df['from'].isna())].index)
    return df_cleaned
            

def get_vacancy_tables(jobs):
    # Step 1: Create the main table
    jobs_df = []
    salary_df = []
    employer_df = []

    # Step 2: Iterate through each row
    for row in jobs:
        # Employer table
        employer = row.get('employer', {})
        employer_id = employer.get('id')
        job_id = row['id']
        # Jobs table
        jobs_df.append({
            'id': job_id,
            'premium': row['premium'],
            'name': row['name'],
            'created_at': row['created_at'],
            'area': row['area']['name'],
            'url': row['url'],
            'internship': row['internship'],
            'schedule': row['schedule']['id'],
            'employment_form': row['employment_form']['id'],
            'working_hours': row['working_hours'][0]['id'],
            'work_format': row.get('work_format', [])[0].get('id') if len(row['work_format']) > 0 else None,
            'employer_id': employer_id,     
            'experience_id': row['experience']['id']
        })
        
        # Salary table
        if row['salary'] is not None:
            salary = row.get('salary', {})
            salary_df.append({
                'job_id': job_id,
                'employer_id':employer_id,
                'from': salary.get('from'),
                'to': salary.get('to'),
                'average': get_avg_sal(salary.get('from'),salary.get('to')),
                'currency': salary.get('currency'),
                'gross': salary.get('gross')
            })
        
        # Employer table
        employer_df.append({
            'id': employer_id,
            'employer_name': employer.get('name')
        })
        

    # Step 3: Convert to DataFrames
    jobs_df = pd.DataFrame(jobs_df)
    salary_df = pd.DataFrame(salary_df)
    employer_df = pd.DataFrame(employer_df)

    return {
        "main":jobs_df, 
        "salary":clean_salary_df(salary_df), 
        "employer":employer_df}