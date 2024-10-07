from flask import Blueprint, jsonify
import requests

visualize_bp = Blueprint('visualize', __name__)

@visualize_bp.route('/', methods=['GET'])
def visualize_data():
    """
    Endpoint untuk memvisualisasikan data.
    """
    # Mengambil data dari endpoint preprocess
    preprocess_url = 'http://localhost:5000/preprocess'  # Ganti dengan URL endpoint preprocess
    response = requests.get(preprocess_url)

    if response.status_code != 200:
        return jsonify({'message': 'Failed to preprocess data'}), 400

    processed_data = response.json()['processed_data']

    if processed_data is None:
        return jsonify({'message': 'No processed data found. Please preprocess data first.'}), 400

    # Buat visualisasi data (contoh data yang diambil)
    data = {
        'date': [d['date'] for d in processed_data],
        'value': [d['value'] for d in processed_data]
    }

    return jsonify({
        'message': 'Data Visualized Successfully',
        'data_plot': data
    })
