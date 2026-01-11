import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import Base, SessionLocal, UserORM, app, engine, pwd_context


@pytest.fixture(scope="session", autouse=True)
def setup_database() -> None:
    """Create all tables once for the test session.

    여기서는 실제 SQLite 파일(`app.db`)을 그대로 사용합니다.
    별도의 테스트 전용 DB로 분리하고 싶으면 URL을 분리하는 방식으로 확장 가능합니다.
    """
    Base.metadata.create_all(bind=engine)


@pytest.fixture()
def db() -> Generator[SessionLocal, None, None]:
    """Provide a DB session for tests."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client() -> TestClient:
    """FastAPI TestClient fixture."""
    return TestClient(app)


@pytest.fixture()
def test_user(db) -> UserORM:
    """Ensure a known test user exists in the DB and return it."""
    user = db.query(UserORM).filter(UserORM.username == "test").first()
    if not user:
        user = UserORM(
            username="test",
            full_name="Test User",
            hashed_password=pwd_context.hash("test1234"),
            disabled=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user