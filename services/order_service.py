from services.payment import process_payment



def create_order_payment(amount: float) -> str:
    return process_payment(amount)
