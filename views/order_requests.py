import json
import sqlite3
from modules import Orders, Metals, Sizes, Styles
from .metal_requests import get_single_metal
from .size_requests import get_single_size
from .style_requests import get_single_style

ORDERS = [
    {
        "id": 1,
        "metalId": 3,
        "sizeId": 2,
        "styleId": 3,
        "timestamp": 1614659931693
    }
]

def get_all_orders():
    # Open a connection to the database
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # swp - this is my SQL query (full dict. for orders, relevent items from
        # metal, size and style)
        db_cursor.execute(
            """
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            o.timestamp,
            m.metal metal_metal,
            m.price metal_price,
            si.carats size_carats,
            si.price size_price,
            st.style style_style,
            st.price style_price
        FROM Orders o
        JOIN Metals m
            ON m.id = o.metal_id
        JOIN Sizes si
            ON si.id = o.size_id
        JOIN Styles st
            ON st.id = o.style_id
        """
        )
        # coach - Initialize an empty list to hold all order representations
        orders = []
        # coach - Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        # Iterate list of data returned from database
        for row in dataset:
            # Create an order instance from the current row
            order = Orders(
                row["id"],
                row["metal_id"],
                row["size_id"],
                row["style_id"],
                row["timestamp"],
            )
            # swp - Create a Metals instance from the current row
            metal = Metals(
                row["id"], row["metal_metal"], row["metal_price"]
            )
            # swp - Create a Sizes instance from the current row
            size = Sizes(
                row["id"],
                row["size_carats"],
                row["size_price"],
            )
            # swp - Create a Styles instance from the current row
            style = Styles(
                row["id"],
                row["style_style"],
                row["style_price"],
            )
            # Add the dictionary representation of the metal to the order
            order.metal = metal.__dict__
            # Add the dictionary representation of the size to the order
            order.size = size.__dict__
            # Add the dictionary representation of the style to the order
            order.style = style.__dict__
            # Add the dictionary representation of the order to the list
            orders.append(order.__dict__)
    return orders

def get_single_order(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            o.timestamp
        FROM Orders o
        WHERE o.id = ?
        """,
            (id,),
        )
        # Load the single result into memory
        data = db_cursor.fetchone()
        # Create an order instance from the current row
        order = Orders(
            data["id"],
            data["metal_id"],
            data["size_id"],
            data["style_id"],
            data["timestamp"],
        )
        return order.__dict__

def create_order(new_order):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
        INSERT INTO Orders
            ( metal_id, size_id, style_id, timestamp )
        VALUES
            ( ?, ?, ?, ? );
        """,
            (
                new_order["metal_id"],
                new_order["size_id"],
                new_order["style_id"],
                new_order["timestamp"],
            ),
        )
        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid
        # Add the `id` property to the order dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_order["id"] = id
    return new_order

def delete_order(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
        DELETE FROM Orders
        WHERE id = ?
        """,
            (id,),
        )


def update_order(id, new_order):
    # Iterate the orderS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Update the value.
            ORDERS[index] = new_order
            break