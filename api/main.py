from fastapi import FastAPI

from api.schemas import CreateOrderRequest
from models.order import Order
from services.order_repository import create_order

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