import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.database.models import Base
from src.database.database import get_postgres_db

# SQLITE_URL = "sqlite://"
SQLITE_URL = "sqlite:///recipes.db"
engine = create_engine(SQLITE_URL)

TestSession = sessionmaker(engine)

def get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='module')
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    return db

@pytest.fixture(scope="module")
def client(session):
    # Dependency override

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_postgres_db] = override_get_db

    yield TestClient(app)
