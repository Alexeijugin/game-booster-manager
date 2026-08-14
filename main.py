from models.order import Order
from services.statistics import calculate_statistics

orders = [
    Order(1000, 2.5, 10),
    Order(950, 3, 10),
    Order(1500, 4, 15),
    Order(700, 2, 0),
]

statistics = calculate_statistics(orders)
print(statistics)

print(f"Общая прибыль: {statistics[0]:.2f} ₽")
print(f"Отработано: {statistics[1]:.2f} ч")
print(f"Прибыль/час: {statistics[2]:.2f} ₽")
