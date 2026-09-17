import psycopg2
import pytest

from db_clients.database_facade import FacadeDB


@pytest.fixture(scope="session")
def data_base():
    connection = psycopg2.connect(
        database="store",
        user="store",
        password="store",
        host="localhost",
    )
    db_facade = FacadeDB(connection)
    yield db_facade
    connection.close()