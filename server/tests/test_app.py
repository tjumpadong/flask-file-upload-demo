import io

from app import create_app


def test_index(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.data == b'Hello, World!'


def test_upload_saves_file(client, upload_dir):
    response = client.post(
        '/demo',
        data={'file': (io.BytesIO(b'hello'), 'note.txt')},
        content_type='multipart/form-data',
    )

    assert response.status_code == 201
    assert response.get_json() == {'result': 'hello'}
    assert (upload_dir / 'note.txt').read_bytes() == b'hello'


def test_upload_without_file_returns_400(client):
    response = client.post(
        '/demo', data={}, content_type='multipart/form-data'
    )

    assert response.status_code == 400
    assert response.get_json() == {'error': "missing file field 'file'"}


def test_upload_sanitizes_filename(client, upload_dir):
    response = client.post(
        '/demo',
        data={'file': (io.BytesIO(b'x'), '../../etc/passwd')},
        content_type='multipart/form-data',
    )

    assert response.status_code == 201
    saved = list(upload_dir.iterdir())
    assert [path.name for path in saved] == ['etc_passwd']
    assert saved[0].parent == upload_dir


def test_create_app_creates_upload_folder(tmp_path):
    target = tmp_path / 'nested' / 'uploads'

    create_app({'TESTING': True, 'UPLOAD_FOLDER': str(target)})

    assert target.is_dir()
