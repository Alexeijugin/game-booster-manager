from fastapi import FastAPI, HTTPException
from typing import Optional
from fastapi import Query

from api.schemas import CreateOrderRequest, OrderResponse
from models.order import Order
from services.order_repository import create_order, get_order, delete_order, update_order, get_orders

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/orders")
def create_order_endpoint(order_data: CreateOrderRequest):
    order = Order(
        order_data.price,
        order_data.hours,
        order_data.commission_percent,
    )

    profit, profit_per_hour = order.calculate_profit()

    order_id = create_order(
        order_data.price,
        order_data.hours,
        order_data.commission_percent,
        order_data.booster_id,
    )

    return {
        "id": order_id,
        "profit": profit,
        "profit_per_hour": profit_per_hour,
    }


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_endpoint(order_id: int):
    order = get_order(order_id)

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "id": order[0],
        "price": float(order[1]),
        "hours": float(order[2]),
        "commission_percent": float(order[3]),
        "booster_id": order[4],
    }

@app.get("/orders")
def get_orders_endpoint(
    booster_id: Optional[int] = Query(default=None),
):
    orders = get_orders(booster_id)

    return [
        {
            "id": order[0],
            "price": float(order[1]),
            "hours": float(order[2]),
            "commission_percent": float(order[3]),
            "booster_id": order[4],
        }
        for order in orders
    ]


@app.delete("/orders/{order_id}", status_code=204)
def delete_order_endpoint(order_id: int):
    deleted = delete_order(order_id)

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}", response_model=OrderResponse)
def update_order_endpoint(
    order_id: int,
    order_data: CreateOrderRequest,
):
    updated = update_order(
        order_id,
        order_data.price,
        order_data.hours,
        order_data.commission_percent,
        order_data.booster_id,
    )

    if updated == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "id": order_id,
        "price": order_data.price,
        "hours": order_data.hours,
        "commission_percent": order_data.commission_percent,
        "booster_id": order_data.booster_id,
    }