import pandas as pd
from data_handler import get_uploaded_data, save_uploaded_data
import os

JOB_FOLDER = os.path.join(os.getcwd(), 'jobs')


def handle_missing_values(df, method='mean'):
    """Handle missing values in the dataframe."""
    if method == 'mean':
        return df.fillna(df.mean(numeric_only=True))
    elif method == 'median':
        return df.fillna(df.median(numeric_only=True))
    elif method == 'drop':
        return df.dropna()
    else:
        return df  # Default to no changes

def handle_duplicates(df, method='first'):
    """Handle duplicate rows in the dataframe."""
    if method == 'first':
        return df.drop_duplicates(keep='first')
    elif method == 'last':
        return df.drop_duplicates(keep='last')
    elif method == 'none':
        return df  # Keep all duplicates
    else:
        return df

def manipulate_data(job_id, handle_null_method='mean', handle_duplicate_method='first'):
    """Apply data manipulations to the uploaded dataset and store the result separately."""
    df = get_uploaded_data(job_id)
    
    if df is None:
        return None, 'No data found for this job.'
    
    # Handle missing values
    df = handle_missing_values(df, handle_null_method)
    
    # Handle duplicates
    df = handle_duplicates(df, handle_duplicate_method)
    
    # Save the manipulated data into a separate CSV file
    manipulated_file_path = os.path.join(JOB_FOLDER, job_id, 'manipulated_data.csv')
    df.to_csv(manipulated_file_path, index=False)
    
    return df, None
