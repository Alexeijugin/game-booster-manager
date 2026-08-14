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


orders = [
    Order(1000, 2.5, 10),
    Order(950, 3, 10),
    Order(1500, 4, 15),
    Order(700, 2, 0),
]


def calculate_statistics(orders):
    total_profit = 0
    total_hours = 0
    for order in orders:
        profit, _ = order.calculate_profit()
        total_profit += profit
        total_hours += order.hours

    real_profit_per_hour = total_profit / total_hours
    return total_profit, total_hours, real_profit_per_hour

statistics = calculate_statistics(orders)
print(statistics)

print(f"Общая прибыль: {statistics[0]:.2f} ₽")
print(f"Отработано: {statistics[1]:.2f} ч")
print(f"Прибыль/час: {statistics[2]:.2f} ₽")