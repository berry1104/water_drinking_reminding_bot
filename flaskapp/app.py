from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    # Connect to your database
    conn = sqlite3.connect('water_data_test.db')
    cursor = conn.cursor()

    # Execute the query
    cursor.execute("SELECT * FROM water_data")
    data = cursor.fetchall()

    # Close the connection
    conn.close()

    # Convert the data to a format that can be sent as a response
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
