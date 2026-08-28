import httpx
import pytest

from models.order import Order
from database import get_connection

@pytest.fixture
def orders():
    return [
        Order(1000, 2.5, 10),
        Order(950, 3, 10),
        Order(1500, 4, 15),
        Order(700, 2, 0),
    ]


@pytest.fixture
def order():
    return Order(1000, 2.5, 10)


@pytest.fixture
def client():
    with httpx.Client(base_url="http://127.0.0.1:8000") as client:
        yield client


@pytest.fixture
def db_connection():
    connection = get_connection()

    yield connection

    connection.rollback()
    connection.close()