import sqlite3

conn = sqlite3.connect("data/sql_store.db")
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS USERS (
                   ID INTEGER PRIMARY KEY,
                   NAME TEXT,
                   ROLE TEXT
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS ORDERS (
                   ID INTEGER PRIMARY KEY,
                   USER_ID INTEGER,
                   ITEM TEXT,
                   PRICE REAL
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS VENDORS (
                   ID INTEGER PRIMARY KEY,
                   NAME TEXT,
                   CUISINE TEXT
               )
               """)

cursor.executemany(
                """
                INSERT INTO users (id, name, role)
                VALUES (?, ?, ?)
                """,
                [
                (1, "Alice", "Employee"),
                (2, "Bob", "Pantry Manager"),
                (3, "Charlie", "Employee"),
                (4, "David", "Vendor")
                ])

cursor.executemany(
                """
                INSERT INTO orders (id, user_id, item, price)
                VALUES (?, ?, ?, ?)
                """,
                [
                (1, 1, "Burger", 120),
                (2, 1, "Coffee", 40),
                (3, 3, "Pizza", 200),
                (4, 3, "Pasta", 180)
                ])

cursor.executemany(
                """
                INSERT INTO vendors (id, name, cuisine)
                VALUES (?, ?, ?)
                """,
                [
                (1, "FoodHub", "Multi Cuisine"),
                (2, "SpiceKitchen", "Indian")
                ])

conn.commit()
conn.close()

print("Database Init Completed")