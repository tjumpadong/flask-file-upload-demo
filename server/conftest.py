import pytest

from app import create_app


@pytest.fixture
def upload_dir(tmp_path):
    return tmp_path / 'uploads'


@pytest.fixture
def client(upload_dir):
    app = create_app({'TESTING': True, 'UPLOAD_FOLDER': str(upload_dir)})
    return app.test_client()
