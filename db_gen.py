import sqlite3

connection = sqlite3.connect("users.db")
cursor = connection.cursor()

query = """CREATE TABLE user_data(
            username TEXT PRIMARY KEY UNIQUE NOT NULL,
            active INTEGER NOT NULL,
            auth_method TEXT NOT NULL,
            password TEXT NOT NULL,
            auth INTEGER NOT NULL,
            roles TEXT NOT NULL);"""

cursor.execute(query)

