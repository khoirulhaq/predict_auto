from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
import uuid
import shutil
from data_handler import save_uploaded_data, get_uploaded_data, upload_file, preview_data, data_preview
from data_manipulator import manipulate_data
import pandas as pd
app = Flask(__name__)

# Set folder untuk menyimpan job
JOB_FOLDER = os.path.join(os.getcwd(), 'jobs')

# Pastikan folder jobs ada
if not os.path.exists(JOB_FOLDER):
    os.makedirs(JOB_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/job_list', methods=['GET'])
def job_list():
    jobs = [job for job in os.listdir(JOB_FOLDER) if os.path.isdir(os.path.join(JOB_FOLDER, job))]
    return render_template('job_list.html', jobs=jobs)

# API untuk membuat job baru
@app.route('/create_job', methods=['POST'])
def create_job():
    job_name = request.form.get('job_name')
    job_id = str(uuid.uuid4())
    
    # Buat folder untuk job berdasarkan job_id
    job_path = os.path.join(JOB_FOLDER, job_id)
    os.makedirs(job_path)
    
    # Simpan informasi job
    with open(os.path.join(job_path, 'info.txt'), 'w') as f:
        f.write(f'Job Name: {job_name}\nJob ID: {job_id}\n')
    
    return jsonify({'message': 'Job created successfully', 'job_id': job_id})

# API untuk menghapus job berdasarkan job_id
@app.route('/delete_job/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    job_path = os.path.join(JOB_FOLDER, job_id)

    if not os.path.exists(job_path):
        return jsonify({'message': 'Job not found'}), 404

    # Hapus folder job beserta isinya
    shutil.rmtree(job_path)

    return jsonify({'message': 'Job deleted successfully', 'job_id': job_id})

@app.route('/job/<job_id>', methods=['GET', 'POST'])
def job_page(job_id):
    job_path = os.path.join(JOB_FOLDER, job_id)
    
    if not os.path.exists(job_path):
        return jsonify({'message': 'Job not found'}), 404
    
    if request.method == 'POST':
        # Upload file CSV
        return upload_file(job_id)
    
    return render_template('upload.html', job_id=job_id)

# Preview data setelah upload
@app.route('/job/<job_id>/preview', methods=['GET'])
def preview_data_endpoint(job_id):
    return preview_data(job_id)

# API untuk mengakses data yang di-upload
@app.route('/job/<job_id>/data', methods=['GET'])
def get_data_endpoint(job_id):
    df = get_uploaded_data(job_id)  # Ambil DataFrame dari job_id
    if df is None:
        return jsonify({'message': 'No data found for this job.'}), 404

    # Konversi DataFrame menjadi dictionary dan kembalikan sebagai JSON
    return jsonify(df.to_dict(orient='records'))

# API untuk data preview
@app.route('/job/<job_id>/data_preview', methods=['GET'])
def data_preview_endpoint(job_id):
    return data_preview(job_id)

#========== Data Manipulate ====================

@app.route('/job/<job_id>/manipulate', methods=['POST'])
def manipulate_data_endpoint(job_id):
    data = request.json
    
    # Get parameters for handling missing values and duplicates
    handle_null = data.get('handle_null', 'mean')  # Default to 'mean'
    handle_duplicate = data.get('handle_duplicate', 'first')  # Default to 'first'
    
    # Perform data manipulation
    df, error = manipulate_data(job_id, handle_null_method=handle_null, handle_duplicate_method=handle_duplicate)
    
    if error:
        return jsonify({'error': error}), 404

    # Return the manipulated data as JSON
    return jsonify(df.to_dict(orient='records'))

# New endpoint to get the manipulated data
@app.route('/job/<job_id>/manipulate-result', methods=['GET'])
def get_manipulate_result(job_id):
    """Return the manipulated data from the stored CSV."""
    manipulated_file_path = os.path.join(JOB_FOLDER, job_id, 'manipulated_data.csv')
    
    if not os.path.exists(manipulated_file_path):
        return jsonify({'message': 'No manipulated data found for this job.'}), 404
    
    # Load the manipulated data from the CSV
    df = pd.read_csv(manipulated_file_path)
    
    # Return the manipulated data as JSON
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
