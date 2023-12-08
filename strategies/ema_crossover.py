import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas_datareader.data as web
from scipy.optimize import brute

plt.style.use("seaborn")


class EMABacktester():
    def __init__(self, symbol, EMA_S, EMA_L, start, end) -> None:
        self.symbol = symbol
        self.EMA_S = EMA_S
        self.EMA_L = EMA_L
        self.start = start
        self.end = end
        self.results = None

        self.get_data()
    
    def __repr__(self) -> str:
        pass

    def get_data(self):
        dataset = web.get_data_yahoo(self.symbol, start=self.start, end=self.end)

        dataset["returns"] = np.log(dataset["Adj Close"] / dataset["Adj Close"].shift(1))
        dataset["EMA_S"] = dataset["Adj Close"].ewm(span=self.EMA_S, min_periods=self.EMA_S).mean()
        dataset["EMA_L"] = dataset["Adj Close"].ewm(span=self.EMA_L, min_periods=self.EMA_L).mean()

        self.data = dataset

        return dataset

    def set_parameters(self, EMA_S=None, EMA_L=None):
        if EMA_S is not None:
            self.EMA_S = EMA_S
            self.data["EMA_S"] = self.data["Adj Close"].ewm(span=self.EMA_S, min_periods=self.EMA_S).mean()
        if EMA_L is not None:
            self.EMA_L = EMA_L
            self.data["EMA_L"] = self.data["Adj Close"].ewm(span=self.EMA_S, min_periods=self.EMA_S).mean()
    
    def test_strategy(self):
        data = self.data.copy().dropna()

        data["position"] = np.where(data["EMA_S"] > data["EMA_L"], 1, -1)
        data["strategy"] = data["position"].shift(1) * data["returns"]

        data.dropna()

        data["creturns"] = data["returns"].cumsum().apply(np.exp)
        data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)

        self.results = data

        perf = data["cstrategy"].iloc[-1]
        outperf = perf - data["creturns"].iloc[-1]

        return round(perf, 2), round(outperf, 2)
    
    def plot_results(self):
        if self.results is None:
            print("No results to plot yet. Run a strategy.")
        else:
            title = "{} | EMA_S = {} | EMA_L = {}".format(self.symbol, self.EMA_S, self.EMA_L)
            self.results[["creturns", "cstrategy"]].plot(title=title, figsize=(12, 8))
            plt.show()
    
    def update_and_run(self, EMA):
        self.set_parameters(int(EMA[0]), int(EMA[1]))
        return -self.test_strategy()[0]
    
    def optimize_parameters(self, EMA_S_range, EMA_L_range):
        opt = brute(self.update_and_run, (EMA_S_range, EMA_L_range), finish=None)
        return opt, -self.update_and_run(opt)

