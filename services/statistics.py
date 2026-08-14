def calculate_statistics(orders):
    total_profit = 0
    total_hours = 0

    for order in orders:
        profit, _ = order.calculate_profit()
        total_profit += profit
        total_hours += order.hours

    real_profit_per_hour = total_profit / total_hours
    return total_profit, total_hours, real_profit_per_hour
