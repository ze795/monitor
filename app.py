import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Server configuration
SERVER_CONFIG = {
    'host': 'localhost',
    'port': 5000,
    'debug': True
}

# Mock user database
users = {
    'admin': generate_password_hash('admin')
}

# Mock futures data
futures_data = {
    'Rebar': {'current_price': 3800.0, 'monitor_price': 3799.0, 'monitor_enabled': False},
    'Iron Ore': {'current_price': 780.0, 'monitor_price': 778.0, 'monitor_enabled': False},
    'Coke': {'current_price': 2200.0, 'monitor_price': 2198.0, 'monitor_enabled': False},
    'Coking Coal': {'current_price': 1500.0, 'monitor_price': 1498.0, 'monitor_enabled': False}
}

# ATR monitoring data
atr_data = {
    'Rebar': {'direction': 'Long', 'monitor_enabled': False},
    'Iron Ore': {'direction': 'Short', 'monitor_enabled': False},
    'Coke': {'direction': 'Long', 'monitor_enabled': False},
    'Coking Coal': {'direction': 'Short', 'monitor_enabled': False}
}

# Pattern monitoring data
pattern_data = {
    'Rebar': {'direction': 'Long', 'monitor_enabled': False},
    'Iron Ore': {'direction': 'Short', 'monitor_enabled': False},
    'Coke': {'direction': 'Long', 'monitor_enabled': False},
    'Coking Coal': {'direction': 'Short', 'monitor_enabled': False}
}

# Log directory
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Get today's log file path
def get_today_log_path():
    today = datetime.now().strftime('%Y-%m-%d')
    return os.path.join(LOG_DIR, f'{today}.json')

# Get logs for a specific date
def get_logs(date_str=None):
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')
    log_path = os.path.join(LOG_DIR, f'{date_str}.json')
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Save logs
def save_log(logs, date_str=None):
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')
    log_path = os.path.join(LOG_DIR, f'{date_str}.json')
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

# Check login status
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# Server configuration page
@app.route('/server_config', methods=['GET', 'POST'])
@login_required
def server_config():
    if request.method == 'POST':
        SERVER_CONFIG['host'] = request.form.get('host', 'localhost')
        SERVER_CONFIG['port'] = int(request.form.get('port', 5000))
        SERVER_CONFIG['debug'] = request.form.get('debug') == 'on'
        
        # Save configuration to file
        with open('server_config.json', 'w') as f:
            json.dump(SERVER_CONFIG, f)
            
        return render_template('server_config.html', config=SERVER_CONFIG, message='Configuration saved! Restart the application to take effect.')
    
    # Load configuration from file (if exists)
    if os.path.exists('server_config.json'):
        with open('server_config.json', 'r') as f:
            config = json.load(f)
            SERVER_CONFIG.update(config)
    
    return render_template('server_config.html', config=SERVER_CONFIG)

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
    global futures_data
    if request.method == 'POST':
        for symbol in futures_data:
            price = request.form.get(f'price_{symbol}')
            if price:
                futures_data[symbol]['monitor_price'] = float(price)
            enabled = request.form.get(f'enabled_{symbol}')
            futures_data[symbol]['monitor_enabled'] = enabled == 'on'
        
        # Check price difference and add log
        for symbol, data in futures_data.items():
            if data['monitor_enabled']:
                price_diff = abs(data['current_price'] - data['monitor_price'])
                if price_diff < 2:
                    logs = get_logs()
                    log_entry = {
                        'id': len(logs) + 1,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'type': 'Price Monitoring',
                        'symbol': symbol,
                        'message': f"{symbol} Price monitor triggered: Current price {data['current_price']}, Monitor price {data['monitor_price']}, Price difference {price_diff:.2f}",
                        'processed': False
                    }
                    logs.append(log_entry)
                    save_log(logs)
        
        return redirect(url_for('price_monitor'))
    
    return render_template('price_monitor.html', futures_data=futures_data)

# ATR monitoring
@app.route('/atr_monitor', methods=['GET', 'POST'])
@login_required
def atr_monitor():
    global atr_data
    if request.method == 'POST':
        for symbol in atr_data:
            direction = request.form.get(f'direction_{symbol}')
            if direction:
                atr_data[symbol]['direction'] = direction
            enabled = request.form.get(f'enabled_{symbol}')
            atr_data[symbol]['monitor_enabled'] = enabled == 'on'
        
        # Simulate ATR monitoring logic
        for symbol, data in atr_data.items():
            if data['monitor_enabled']:
                # This is a simulated monitoring logic, to be implemented by the user in practice
                import random
                if random.random() < 0.1:  # 10% chance to trigger
                    logs = get_logs()
                    log_entry = {
                        'id': len(logs) + 1,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'type': 'ATR Monitoring',
                        'symbol': symbol,
                        'message': f"{symbol} ATR monitor triggered: Direction {data['direction']}",
                        'processed': False
                    }
                    logs.append(log_entry)
                    save_log(logs)
        
        return redirect(url_for('atr_monitor'))
    
    return render_template('atr_monitor.html', atr_data=atr_data)

# Pattern monitoring
@app.route('/pattern_monitor', methods=['GET', 'POST'])
@login_required
def pattern_monitor():
    global pattern_data
    if request.method == 'POST':
        for symbol in pattern_data:
            direction = request.form.get(f'direction_{symbol}')
            if direction:
                pattern_data[symbol]['direction'] = direction
            enabled = request.form.get(f'enabled_{symbol}')
            pattern_data[symbol]['monitor_enabled'] = enabled == 'on'
        
        # Simulate pattern monitoring logic
        for symbol, data in pattern_data.items():
            if data['monitor_enabled']:
                # This is a simulated monitoring logic, to be implemented by the user in practice
                import random
                if random.random() < 0.05:  # 5% chance to trigger
                    logs = get_logs()
                    log_entry = {
                        'id': len(logs) + 1,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'type': 'Pattern Monitoring',
                        'symbol': symbol,
                        'message': f"{symbol} Pattern monitor triggered: Direction {data['direction']}",
                        'processed': False
                    }
                    logs.append(log_entry)
                    save_log(logs)
        
        return redirect(url_for('pattern_monitor'))
    
    return render_template('pattern_monitor.html', pattern_data=pattern_data)

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

# if __name__ == '__main__':
    # # Load configuration from file (if exists)
    # if os.path.exists('server_config.json'):
    #     with open('server_config.json', 'r') as f:
    #         config = json.load(f)
    #         SERVER_CONFIG.update(config)
    
    # print(f"Server will run at http://{SERVER_CONFIG['host']}:{SERVER_CONFIG['port']}")
    # app.run(
    #     host=SERVER_CONFIG['host'],
    #     port=SERVER_CONFIG['port'],
    #     debug=SERVER_CONFIG['debug']
    # )    
if __name__ == '__main__':
    app.run(host="192.168.31.228", debug=True)    