import json
import sqlite3
from modules import Sizes
SIZES = [
        { "id": 1, "carats": 0.5, "price": 405 },
        { "id": 2, "carats": 0.75, "price": 782 },
        { "id": 3, "carats": 1, "price": 1470 },
        { "id": 4, "carats": 1.5, "price": 1997 },
        { "id": 5, "carats": 2, "price": 3638 }
]

def get_all_sizes():
    # Open a connection to the database
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            si.id,
            si.carats,
            si.price
        FROM sizes si
        """
        )
        # Initialize an empty list to hold all size representations
        sizes = []
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        # Iterate list of data returned from database
        for row in dataset:
            # Create a size instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # size class above.
            size = Sizes(row["id"], row["carats"], row["price"])
            sizes.append(size.__dict__)
 
    return sizes
def get_single_size(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
        SELECT
            si.id,
            si.carats,
            si.price
        FROM Sizes si
        WHERE si.id = ?
        """,
            (id,),
        )

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an metal instance from the current row
        size = Sizes(
            data['id'],
            data['carats'],
            data['price'],
        )
        return size.__dict__
def create_size(size):
    # Get the id value of the last size in the list
    max_id = SIZES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the size dictionary
    size["id"] = new_id

    # Add the size dictionary to the list
    SIZES.append(size)

    # Return the dictionary with `id` property added
    return size
def delete_size(id):
    # Initial -1 value for size index, in case one isn't found
    size_index = -1

    # Iterate the sizeS list, but use enumerate() so that you
    # can access the index value of each item
    for index, size in enumerate(SIZES):
        if size["id"] == id:
            # Found the size. Store the current index.
            size_index = index

    # If the size was found, use pop(int) to remove it from list
    if size_index >= 0:
        SIZES.pop(size_index)

def update_size(id, new_size):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Sizes
            SET
                carats = ?,
                price = ?
        WHERE id = ?
        """, (new_size['carats'], new_size['price'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
