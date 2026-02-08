import os
import uuid
import httpx

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def test_health_ok():
    r = httpx.get(f"{BASE_URL}/healthz", timeout=5)
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_event_and_list():
    payload = {"ok": True, "n": 123, "req": str(uuid.uuid4())}
    r = httpx.post(
        f"{BASE_URL}/events",
        json={"source": "pytest", "type": "smoke", "payload": payload},
        timeout=10,
    )
    assert r.status_code == 201
    data = r.json()
    assert isinstance(data["id"], int)
    assert data["source"] == "pytest"
    assert data["type"] == "smoke"
    assert data["payload"] == payload
    assert "created_at" in data

    r2 = httpx.get(f"{BASE_URL}/events?limit=20", timeout=10)
    assert r2.status_code == 200
    items = r2.json()
    assert isinstance(items, list)
    assert len(items) >= 1
    assert items[0]["id"] >= data["id"]  # последние сверху


def test_create_event_rejects_extra_fields():
    r = httpx.post(
        f"{BASE_URL}/events",
        json={"source": "pytest", "type": "bad", "payload": {}, "extra": 1},
        timeout=10,
    )
    assert r.status_code == 422


def test_list_limit_validation():
    r = httpx.get(f"{BASE_URL}/events?limit=0", timeout=10)
    assert r.status_code == 422

    r2 = httpx.get(f"{BASE_URL}/events?limit=999", timeout=10)
    assert r2.status_code == 422


def test_request_id_header_is_set():
    r = httpx.get(f"{BASE_URL}/healthz", timeout=5)
    assert r.status_code == 200
    assert "X-Request-Id" in r.headers
    assert r.headers["X-Request-Id"]
