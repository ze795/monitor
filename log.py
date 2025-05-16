import os
import json
from datetime import datetime

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