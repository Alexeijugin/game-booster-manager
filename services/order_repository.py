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

order = get_order(7)
print(order)