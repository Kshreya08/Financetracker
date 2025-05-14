import sqlite3
import os

# Resolve absolute path to backend/data.db
backend_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend', 'data.db'))
print("Using database:", backend_db_path)

if not os.path.exists(backend_db_path):
    print("❌ Database file not found at path above.")
    exit()

# Connect and inspect tables
conn = sqlite3.connect(backend_db_path)
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("\nTables in DB:")
for table in tables:
    print(table[0])

# View 'user' table
print("\nUser table contents:")
try:
    cursor.execute("SELECT * FROM user;")
    for row in cursor.fetchall():
        print(row)
except Exception as e:
    print("Error:", e)

# View 'expense' table
print("\nExpense table contents:")
try:
    cursor.execute("SELECT * FROM expense;")
    for row in cursor.fetchall():
        print(row)
except Exception as e:
    print("Error:", e)

conn.close()
