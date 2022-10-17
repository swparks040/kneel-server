import json
import sqlite3
from modules import Metals

METALS = [
    {"id": 1, "metal": "Sterling Silver", "price": 12.42},
    {"id": 2, "metal": "14K Gold", "price": 736.4},
    {"id": 3, "metal": "24K Gold", "price": 1258.9},
    {"id": 4, "metal": "Platinum", "price": 795.45},
    {"id": 5, "metal": "Palladium", "price": 1241},
]


def get_all_metals():
    # Open a connection to the database
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            m.id,
            m.metal,
            m.price
        FROM Metals m
        """
        )
        # Initialize an empty list to hold all metal representations
        metals = []
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        # Iterate list of data returned from database
        for row in dataset:
            # Create a metal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # metal class above.
            metal = Metals(row["id"], row["metal"], row["price"])
            metals.append(metal.__dict__)
 
    return metals


def get_single_metal(id):
    # Variable to hold the found metal, if it exists
    requested_metal = None

    # Iterate the METALS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for metal in METALS:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if metal["id"] == id:
            requested_metal = metal
    return requested_metal


def create_metal(metal):
    # Get the id value of the last metal in the list
    max_id = METALS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the metal dictionary
    metal["id"] = new_id

    # Add the metal dictionary to the list
    METALS.append(metal)

    # Return the dictionary with `id` property added
    return metal


def delete_metal(id):
    # Initial -1 value for metal index, in case one isn't found
    metal_index = -1

    # Iterate the metalS list, but use enumerate() so that you
    # can access the index value of each item
    for index, metal in enumerate(METALS):
        if metal["id"] == id:
            # Found the metal. Store the current index.
            metal_index = index

    # If the metal was found, use pop(int) to remove it from list
    if metal_index >= 0:
        METALS.pop(metal_index)


def update_metal(id, new_metal):
    # Iterate the metalS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, metal in enumerate(METALS):
        if metal["id"] == id:
            # Found the metal. Update the value.
            METALS[index] = new_metal
            break
