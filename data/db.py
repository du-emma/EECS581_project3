# Owner: Emma R
# Simple SQLite database for aisles and items 
# No server / Docker / passwords — just a local .db file created on first run.

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "grocery.db"

# Hardcoded starter data — edit here to change what's in the store.
AISLES = [
    ("dairy", "Dairy & Eggs"),
    ("meat", "Meat"),
    ("baking", "Baking"),
    ("produce", "Produce"),
]

ITEMS = [
    # (item_name, aisle_id, price, stock_quantity) — 15 items per aisle
    # dairy
    ("milk", "dairy", 3.49, 12),
    ("eggs", "dairy", 4.99, 8),
    ("cheese", "dairy", 2.99, 15),
    ("butter", "dairy", 4.29, 10),
    ("yogurt", "dairy", 1.89, 14),
    ("cream cheese", "dairy", 2.59, 11),
    ("sour cream", "dairy", 2.19, 13),
    ("heavy cream", "dairy", 3.79, 9),
    ("cottage cheese", "dairy", 3.29, 10),
    ("whipped cream", "dairy", 2.99, 12),
    ("string cheese", "dairy", 3.49, 16),
    ("half and half", "dairy", 2.79, 11),
    ("greek yogurt", "dairy", 4.49, 14),
    ("almond milk", "dairy", 3.99, 10),
    ("shredded cheese", "dairy", 3.59, 13),
    # meat
    ("chicken", "meat", 6.49, 9),
    ("beef", "meat", 8.99, 7),
    ("pork", "meat", 5.79, 8),
    ("turkey", "meat", 7.49, 6),
    ("salmon", "meat", 9.99, 5),
    ("bacon", "meat", 5.49, 12),
    ("sausage", "meat", 4.99, 10),
    ("ham", "meat", 6.29, 8),
    ("ground turkey", "meat", 5.99, 9),
    ("shrimp", "meat", 8.49, 7),
    ("tilapia", "meat", 6.79, 8),
    ("steak", "meat", 11.99, 5),
    ("chicken wings", "meat", 7.29, 9),
    ("hot dogs", "meat", 3.99, 14),
    ("deli turkey", "meat", 5.29, 11),
    # baking
    ("flour", "baking", 2.49, 20),
    ("sugar", "baking", 2.19, 18),
    ("baking soda", "baking", 1.29, 16),
    ("vanilla", "baking", 3.99, 11),
    ("chocolate chips", "baking", 3.49, 13),
    ("brown sugar", "baking", 2.39, 17),
    ("baking powder", "baking", 1.59, 15),
    ("cocoa powder", "baking", 3.29, 12),
    ("cake mix", "baking", 2.79, 14),
    ("frosting", "baking", 2.49, 13),
    ("yeast", "baking", 1.99, 10),
    ("cornmeal", "baking", 2.29, 12),
    ("powdered sugar", "baking", 2.19, 16),
    ("vegetable oil", "baking", 3.49, 14),
    ("sprinkles", "baking", 1.89, 18),
    # produce
    ("apples", "produce", 1.99, 25),
    ("lettuce", "produce", 2.29, 12),
    ("celery", "produce", 1.79, 14),
    ("carrots", "produce", 1.49, 22),
    ("bananas", "produce", 0.79, 30),
    ("oranges", "produce", 2.49, 20),
    ("tomatoes", "produce", 2.19, 18),
    ("potatoes", "produce", 3.49, 24),
    ("onions", "produce", 1.29, 26),
    ("broccoli", "produce", 2.59, 15),
    ("spinach", "produce", 2.99, 13),
    ("cucumbers", "produce", 1.59, 17),
    ("grapes", "produce", 3.99, 14),
    ("strawberries", "produce", 3.49, 12),
    ("avocado", "produce", 1.89, 16),
]


def get_connection():
    """Open the database, creating and seeding it if needed."""
    init_needed = not DB_PATH.exists()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    if init_needed:
        _create_and_seed(conn)
    return conn


def _create_and_seed(conn):
    conn.executescript(
        """
        CREATE TABLE aisles (
            aisle_id   TEXT PRIMARY KEY,
            aisle_name TEXT NOT NULL
        );

        CREATE TABLE items (
            item_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name      TEXT NOT NULL UNIQUE,
            aisle_id       TEXT NOT NULL,
            price          REAL NOT NULL,
            stock_quantity INTEGER NOT NULL,
            FOREIGN KEY (aisle_id) REFERENCES aisles(aisle_id)
        );
        """
    )
    conn.executemany(
        "INSERT INTO aisles (aisle_id, aisle_name) VALUES (?, ?)",
        AISLES,
    )
    conn.executemany(
        """
        INSERT INTO items (item_name, aisle_id, price, stock_quantity)
        VALUES (?, ?, ?, ?)
        """,
        ITEMS,
    )
    conn.commit()


def fetch_all(query, params=()):
    """Run a SELECT and return a list of dicts."""
    conn = get_connection()
    try:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def execute(query, params=()):
    """Run an INSERT/UPDATE/DELETE and commit."""
    conn = get_connection()
    try:
        conn.execute(query, params)
        conn.commit()
    finally:
        conn.close()


def reset_db():
    """Delete the .db file so the next connection rebuilds from AISLES/ITEMS."""
    if DB_PATH.exists():
        DB_PATH.unlink()
