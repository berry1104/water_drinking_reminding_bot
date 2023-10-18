from flask import Flask, render_template, jsonify
import sqlite3
import subprocess
from datetime import datetime, timedelta

app = Flask(__name__)
# app.config['STATIC_FOLDER'] = 'static'
app.config['DEBUG'] = True
db_name = 'water_data_test.db'


### GET DATA FROM THE LAST 24 HOURS
def get_data_since(time_delta):
    # Calculate the time range
    now = datetime.now()
    start_date = now - time_delta

    # Connect to your database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Query to fetch data from the start_date to now
    cursor.execute("SELECT * FROM water_data WHERE now >= ?", (start_date,))
    data_24 = cursor.fetchall()

    conn.close()
    return data_24


def get_last_24_hours_data():
    try:
        # Calculate the timestamp for 24 hours ago
        time_24_hours_ago = datetime.now() - timedelta(hours=24)
        
        with sqlite3.connect('water_data_test.db') as conn:
            cursor = conn.cursor()
            # Fetch records that are newer than 24 hours ago
            cursor.execute("SELECT * FROM water_data WHERE now > ?", (time_24_hours_ago.strftime('%Y-%m-%d %H:%M:%S'),))
            data_24 = cursor.fetchall()
            return data_24
    except sqlite3.Error as e:
        print("SQLITE ERROR", e)
        return None

@app.route('/data/last_24_hours', methods=['GET'])
def last_24_hours():
    data = get_last_24_hours_data()
    # if data is not None:
        # Convert the data to a format suitable for your chart, if necessary
    return jsonify(data)
    # else:
        # return jsonify({'error': 'Unable to fetch data'}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    # Connect to your database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Execute the query
    cursor.execute("SELECT * FROM water_data")
    data = cursor.fetchall()

    # Close the connection
    conn.close()

    # Convert the data to a format that can be sent as a response
    return jsonify(data)

@app.route('/get_data')
def get_data():
    # 连接到数据库
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # 执行数据库查询
    cursor.execute("SELECT * FROM water_data")

    # 获取查询结果
    data = cursor.fetchall()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    print(data)  # 打印数据以进行调试

    # 将数据转换为JSON并传递给前端
    return jsonify(data)


@app.route('/start', methods=['POST'])
def start_data_collection():
    # 启动获取数据的程序（调用 water_BCM.py）
    # 这里可以添加启动获取数据的逻辑
    subprocess.Popen(['python3', 'water_BCM.py'])
    return 'Data collection started'

@app.route('/stop', methods=['POST'])
def stop_data_collection():
    # 停止获取数据的程序（终止 water_BCM.py 进程）
    # 这里可以添加停止获取数据的逻辑
    subprocess.Popen(['pkill', '-f', 'water_BCM.py'])
    return 'Data collection stopped'


if __name__ == '__main__':
    app.run(debug=True)







### IGNORE
# @app.route('/data/<string:period>')
# def get_data(period):
#     # Calculate the time range based on the period
#     if period == "24h":
#         time_threshold = datetime.now() - timedelta(hours=24)
#     elif period == "week":
#         time_threshold = datetime.now() - timedelta(days=7)
#     else:  # Assuming "month" as default for simplicity
#         time_threshold = datetime.now() - timedelta(days=30)

#     # Connect to your database
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()

#     # Query to fetch data based on the time period
#     cursor.execute("SELECT * FROM water_data WHERE timestamp >= ?", (time_threshold,))
#     data = cursor.fetchall()

#     conn.close()

#     return jsonify(data)

# @app.route('/data/24h')
# def data_24h():
#     data = get_data_since(timedelta(days=1))  # last 24 hours
#     return jsonify(data)

# @app.route('/data/week')
# def data_week():
#     data = get_data_since(timedelta(weeks=1))  # last week
#     return jsonify(data)

# @app.route('/data/month')
# def data_month():
#     data = get_data_since(timedelta(days=30))  # last month
#     return jsonify(data)