# Owner: Emma R
# Query helpers for grocery items in the SQLite database.

from data.db import ITEMS, execute, fetch_all, get_connection


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


def increment_stock(item_id, amount=1):
    """Add stock back when an item is removed from the cart. Returns the updated item."""
    if amount <= 0:
        return None
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
    execute(
        """
        UPDATE items
        SET stock_quantity = stock_quantity + ?
        WHERE item_id = ?
        """,
        (amount, item_id),
    )
    item["stock_quantity"] += amount
    return item


def restock_all():
    """Reset every item's stock to its starting amount.

    Called when a new shopping session starts, so stock taken by earlier
    sessions (or earlier runs of the game) can't make an order impossible.
    """
    conn = get_connection()
    try:
        conn.executemany(
            "UPDATE items SET stock_quantity = ? WHERE item_name = ?",
            [(stock, name) for name, _aisle, _price, stock in ITEMS],
        )
        conn.commit()
    finally:
        conn.close()