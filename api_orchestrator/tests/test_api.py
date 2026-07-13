from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from api_orchestrator import main as app_module


class FakeBackend:
    def estimate_gemm_cache(self, N, tile):
        # return object with attributes expected by the API
        return SimpleNamespace(cache_misses=(N // tile) * 10, accesses=N * N)


@pytest.fixture(autouse=True)
def patch_backend(monkeypatch):
    # default: no backend (simulate missing extension)
    monkeypatch.setattr(app_module.dependencies, 'get_backend', lambda: None)


def test_estimate_backend_missing():
    client = TestClient(app_module.app)
    resp = client.post('/estimate', json={'N': 16, 'tile': 4})
    assert resp.status_code == 500
    assert 'Backend not available' in resp.json().get('detail', '')


def test_estimate_success(monkeypatch):
    # Patch to return a fake backend for this test
    monkeypatch.setattr(app_module.dependencies, 'get_backend', lambda: FakeBackend())
    client = TestClient(app_module.app)
    resp = client.post('/estimate', json={'N': 8, 'tile': 2})
    assert resp.status_code == 200
    body = resp.json()
    assert 'cache_misses' in body and 'accesses' in body
    assert body['accesses'] == 64
