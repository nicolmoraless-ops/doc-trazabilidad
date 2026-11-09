"""Pruebas unitarias de app.py."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # noqa: E402


def client():
    app.config['TESTING'] = True
    return app.test_client()


def test_hello_con_nombre():
    r = client().get('/hello?name=Duoc')
    assert r.status_code == 200
    assert r.get_data(as_text=True) == 'Hello, Duoc!'


def test_hello_sin_nombre():
    r = client().get('/hello')
    assert r.get_data(as_text=True) == 'Hello, Mundo!'


def test_hello_escapa_html():
    r = client().get('/hello?name=<script>alert(1)</script>')
    body = r.get_data(as_text=True)
    assert '<script>' not in body
    assert '&lt;script&gt;' in body


def test_health():
    r = client().get('/health')
    assert r.get_json() == {'status': 'ok'}
