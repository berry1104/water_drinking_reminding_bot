from flask import Flask, render_template, jsonify
import sqlite3
import subprocess

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

# 配置数据库连接信息
db_name = 'water_data_test.db'

@app.route('/')
def index():
    return render_template('index.html')

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
