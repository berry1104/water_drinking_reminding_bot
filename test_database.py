DIAMETER = 5
import sqlite3
import time

# Database connection and table creation
conn = sqlite3.connect('distance_data.db')  # Connect to or create the database file
cursor = conn.cursor()
# Create a table to store distance data if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS distance_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    distance REAL
                )''')
conn.commit()

def get_amount(DIAMETER):
    return 100

for i in range(10):

    amount = get_amount(DIAMETER)
    now = time.ctime()
    print(f" -------- - {i}th test ----------")
    print("now is", now)
    print("amount is", amount)



except KeyboardInterrupt:
    #GPIO.cleanup()
    conn.close()