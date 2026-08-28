def test_database_connection(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT 1")

        result = cursor.fetchone()

    assert result == (1,)

def test_create_order_in_database(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO orders (price, hours, commission_percent, booster_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (1000, 2.5, 10, 1),
        )

        order_id = cursor.fetchone()[0]

    db_connection.commit()

    with db_connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM orders WHERE id = %s",
            (order_id,),
        )

        order = cursor.fetchone()

    assert order[0] == order_id
    assert order[1] == 1000
    assert order[2] == 2.5
    assert order[3] == 10
    assert order[4] == 1