from flask import Blueprint, jsonify, render_template
import pandas as pd

load_data_bp = Blueprint('load_data', __name__)

@load_data_bp.route('/', methods=['GET'])
def load_data():
    """
    Endpoint untuk memuat data dari test.csv.
    """
    # Membaca data dari file CSV
    file_path = 'test.csv'
    df = pd.read_csv(file_path)

    # Mengirim data dalam bentuk dictionary
    data_dict = df.to_dict(orient='records')

    return render_template('index.html', data=data_dict, columns=df.columns.tolist())
