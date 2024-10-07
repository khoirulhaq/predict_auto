from flask import Blueprint, jsonify, request
import requests
import pandas as pd

preprocess_bp = Blueprint('preprocess', __name__)

@preprocess_bp.route('/', methods=['GET'])
def preprocess_data():
    """
    Endpoint untuk memproses data.
    """
    # Mengambil data dari endpoint load_data
    load_data_url = 'http://localhost:5000/load_data'  # Ganti dengan URL endpoint load_data
    response = requests.get(load_data_url)

    if response.status_code != 200:
        return jsonify({'message': 'Failed to load data'}), 400

    raw_data = pd.DataFrame(response.json()['data'])

    # Lakukan preprocessing di sini (misalnya, menghapus duplikat)
    processed_data = raw_data.drop_duplicates()

    return jsonify({'processed_data': processed_data.to_dict(orient='records')})
