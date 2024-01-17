import pandas_datareader.data as web
from pandas_datareader import data
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

def backt(input_cash,input_margin,symbol,inn1,inn2):
    yf.pdr_override()
    print("backt実行")
    data_yahoo = data.get_data_yahoo(symbol, "2020-1-5", "2023-1-5")
    # 売買戦略
    class SmaCross(Strategy):
        n1 = inn1 # 短期SMA
        n2 = inn2 # 長期SMA

        def init(self):
            self.sma1 = self.I(SMA, self.data.Close, self.n1)
            self.sma2 = self.I(SMA, self.data.Close, self.n2)
        def next(self): # チャートデータの行ごとに呼び出される
            if crossover(self.sma1, self.sma2): # sma1がsma2を上回った時
                self.buy() # 買い
            elif crossover(self.sma2, self.sma1):
                self.position.close() # 売り

    # バックテストを設定
    bt = Backtest(
        data_yahoo, # チャートデータ
        SmaCross, # 売買戦略
        cash=input_cash, # 最初の所持金
        commission=0.00495, # 取引手数料
        margin=input_margin, # レバレッジ倍率の逆数（0.5で2倍レバレッジ）
        trade_on_close=True, # True：現在の終値で取引，False：次の時間の始値で取引
        exclusive_orders=True #自動でポジションをクローズ
    )

    output = bt.run() # バックテスト実行
    print(output) # 実行結果(データ)
    print(type(output))
    #bt.plot(formatter='%d %b')
    # 実行結果（グラフ）

    print("最適化後")

    #最適化
    #output2=bt.optimize(n1=range(10, 70, 5),n2=range(10, 70, 5))
    #print(output2)
    #bt.plot(formatter='%d %b')
    profit=output[4]-input_cash
    result_dict = {
    'Equity Final': round(output[4],2),
    'Return (Ann)': round(output[8],2),
    'Win Rate': round(output[18],2),
    'Profit':round(profit,2),
    'Symbol':symbol
    }

    """"
    result_list=[]
    result_list.append(result_dict)
    print(result_list)
    """
    return result_dict


