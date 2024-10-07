from flask import Blueprint, jsonify, request
import requests
import pandas as pd

preview_bp = Blueprint('preview', __name__)

@preview_bp.route('/data_preview', methods=['GET'])
def data_preview():
    """
    Endpoint untuk melihat preview data dengan info, deskripsi, dan data duplikat.
    Parameter:
        - cek: 'info', 'describe', atau 'duplicate'
    """
    # Mengambil data dari endpoint load_data
    load_data_url = 'http://localhost:5000/load_data'  # Ganti dengan URL endpoint load_data
    response = requests.get(load_data_url)

    if response.status_code != 200:
        return jsonify({'message': 'Failed to load data'}), 400

    raw_data = pd.DataFrame(response.json()['data'])

    # Ambil parameter cek
    cek = request.args.get('cek')

    if cek == 'info':
        data_info = {
            'shape': raw_data.shape,
            'columns': raw_data.columns.tolist(),
            'head': raw_data.head().to_dict(orient='records')
        }
        return jsonify({'data_info': data_info})

    elif cek == 'describe':
        data_description = raw_data.describe(include='all').to_dict()
        return jsonify({'data_description': data_description})

    elif cek == 'duplicate':
        data_duplicates = raw_data[raw_data.duplicated()].to_dict(orient='records')
        return jsonify({'data_duplicates': data_duplicates})

    else:
        return jsonify({'message': 'Invalid parameter. Use "info", "describe", or "duplicate".'}), 400
