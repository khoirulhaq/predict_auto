from flask import Flask
from eda.load_data import load_data_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(load_data_bp, url_prefix='/load_data')

if __name__ == '__main__':
    app.run(debug=True)
