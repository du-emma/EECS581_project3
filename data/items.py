# Owner: Emma R
# Query helpers for grocery items in the SQLite database.

from data.db import execute, fetch_all


def get_all_aisles():
    return fetch_all(
        "SELECT aisle_id, aisle_name FROM aisles ORDER BY aisle_id"
    )


def get_all_items():
    return fetch_all(
        """
        SELECT item_id, item_name, aisle_id, price, stock_quantity
        FROM items
        ORDER BY aisle_id, item_name
        """
    )


def get_items_by_aisle(aisle_id):
    return fetch_all(
        """
        SELECT item_id, item_name, aisle_id, price, stock_quantity
        FROM items
        WHERE aisle_id = ?
        ORDER BY item_name
        """,
        (aisle_id,),
    )


def get_item_names():
    return [row["item_name"] for row in fetch_all(
        "SELECT item_name FROM items ORDER BY item_name"
    )]


def get_item_by_name(item_name):
    rows = fetch_all(
        """
        SELECT item_id, item_name, aisle_id, price, stock_quantity
        FROM items
        WHERE item_name = ?
        LIMIT 1
        """,
        (item_name,),
    )
    return rows[0] if rows else None


def decrement_stock(item_id):
    """Subtract 1 from stock if any remains. Returns the updated item, or None."""
    rows = fetch_all(
        """
        SELECT item_id, item_name, aisle_id, price, stock_quantity
        FROM items
        WHERE item_id = ?
        LIMIT 1
        """,
        (item_id,),
    )
    if not rows:
        return None
    item = rows[0]
    if item["stock_quantity"] <= 0:
        return item
    execute(
        """
        UPDATE items
        SET stock_quantity = stock_quantity - 1
        WHERE item_id = ? AND stock_quantity > 0
        """,
        (item_id,),
    )
    item["stock_quantity"] -= 1
    return item
