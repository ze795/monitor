import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_apscheduler import APScheduler
from threading import Lock
import threading
import time
import akshare as ak

from log import *


app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

scheduler = APScheduler()
data_lock = Lock()

# Server configuration
SERVER_CONFIG = {
    'host': '192.168.31.228',
    'port': 5000,
    'debug': True
}

# Mock user database
users = {
    'admin': generate_password_hash('admin')
}

# Mock futures data
futures_data = {
    'PVC连续': {
        'symbol': 'V0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '棕榈油连续': {
        'symbol': 'P0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '豆二连续': {
        'symbol': 'B0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '豆粕连续': {
        'symbol': 'M0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '铁矿石连续': {
        'symbol': 'I0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '塑料连续': {
        'symbol': 'L0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '聚丙烯连续': {
        'symbol': 'PP0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '豆油连续': {
        'symbol': 'Y0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '玉米连续': {
        'symbol': 'C0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '豆一连续': {
        'symbol': 'A0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '苯乙烯连续ac': {
        'symbol': 'EB0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    'PTA连续': {
        'symbol': 'TA0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '菜油连续': {
        'symbol': 'OI0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '菜粕连续': {
        'symbol': 'RM0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '白糖连续': {
        'symbol': 'SR0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '棉花连续': {
        'symbol': 'CF0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '甲醇连续': {
        'symbol': 'MA0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '玻璃连续': {
        'symbol': 'FG0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '红枣连续': {
        'symbol': 'CJ0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '纯碱连续': {
        'symbol': 'SA0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '螺纹钢连续': {
        'symbol': 'RB0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    },
    '纸浆连续': {
        'symbol': 'SP0',
        'price': {
            'current_price': 0.0,
            'monitor_price': 0.0,
            'monitor_enabled': False
        },
        'atr': {
            'direction': 'Long',
            'monitor_enabled': False
        },
        'pattern': {
            'direction': 'Long',
            'monitor_enabled': False
        }
    }
}


# Check login status
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# Login verification
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Incorrect username or password')
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Home page
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Price monitoring
@app.route('/price_monitor', methods=['GET', 'POST'])
@login_required
def price_monitor():
    if request.method == 'POST':
        for symbol in futures_data:
            price = request.form.get(f'price_{symbol}')
            current_price = request.form.get(f'current_price_{symbol}')
            if price:
                futures_data[symbol]['price']['monitor_price'] = float(price)
            if current_price:
                futures_data[symbol]['price']['current_price'] = float(current_price)
            enabled = request.form.get(f'enabled_{symbol}')
            futures_data[symbol]['price']['monitor_enabled'] = enabled == 'on'
        return redirect(url_for('price_monitor'))
    
    return render_template('price_monitor.html', futures_data=futures_data)

# ATR monitoring
@app.route('/atr_monitor', methods=['GET', 'POST'])
@login_required
def atr_monitor():
    if request.method == 'POST':
        for symbol in futures_data:
            direction = request.form.get(f'direction_{symbol}')
            if direction:
                futures_data[symbol]['atr']['direction'] = direction
            enabled = request.form.get(f'enabled_{symbol}')
            futures_data[symbol]['atr']['monitor_enabled'] = enabled == 'on'

        return redirect(url_for('atr_monitor'))
    
    return render_template('atr_monitor.html', futures_data=futures_data)

# Pattern monitoring
@app.route('/pattern_monitor', methods=['GET', 'POST'])
@login_required
def pattern_monitor():
    if request.method == 'POST':
        for symbol in futures_data:
            direction = request.form.get(f'direction_{symbol}')
            if direction:
                futures_data[symbol]['pattern']['direction'] = direction
            enabled = request.form.get(f'enabled_{symbol}')
            futures_data[symbol]['pattern']['monitor_enabled'] = enabled == 'on'

        return redirect(url_for('pattern_monitor'))
    
    return render_template('pattern_monitor.html', futures_data=futures_data)

# Today's logs
@app.route('/today_logs', methods=['GET', 'POST'])
@login_required
def today_logs():
    if request.method == 'POST':
        logs = get_logs()
        processed_ids = request.form.getlist('processed')
        processed_ids = [int(id) for id in processed_ids]
        
        for log in logs:
            if log['id'] in processed_ids:
                log['processed'] = True
        
        save_log(logs)
        return redirect(url_for('today_logs'))
    
    logs = get_logs()
    return render_template('today_logs.html', logs=logs)

# History logs
@app.route('/history_logs', methods=['GET', 'POST'])
@login_required
def history_logs():
    if request.method == 'POST':
        date_str = request.form.get('date')
        if date_str:
            logs = get_logs(date_str)
            return render_template('history_logs.html', logs=logs, selected_date=date_str)
    
    # Get dates of all log files
    log_files = [f for f in os.listdir(LOG_DIR) if f.endswith('.json')]
    dates = [f.replace('.json', '') for f in log_files]
    dates.sort(reverse=True)  # Sort by date in descending order

    # Default to showing today's logs
    logs = get_logs()
    return render_template('history_logs.html', logs=logs, dates=dates)

# 价格监测函数
def monitor_prices():
    with data_lock:
        logs = get_logs()
        for symbol, data in futures_data.items():
            price_data = data['price']
            if price_data['monitor_enabled']:
                price_diff = abs(price_data['current_price'] - price_data['monitor_price'])
                if price_diff < MONITOR_CONFIG['price_threshold']:
                    log_entry = {
                        'id': len(logs) + 1,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'type': 'Price Monitoring',
                        'symbol': symbol,
                        'message': f"{symbol} Price monitor triggered: Current price {price_data['current_price']}, Monitor price {price_data['monitor_price']}, Price difference {price_diff:.2f}",
                        'processed': False
                    }
                    logs.append(log_entry)
        save_log(logs)

# ATR监测函数
def monitor_atr():
    with data_lock:
        logs = get_logs()
        for symbol, data in futures_data.items():
            atr_data = data['atr']
            if atr_data['monitor_enabled']:
                # 这里应该是真实的ATR监测逻辑
                # 示例使用随机触发模拟
                import random
                if random.random() < 0.1:  # 10%的触发概率
                    log_entry = {
                        'id': len(logs) + 1,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'type': 'ATR Monitoring',
                        'symbol': symbol,
                        'message': f"{symbol} ATR monitor triggered: Direction {atr_data['direction']}",
                        'processed': False
                    }
                    logs.append(log_entry)
        save_log(logs)

# 形态监测函数
def monitor_pattern():
    with data_lock:
        logs = get_logs()
        for symbol, data in futures_data.items():
            pattern_data = data['pattern']
            if pattern_data['monitor_enabled']:
                # 这里应该是真实的形态监测逻辑
                # 示例使用随机触发模拟
                import random
                if random.random() < 0.05:  # 5%的触发概率
                    log_entry = {
                        'id': len(logs) + 1,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'type': 'Pattern Monitoring',
                        'symbol': symbol,
                        'message': f"{symbol} Pattern monitor triggered: Direction {pattern_data['direction']}",
                        'processed': False
                    }
                    logs.append(log_entry)
        save_log(logs)

def update_futures_prices():
    with data_lock:
        for symbol in futures_data:
            current_price = 0 # ak
            current_price = ak.futures_zh_spot(symbol=futures_data[symbol]['symbol'], market="CF", adjust='0')['current_price'][0]
            if current_price:
                futures_data[symbol]['price']['current_price'] = float(current_price)

def periodic_task(interval):
    while True:
        update_futures_prices()
        time.sleep(interval)  # 阻塞等待下一次执行


def update_price_thread():
    # 启动线程
    interval = 10
    thread = threading.Thread(target=periodic_task, args=(interval,), daemon=True)
    thread.start()
    # print("主线程继续运行...")
    # thread.join()  # 可选：主线程阻塞等待子线程结束

if __name__ == '__main__':
    # 配置调度器
    # 监测配置
    MONITOR_CONFIG = {
        'check_interval': 60,  # 检查间隔（秒）
        'price_threshold': 2.0  # 价格差异触发阈值
    }
    scheduler.add_job(id='price_monitor', func=monitor_prices, trigger='interval', seconds=MONITOR_CONFIG['check_interval'])
    scheduler.add_job(id='atr_monitor', func=monitor_atr, trigger='interval', seconds=MONITOR_CONFIG['check_interval'])
    scheduler.add_job(id='pattern_monitor', func=monitor_pattern, trigger='interval', seconds=MONITOR_CONFIG['check_interval'])


    # 启动调度器
    scheduler.start()
    update_price_thread()


    # Load configuration from file (if exists)
    print(f"Server will run at http://{SERVER_CONFIG['host']}:{SERVER_CONFIG['port']}")
    app.run(
        host=SERVER_CONFIG['host'],
        port=SERVER_CONFIG['port'],
        debug=SERVER_CONFIG['debug']
    )    