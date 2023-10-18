from flask import Flask, render_template, jsonify
import sqlite3
# import subprocess

app = Flask(__name__)
# app.config['STATIC_FOLDER'] = 'static'
app.config['DEBUG'] = True
db_name = 'water_data_test.db'

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


### POST METHODS ??
# @app.route('/start', methods=['POST'])
# def start_data_collection():
#     # 启动获取数据的程序（调用 water_BCM.py）
#     # 这里可以添加启动获取数据的逻辑
#     subprocess.Popen(['python3', 'water_BCM.py'])
#     return 'Data collection started'

# @app.route('/stop', methods=['POST'])
# def stop_data_collection():
#     # 停止获取数据的程序（终止 water_BCM.py 进程）
#     # 这里可以添加停止获取数据的逻辑
#     subprocess.Popen(['pkill', '-f', 'water_BCM.py'])
#     return 'Data collection stopped'


if __name__ == '__main__':
    app.run(debug=True)
