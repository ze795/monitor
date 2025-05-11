import akshare as ak
import pandas as pd
import time
import threading
import json
import hashlib
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
from datetime import datetime
import random  # 用于模拟价格数据

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# 期货品种数据
futures_instruments = [
    {"id": 0, "name": "PVC连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 1, "name": "棕榈油连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 2, "name": "豆二连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 3, "name": "豆粕连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 4, "name": "铁矿石连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 5, "name": "塑料连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 6, "name": "聚丙烯连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 7, "name": "豆油连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 8, "name": "玉米连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 9, "name": "豆一连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 10, "name": "苯乙烯连续ac", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 11, "name": "PTA连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 12, "name": "菜油连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 13, "name": "菜粕连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 14, "name": "白糖连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 15, "name": "棉花连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 16, "name": "甲醇连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 17, "name": "玻璃连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 18, "name": "红枣连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 19, "name": "纯碱连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 20, "name": "螺纹钢连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""},
    {"id": 21, "name": "纸浆连续", "price": 0, "monitor_price": 0, "price_monitor": False, "atr_direction": "多", "atr_monitor": False, "pattern_direction": "多", "pattern_monitor": False, "status": ""}
]

# 监测配置
monitoring_config = {
    "auto_refresh": True,
    "price_alert_notify": True,
    "atr_alert_notify": True,
    "pattern_alert_notify": True
}

# 预警历史
alert_history = []

# 用户账户
users = {
    "admin": hashlib.sha256("1234".encode()).hexdigest()  # 密码哈希值
}

# 身份验证装饰器
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ATR计算函数（示例实现，需根据实际需求完善）
def calculate_atr(symbol, timeframe='daily', period=14):
    """计算ATR指标
    
    Args:
        symbol: 期货品种代码
        timeframe: 时间周期，如'daily'
        period: ATR计算周期
        
    Returns:
        当前ATR值
    """
    try:
        # 使用akshare获取期货历史数据
        # 注意：这里需要根据实际期货品种代码调整
        df = ak.futures_main_sina(symbol=symbol)
        
        # 计算TR (True Range)
        df['high_low'] = df['最高价'] - df['最低价']
        df['high_close'] = abs(df['最高价'] - df['收盘价'].shift())
        df['low_close'] = abs(df['最低价'] - df['收盘价'].shift())
        df['tr'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
        
        # 计算ATR (Average True Range)
        df['atr'] = df['tr'].rolling(window=period).mean()
        
        return df['atr'].iloc[-1]
    except Exception as e:
        print(f"计算ATR时出错: {e}")
        return None

# 形态识别函数（示例实现，需根据实际需求完善）
def recognize_pattern(symbol, timeframe='daily'):
    """识别K线形态
    
    Args:
        symbol: 期货品种代码
        timeframe: 时间周期，如'daily'
        
    Returns:
        识别出的形态名称或None
    """
    try:
        # 使用akshare获取期货历史数据
        df = ak.futures_main_sina(symbol=symbol)
        
        # 这里应该实现形态识别逻辑
        # 示例：简单识别锤子线形态
        # 锤子线条件: 下影线长，实体小，上影线短
        last_candle = df.iloc[-1]
        prev_candle = df.iloc[-2]
        
        # 简化的形态识别逻辑
        if last_candle['收盘价'] > last_candle['开盘价']:  # 阳线
            body = last_candle['收盘价'] - last_candle['开盘价']
            lower_shadow = last_candle['开盘价'] - last_candle['最低价']
            upper_shadow = last_candle['最高价'] - last_candle['收盘价']
            
            if lower_shadow > 2 * body and upper_shadow < 0.1 * body:
                return "锤子线"
                
        return None  # 未识别出形态
    except Exception as e:
        print(f"形态识别时出错: {e}")
        return None

# 监测任务
def monitoring_task():
    """定时监测任务，每分钟执行一次"""
    while True:
        if monitoring_config["auto_refresh"]:
            print("开始执行监测任务...")
            perform_monitoring()
            print("监测任务完成")
            
            # 发送更新到所有客户端
            socketio.emit('update_data', {'instruments': futures_instruments})
        
        # 每分钟执行一次
        time.sleep(60)

# 执行监测
def perform_monitoring():
    """执行全量监测"""
    global futures_instruments
    
    for i, instrument in enumerate(futures_instruments):
        try:
            # 获取实时价格（使用akshare）
            # 注意：这里需要根据实际期货品种代码调整
            real_time_price = get_real_time_price(instrument["name"])
            if real_time_price is not None:
                futures_instruments[i]["price"] = real_time_price
                
                # 价格监测
                if instrument["price_monitor"] and instrument["monitor_price"] != 0:
                    if abs(float(real_time_price) - float(instrument["monitor_price"])) <= 2:
                        futures_instruments[i]["status"] = "价格预警"
                        add_alert_history(instrument["name"], "价格预警")
                        if monitoring_config["price_alert_notify"]:
                            socketio.emit('alert', {
                                'message': f"{instrument['name']} 价格预警 (监测价: {instrument['monitor_price']})",
                                'type': 'danger'
                            })
                    else:
                        # 检查是否需要清除预警状态
                        if futures_instruments[i]["status"] == "价格预警":
                            futures_instruments[i]["status"] = ""
                
                # ATR监测
                if instrument["atr_monitor"]:
                    atr_value = calculate_atr(instrument["name"])
                    if atr_value is not None:
                        # ATR监测逻辑（这里需要根据实际策略调整）
                        # 示例：ATR值连续增加时触发预警
                        is_atr_alert = check_atr_alert(instrument["name"], atr_value, instrument["atr_direction"])
                        if is_atr_alert:
                            futures_instruments[i]["status"] = "ATR预警"
                            add_alert_history(instrument["name"], "ATR预警")
                            if monitoring_config["atr_alert_notify"]:
                                socketio.emit('alert', {
                                    'message': f"{instrument['name']} ATR预警 (方向: {instrument['atr_direction']})",
                                    'type': 'warning'
                                })
                        else:
                            if futures_instruments[i]["status"] == "ATR预警":
                                futures_instruments[i]["status"] = ""
                
                # 形态监测
                if instrument["pattern_monitor"]:
                    pattern = recognize_pattern(instrument["name"])
                    if pattern is not None:
                        futures_instruments[i]["status"] = f"形态预警 ({pattern})"
                        add_alert_history(instrument["name"], f"形态预警 ({pattern})")
                        if monitoring_config["pattern_alert_notify"]:
                            socketio.emit('alert', {
                                'message': f"{instrument['name']} 形态预警 ({pattern}, 方向: {instrument['pattern_direction']})",
                                'type': 'warning'
                            })
                    else:
                        if futures_instruments[i]["status"].startswith("形态预警"):
                            futures_instruments[i]["status"] = ""
            else:
                print(f"获取{instrument['name']}价格失败")
                
        except Exception as e:
            print(f"处理{instrument['name']}时出错: {e}")

# 获取实时价格（示例实现，需根据实际需求完善）
def get_real_time_price(instrument_name):
    """获取期货实时价格
    
    Args:
        instrument_name: 期货品种名称
        
    Returns:
        实时价格或None
    """
    try:
        # 这里应该使用akshare获取实时价格
        # 示例中使用随机数模拟价格
        # 实际应用中需要根据品种名称映射到正确的期货代码
        # price = ak.futures_realtime_sina(symbol=instrument_code)
        price = round(1000 + random.random() * 200, 2)  # 模拟价格
        return str(price)
    except Exception as e:
        print(f"获取{instrument_name}实时价格时出错: {e}")
        return None

# 检查ATR预警条件（示例实现，需根据实际需求完善）
def check_atr_alert(instrument_name, current_atr, direction):
    """检查ATR预警条件
    
    Args:
        instrument_name: 期货品种名称
        current_atr: 当前ATR值
        direction: 监测方向 ('多'或'空')
        
    Returns:
        是否触发预警
    """
    # 这里应该实现ATR预警逻辑
    # 示例：ATR值连续增加或减少时触发预警
    return random.random() > 0.8  # 随机模拟20%的概率触发预警

# 添加预警历史
def add_alert_history(instrument_name, alert_type):
    """添加预警记录到历史"""
    global alert_history
    
    alert = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "instrument": instrument_name,
        "type": alert_type
    }
    
    alert_history.insert(0, alert)  # 添加到开头
    # 限制历史记录数量
    if len(alert_history) > 100:
        alert_history.pop()

# 路由
@app.route('/', endpoint='index')  # 明确指定端点名称为'index'
@login_required
def index():
    return render_template('index.html', instruments=futures_instruments, config=monitoring_config)

@app.route('/login', methods=['GET', 'POST'], endpoint='login')  # 明确指定端点名称为'login'
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 验证用户名和密码
        if username in users and users[username] == hashlib.sha256(password.encode()).hexdigest():
            session['username'] = username
            return redirect(url_for('index'))  # 现在可以正确解析'index'端点
        else:
            return render_template('login.html', error='用户名或密码错误')
    
    return render_template('login.html')

@app.route('/logout', endpoint='logout')  # 明确指定端点名称为'logout'
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))  # 明确指定端点名称    

# 明确指定端点名称，避免冲突
@app.route('/api/instruments', methods=['GET'], endpoint='api_instruments')
@login_required
def get_instruments():
    return jsonify(futures_instruments)

@app.route('/api/config', methods=['GET', 'POST'], endpoint='api_config')
@login_required
def config():
    if request.method == 'POST':
        global monitoring_config
        monitoring_config = request.json
        return jsonify({"status": "success", "config": monitoring_config})
    return jsonify(monitoring_config)

@app.route('/api/update_monitor_price', methods=['POST'], endpoint='api_update_monitor_price')
@login_required
def update_monitor_price():
    data = request.json
    index = data.get('index')
    price = data.get('price')
    
    if index is not None and index < len(futures_instruments):
        futures_instruments[index]['monitor_price'] = float(price)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "无效的索引"})

@app.route('/api/toggle_price_monitor', methods=['POST'], endpoint='api_toggle_price_monitor')
@login_required
def toggle_price_monitor():
    data = request.json
    index = data.get('index')
    status = data.get('status')
    
    if index is not None and index < len(futures_instruments):
        futures_instruments[index]['price_monitor'] = status
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "无效的索引"})

@app.route('/api/update_atr_direction', methods=['POST'], endpoint='api_update_atr_direction')
@login_required
def update_atr_direction():
    data = request.json
    index = data.get('index')
    direction = data.get('direction')
    
    if index is not None and index < len(futures_instruments):
        futures_instruments[index]['atr_direction'] = direction
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "无效的索引"})

@app.route('/api/toggle_atr_monitor', methods=['POST'], endpoint='api_toggle_atr_monitor')
@login_required
def toggle_atr_monitor():
    data = request.json
    index = data.get('index')
    status = data.get('status')
    
    if index is not None and index < len(futures_instruments):
        futures_instruments[index]['atr_monitor'] = status
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "无效的索引"})

@app.route('/api/update_pattern_direction', methods=['POST'], endpoint='api_update_pattern_direction')
@login_required
def update_pattern_direction():
    data = request.json
    index = data.get('index')
    direction = data.get('direction')
    
    if index is not None and index < len(futures_instruments):
        futures_instruments[index]['pattern_direction'] = direction
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "无效的索引"})

@app.route('/api/toggle_pattern_monitor', methods=['POST'], endpoint='api_toggle_pattern_monitor')
@login_required
def toggle_pattern_monitor():
    data = request.json
    index = data.get('index')
    status = data.get('status')
    
    if index is not None and index < len(futures_instruments):
        futures_instruments[index]['pattern_monitor'] = status
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "无效的索引"})

@app.route('/api/alerts', methods=['GET'], endpoint='api_alerts')
@login_required
def get_alerts():
    return jsonify(alert_history)

# SocketIO事件
@socketio.on('connect')
def handle_connect():
    if 'username' in session:
        emit('initial_data', {'instruments': futures_instruments, 'config': monitoring_config})
    else:
        # 未登录用户断开连接
        disconnect()

if __name__ == '__main__':
    # 启动监测线程
    monitoring_thread = threading.Thread(target=monitoring_task)
    monitoring_thread.daemon = True
    monitoring_thread.start()
    
    # 启动Flask应用
    # socketio.run(app, debug=True, host='0.0.0.0', port=5000)    
    socketio.run(app, debug=True, host='192.168.31.228', port=5000)    