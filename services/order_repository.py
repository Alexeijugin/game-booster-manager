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