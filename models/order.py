class Order:
    def __init__(self, price: float, hours: float, commission_percent: float):
        if hours <= 0:
            raise ValueError("Часов должно быть больше чем 0")

        if price <= 0:
            raise ValueError("Цена должна быть больше чем 0")

        if commission_percent < 0 or commission_percent > 100:
            raise ValueError("Комиссия должна быть от 0 до 100")

        self.price = price
        self.hours = hours
        self.commission_percent = commission_percent

    def calculate_profit(self):
        commission = self.calculate_commission()
        price_non_commission = self.price - commission
        profit_for_hour = price_non_commission / self.hours

        return price_non_commission, profit_for_hour

    def calculate_commission(self):
        return self.price / 100 * self.commission_percent
