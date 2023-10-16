from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
