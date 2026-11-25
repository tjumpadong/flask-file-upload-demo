import os
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

BASE_DIR = Path(__file__).resolve().parent


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        UPLOAD_FOLDER=os.environ.get('UPLOAD_FOLDER', str(BASE_DIR / 'uploads')),
    )
    if config:
        app.config.update(config)
    CORS(app)
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

    @app.route('/')
    def index():
        return 'Hello, World!'

    @app.route('/demo', methods=['POST'])
    def upload_file():
        upload = request.files.get('file')
        if upload is None or not upload.filename:
            return jsonify({'error': "missing file field 'file'"}), 400

        filename = secure_filename(upload.filename)
        if not filename:
            return jsonify({'error': 'invalid filename'}), 400

        upload.save(Path(app.config['UPLOAD_FOLDER']) / filename)
        return jsonify({'result': 'hello'}), 201

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
