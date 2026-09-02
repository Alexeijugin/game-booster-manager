import pytest

from api.schemas import OrderResponse


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_order(client, db_connection, cleanup_order):
    response = client.post(
        "/orders",
        json={
            "price": 1000,
            "hours": 2.5,
            "commission_percent": 10,
            "booster_id": 1,
        },
    )

    data = response.json()
    order_id = data["id"]

    cleanup_order.append(order_id)

    assert response.status_code == 200
    assert data["profit"] == 900
    assert data["profit_per_hour"] == 360
    assert isinstance(data["id"], int)

    with db_connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM orders WHERE id = %s",
            (order_id,),
        )

        order = cursor.fetchone()

    assert order == (
        order_id,
        1000,
        2.5,
        10,
        1,
    )


def test_create_order_invalid_hours(client):
    response = client.post(
        "/orders",
        json={
            "price": 1000,
            "hours": 0,
            "commission_percent": 10,
            "booster_id": 1,
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["type"] == "greater_than"
    assert error["loc"] == ["body", "hours"]


@pytest.mark.parametrize(
    "price, hours, commission_percent, expected_field, expected_type",
    [
        (1000, 0, 10, "hours", "greater_than"),
        (-100, 1, 10, "price", "greater_than"),
        (100, 1, -10, "commission_percent", "greater_than_equal"),
    ],
)
def test_create_order_invalids(
        client,
        price,
        hours,
        commission_percent,
        expected_field,
        expected_type,
):
    response = client.post(
        "/orders",
        json={
            "price": price,
            "hours": hours,
            "commission_percent": commission_percent,
            "booster_id": 1,
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["loc"] == ["body", expected_field]
    assert error["type"] == expected_type


@pytest.mark.parametrize(
    "missing_field",
    [
        "price",
        "hours",
        "commission_percent",
        "booster_id",
    ],
)
def test_create_order_missing_required_field(client, missing_field):
    data = {
        "price": 1000,
        "hours": 2.5,
        "commission_percent": 10,
        "booster_id": 1,
    }

    data.pop(missing_field)

    response = client.post("/orders", json=data)

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["type"] == "missing"
    assert error["loc"] == ["body", missing_field]


@pytest.mark.parametrize(
    "invalid_field, invalid_value",
    [
        ("price", "abc"),
        ("hours", "abc"),
        ("commission_percent", "abc"),
    ],
)
def test_create_order_invalid_type(client, invalid_field, invalid_value):
    data = {
        "price": 1000,
        "hours": 2.5,
        "commission_percent": 10,
        "booster_id": 1,
    }

    data[invalid_field] = invalid_value

    response = client.post("/orders", json=data)

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["type"] == "float_parsing"
    assert error["loc"] == ["body", invalid_field]


def test_get_order(client):
    response = client.get("/orders/2")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 2
    assert data["price"] == 950
    assert data["hours"] == 3
    assert data["commission_percent"] == 10
    assert data["booster_id"] == 1

def test_get_orders_by_booster(client):
    response = client.get(
        "/orders",
        params={
            "booster_id": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    for order in data:
        assert order["booster_id"] == 1


def test_get_order_not_found(client):
    response = client.get("/orders/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Order not found"
    }


def test_delete_order(client):
    create_response = client.post(
        "/orders",
        json={
            "price": 1000,
            "hours": 2.5,
            "commission_percent": 10,
            "booster_id": 1,
        },
    )

    assert create_response.status_code == 200

    order_id = create_response.json()["id"]

    delete_response = client.delete(f"/orders/{order_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/orders/{order_id}")

    assert get_response.status_code == 404





def test_delete_order_not_found(client):
    response = client.delete("/orders/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Order not found"
    }

def test_update_order(client):
    create_response = client.post(
        "/orders",
        json={
            "price": 1000,
            "hours": 2.5,
            "commission_percent": 10,
            "booster_id": 1,
        },
    )

    assert create_response.status_code == 200

    order_id = create_response.json()["id"]

    update_response = client.put(
        f"/orders/{order_id}",
        json={
            "price": 1500,
            "hours": 4,
            "commission_percent": 15,
            "booster_id": 2,
        },
    )

    assert update_response.status_code == 200
    assert update_response.json() == {
        "id": order_id,
        "price": 1500,
        "hours": 4,
        "commission_percent": 15,
        "booster_id": 2,
    }

    get_response = client.get(f"/orders/{order_id}")

    assert get_response.status_code == 200
    assert get_response.json() == {
        "id": order_id,
        "price": 1500,
        "hours": 4,
        "commission_percent": 15,
        "booster_id": 2,
    }

    client.delete(f"/orders/{order_id}")

def test_update_order_not_found(client):
    response = client.put(
        "/orders/999",
        json={
            "price": 1500,
            "hours": 4,
            "commission_percent": 15,
            "booster_id": 2,
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Order not found"
    }


def test_get_order_response_schema(client):
    response = client.get("/orders/2")

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert "price" in data
    assert "hours" in data
    assert "commission_percent" in data
    assert "booster_id" in data

    assert isinstance(data["id"], int)
    assert isinstance(data["price"], float)
    assert isinstance(data["hours"], float)
    assert isinstance(data["commission_percent"], float)
    assert isinstance(data["booster_id"], int)


def test_get_order_response_model(client):
    response = client.get("/orders/2")

    assert response.status_code == 200

    order = OrderResponse(**response.json())

    assert order.id == 2
    assert order.price == 950
    assert order.hours == 3
    assert order.commission_percent == 10
    assert order.booster_id == 1

def test_get_order_content_type(client):
    response = client.get("/orders/2")

    assert response.headers["content-type"] == "application/json"

def test_get_orders_invalid_booster_id(client):
    response = client.get(
        "/orders",
        params={"booster_id": "abc"},
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["type"] == "int_parsing"
    assert error["loc"] == ["query", "booster_id"]