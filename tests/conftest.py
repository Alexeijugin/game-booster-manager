import pytest

from models.order import Order


@pytest.fixture
def orders():
    return [
        Order(1000, 2.5, 10),
        Order(950, 3, 10),
        Order(1500, 4, 15),
        Order(700, 2, 0),
    ]