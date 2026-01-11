from fastapi.testclient import TestClient


def test_read_root(client: TestClient):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Hello from warp-fastapi-demo-ai"}


def test_login_success_and_get_me(client: TestClient, test_user):
    # 로그인 요청
    resp = client.post(
        "/auth/token",
        data={"username": "test", "password": "test1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"

    token = body["access_token"]

    # 보호 엔드포인트 호출
    me_resp = client.get(
        "/users/me", headers={"Authorization": f"Bearer {token}"}
    )

    assert me_resp.status_code == 200
    me = me_resp.json()
    assert me["username"] == "test"
    assert me["full_name"] == "Test User"
    assert me["disabled"] is False


def test_login_failure_wrong_password(client: TestClient, test_user):
    resp = client.post(
        "/auth/token",
        data={"username": "test", "password": "wrong"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert resp.status_code == 401
    body = resp.json()
    assert body["detail"] == "Incorrect username or password"