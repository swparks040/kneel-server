import json
import sqlite3
from modules import Styles
STYLES = [
        { "id": 1, "style": "Classic", "price": 500 },
        { "id": 2, "style": "Modern", "price": 710 },
        { "id": 3, "style": "Vintage", "price": 965 }
]

def get_all_styles():
    # Open a connection to the database
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            st.id,
            st.style,
            st.price
        FROM styles st
        """
        )
        # Initialize an empty list to hold all style representations
        styles = []
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        # Iterate list of data returned from database
        for row in dataset:
            # Create a style instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # style class above.
            style = Styles(row["id"], row["style"], row["price"])
            styles.append(style.__dict__)
 
    return styles
def get_single_style(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
        SELECT
            st.id,
            st.style,
            st.price
        FROM Styles st
        WHERE st.id = ?
        """,
            (id,),
        )

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create a style instance from the current row
        style = Styles(
            data['id'],
            data['style'],
            data['price'],
        )
        return style.__dict__

def create_style(style):
    # Get the id value of the last style in the list
    max_id = STYLES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the style dictionary
    style["id"] = new_id

    # Add the style dictionary to the list
    STYLES.append(style)

    # Return the dictionary with `id` property added
    return style
def delete_style(id):
    # Initial -1 value for style index, in case one isn't found
    style_index = -1

    # Iterate the styleS list, but use enumerate() so that you
    # can access the index value of each item
    for index, style in enumerate(STYLES):
        if style["id"] == id:
            # Found the style. Store the current index.
            style_index = index

    # If the style was found, use pop(int) to remove it from list
    if style_index >= 0:
        STYLES.pop(style_index)

def update_style(id, new_style):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Styles
            SET
                style = ?,
                price = ?
        WHERE id = ?
        """, (new_style['style'], new_style['price'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True