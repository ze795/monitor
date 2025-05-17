
from werkzeug.security import generate_password_hash

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
