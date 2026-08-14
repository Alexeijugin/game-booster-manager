def calculate_order(price, hours, commission_percent):
    if hours <= 0:
        raise ValueError("Часов должно быть больше чем 0")
    if price <= 0:
        raise ValueError("Цена должна быть больше чем 0")
    if commission_percent < 0 or commission_percent > 100:
        raise ValueError("Комиссия должна быть от 0 до 100")

    commission = price / 100 * commission_percent
    price_non_commission = price - commission
    profit_for_hour = price_non_commission / hours

    return price_non_commission, profit_for_hour

