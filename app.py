import time, random
import threading
from flask import Flask, render_template, request, redirect, url_for, session, flash
# 假设 get_price 函数已经定义
# from some_module import get_price

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 模拟商品数据（名称、监测价格、开关、提醒标志）
products = [
    {"name": "Product A", "monitor_price": 3000, "price_switch": True, "alert": ""},
    {"name": "Product B", "monitor_price": 2000, "price_switch": False, "alert": ""},
    # 添加更多产品
]

# 用户凭证
USERNAME = 'admin'
PASSWORD = '1234'

def get_price():
    return random.random()

def price_monitor():
    while True:
        for product in products:
            if product["price_switch"]:
                current_price = get_price(product["name"])
                if current_price > product["monitor_price"]:
                    product["alert"] = f"Alert: {product['name']} price exceeded {product['monitor_price']}!"
                else:
                    product["alert"] = ""
        time.sleep(5)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!')

    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        # 更新监测和开关状态
        name = request.form.get('product_name')
        monitor_price = int(request.form.get('monitor_price'))
        for product in products:
            if product["name"] == name:
                product["monitor_price"] = monitor_price
                product["price_switch"] = "price_switch" in request.form
                break

    return render_template('dashboard.html', products=products)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # 启动一个后台线程来监控
    threading.Thread(target=price_monitor, daemon=True).start()
    app.run(host='127.0.0.1', port=5001)
