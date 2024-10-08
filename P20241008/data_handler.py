import os
import uuid
import shutil
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for, jsonify
import io
# Set folder untuk menyimpan job
JOB_FOLDER = os.path.join(os.getcwd(), 'jobs')

# Pastikan folder jobs ada
if not os.path.exists(JOB_FOLDER):
    os.makedirs(JOB_FOLDER)

def save_uploaded_data(job_id, df):
    """Simpan dataframe ke dalam format CSV di folder job."""
    job_path = os.path.join(JOB_FOLDER, job_id)
    file_path = os.path.join(job_path, 'data.csv')
    df.to_csv(file_path, index=False)

def get_uploaded_data(job_id):
    """Ambil data yang telah di-upload dalam format DataFrame."""
    job_path = os.path.join(JOB_FOLDER, job_id)
    file_path = os.path.join(job_path, 'data.csv')
    
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None

def get_dataframe(job_id):
    """Helper function to load a dataframe for a given job."""
    job_path = os.path.join(JOB_FOLDER, job_id)
    file_path = os.path.join(job_path, 'data.csv')
    
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None

def dataframe_info(df):
    """Helper function to get dataframe info as string."""
    buffer = io.StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()

def dataframe_head(df, n=10):
    """Return head of dataframe in dictionary format."""
    return df.head(n).to_dict()

def dataframe_describe(df):
    """Return describe of dataframe in dictionary format."""
    return df.describe().to_dict()

def dataframe_duplicates(df):
    """Check if there are duplicate rows in dataframe."""
    return int(df.duplicated().sum())

# Route untuk upload file
def upload_file(job_id):
    job_path = os.path.join(JOB_FOLDER, job_id)
    
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and file.filename.endswith('.csv'):
        # Baca data dan simpan ke CSV
        df = pd.read_csv(file)
        save_uploaded_data(job_id, df)
        return redirect(url_for('preview_data_endpoint', job_id=job_id))

# Route untuk preview data
def preview_data(job_id):
    job_path = os.path.join(JOB_FOLDER, job_id)
    file_path = os.path.join(job_path, 'data.csv')

    if not os.path.exists(file_path):
        return jsonify({'message': 'CSV file not found'}), 404

    # Load data menggunakan pandas
    df = pd.read_csv(file_path)

    # Preview data (menampilkan 5 baris pertama)
    preview = df.head().to_html()

    return render_template('preview.html', preview=preview)

# API untuk mengakses data yang di-upload
def get_data(job_id):
    df = get_uploaded_data(job_id)

    if df is None:
        return jsonify({'message': 'No data found for this job.'}), 404

    return df.to_json(orient='records')

# API untuk data preview
def data_preview(job_id):
    df = get_dataframe(job_id)

    if df is None:
        return jsonify({'message': 'CSV file not found'}), 404

    # Get the parameter from the query string
    param = request.args.get('parameter')

    # Depending on the parameter, return the corresponding data
    if param == 'head':
        return jsonify({'head': dataframe_head(df)})
    elif param == 'info':
        return jsonify({'info': dataframe_info(df)})
    elif param == 'describe':
        return jsonify({'describe': dataframe_describe(df)})
    elif param == 'duplicates':
        return jsonify({'duplicates': dataframe_duplicates(df)})
    else:
        return jsonify({'message': 'Invalid parameter. Valid options are: head, info, describe, duplicates'}), 400
