import httpx
import pytest


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_order(client):
    response = client.post(
        "/orders",
        json={
            "price": 1000,
            "hours": 2.5,
            "commission_percent": 10,
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "profit": 900,
        "profit_per_hour": 360,
    }


def test_create_order_invalid_hours(client):
    response = client.post(
        "/orders",
        json={
            "price": 1000,
            "hours": 0,
            "commission_percent": 10,
        },
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "price, hours, commission_percent",
    [
        (1000, 0, 10),
        (-100, 1, 10),
        (100, 1, -10)
    ],
)
def test_create_order_invalids(client, price, hours, commission_percent):
    response = client.post(
        "/orders",
        json={
            "price": price,
            "hours": hours,
            "commission_percent": commission_percent
        }
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "missing_field",
    [
        "price",
        "hours",
        "commission_percent",
    ],
)
def test_create_order_missing_required_field(client, missing_field):
    data = {
        "price": 1000,
        "hours": 2.5,
        "commission_percent": 10,
    }

    data.pop(missing_field)

    response = client.post("/orders", json=data)

    assert response.status_code == 422


@pytest.mark.parametrize(
    "field, value",
    [
        ("price", "abc"),
        ("hours", "abc"),
        ("commission_percent", "abc"),
    ],
)
def test_create_order_invalid_type(client, field, value):
    data = {
        "price": 1000,
        "hours": 2.5,
        "commission_percent": 10,
    }

    data[field] = value

    response = client.post("/orders", json=data)

    assert response.status_code == 422
