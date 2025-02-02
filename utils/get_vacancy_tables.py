import pandas as pd

def get_vacancy_tables(jobs):
    # Step 1: Create the main table
    jobs_df = []
    salary_df = []
    employer_df = []

    # Step 2: Iterate through each row
    for idx, row in enumerate(jobs, start=1):
        # Main table
        jobs_df.append({
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
    jobs_df = pd.DataFrame(jobs_df)
    salary_df = pd.DataFrame(salary_df)
    employer_df = pd.DataFrame(employer_df)

    return {"main":jobs_df, "salary":salary_df, "employer":employer_df}