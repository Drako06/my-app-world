from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from db.db_config import get_db
import os
from dotenv import load_dotenv

load_dotenv()
URL_DATABASE = os.getenv('URL_DATABASE')

SQLALCHEMY_DATABASE_URL = URL_DATABASE

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def atomic(test_func):
    def wrapper(*args, **kwargs):
        session = TestingSessionLocal()
        app.dependency_overrides[get_db] = lambda: session

        connection = engine.connect()
        transaction = connection.begin()
        session.connection = connection

        try:
            result = test_func(*args, **kwargs, session=session)
            transaction.rollback()
        except Exception as e:
            transaction.rollback()
            raise e
        finally:
            session.close()
            connection.close()

        return result

    return wrapper
