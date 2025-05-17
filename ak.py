import sys
import time
import threading
import random
import datetime
import pandas as pd
import akshare as ak
import numpy as np

from typing import List, Dict, Tuple, Optional

class ATRCalculator:
    def cal_60matr(symbol):
        df = ak.futures_zh_minute_sina(symbol=symbol, period="60")[-20:]
        df['high_low'] = df['high'] - df['low']
        df['high_close'] = np.abs(df['high'] - df['close'].shift())
        df['low_close'] = np.abs(df['low'] - df['close'].shift())
        
        df['TR'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
        period = 14
        df['ATR'] = df['TR'].rolling(window=period).mean()
        
        # atr = df[['high', 'low', 'close', 'TR', 'ATR']].tail(1)
        return df['ATR'].iloc[-1]

    def atr_cond(symbol, direction):
        atr = ATRCalculator.cal_60matr(symbol)
        data_15m = ak.futures_zh_minute_sina(symbol="RB0", period="15")[-20:]
        
        if direction == "Short":
            recent_20k_h = data_15m['high'].tail(20).max()
            cur_l = data_15m['low'].iloc[-1]
            print(recent_20k_h, cur_l)
            if (float(recent_20k_h) - float(cur_l)) > 1.3 * atr:
                return 1

        elif direction == "Long":
            recent_20k_l = data_15m['low'].tail(20).min()
            cur_h = data_15m['high'].iloc[-1]
            print(recent_20k_l, cur_h)
            if (float(cur_h) - float(recent_20k_l)) > 1.3 * atr:
                return 1
        return 0


def getRealTimeP(symbol):
    return ak.futures_zh_spot(symbol=symbol, market="CF", adjust='0')['current_price'][0]


# ATRCalculator.atr_cond("V0", "Long")

# df = ak.futures_zh_minute_sina(symbol="V0", period="60")[-20:]
# df['high_low'] = df['high'] - df['low']
# df['high_close'] = np.abs(df['high'] - df['close'].shift())
# df['low_close'] = np.abs(df['low'] - df['close'].shift())

# df['TR'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
# period = 14
# df['ATR'] = df['TR'].rolling(window=period).mean()

# # 输出结果
# atr = df[['high', 'low', 'close', 'TR', 'ATR']].tail(1)
