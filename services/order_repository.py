from database import get_connection


def get_order(order_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM orders WHERE id = %s",
                (order_id,),
            )

            return cursor.fetchone()
    finally:
        connection.close()

def get_orders(booster_id=None):
    connection = get_connection()

    with connection.cursor() as cursor:
        if booster_id:
            cursor.execute(
                """
                SELECT *
                FROM orders
                WHERE booster_id = %s
                """,
                (booster_id,),
            )
        else:
            cursor.execute(
                """
                SELECT *
                FROM orders
                """
            )

        return cursor.fetchall()


def create_order(price, hours, commission_percent, booster_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO orders (price, hours, commission_percent, booster_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (price, hours, commission_percent, booster_id),
            )

            order_id = cursor.fetchone()[0]

        connection.commit()

        return order_id
    finally:
        connection.close()


def delete_order(order_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM orders WHERE id = %s",
                (order_id,),
            )

            deleted = cursor.rowcount

        connection.commit()

        return deleted

    finally:
        connection.close()


def update_order(order_id, price, hours, commission_percent, booster_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE orders
                SET price = %s,
                    hours = %s,
                    commission_percent = %s,
                    booster_id = %s
                WHERE id = %s
                """,
                (price, hours, commission_percent, booster_id, order_id),
            )

            updated = cursor.rowcount

        connection.commit()

        return updated
    finally:
        connection.close()