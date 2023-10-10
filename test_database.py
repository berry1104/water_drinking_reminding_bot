import sqlite3
import time

DIAMETER = 5

def create_table():
    try:
        with sqlite3.connect('water_data_test.db') as conn:
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS water_data
               (id INTEGER PRIMARY KEY AUTOINCREMENT, now TEXT, amount REAL)''')
    except sqlite3.Error as e:
        print("SQLITE ERROR", e)

def insert_data(amount, now):
    try:
        with sqlite3.connect('water_data_test.db') as conn:
            cursor = conn.cursor()

            cursor.execute("INSERT INTO water_data (now, amount) VALUES (?, ?)", (now, amount))
            conn.commit()
    except sqlite3.Error as e:
        print("SQLITE ERROR", e)

def get_amount(DIAMETER):
    # You can modify this function to calculate the amount based on DIAMETER
    return 100

# Create the table if it doesn't exist
create_table()

for i in range(10):
    amount = get_amount(DIAMETER)
    now = time.ctime()
    print(f" -------- - {i}th test ----------")
    print("now is", now)
    print("amount is", amount)

    insert_data(amount, now)
