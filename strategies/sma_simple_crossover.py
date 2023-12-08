import pandas as ps
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brute
import yfinance as yf
import pandas_datareader.data as web

yf.pdr_override()
plt.style.use("seaborn")

from database.insert_strategy import insert_strategy

class SMABacktester():
    """ Class for the vectorized backtesting of SMA-based trading strategies.
    
    Attributes
    =========
    symbol: str
        ticket symbol with which to work with
    SMA_S: int
        time window in days for shorter SMA
    SMA_L: int
        time window in days for long SMA
    start: str
        start date for data retrieval
    end: str
        end date for data retrivel
    
    Methods
    =======
    get_data:
        retrieves and prepares the data
    
    set_parameters:
        sets one or two new SMA parameters
    
    test_strategy:
        run the backtest for the SMA-based strategy
    
    plot_results:
        plots the perfomance of the strategy compared o buy and hold
    
    update_and_run:
        updates SMA parameters and returns the negative absolute perfomance
    
    optimize_parameters:
        implements a brute force optimization for the two SMA parameters 
    """
    def __init__(self, symbol, SMA_S, SMA_L, start, end):
        self.symbol = symbol
        self.SMA_S = SMA_S
        self.SMA_L = SMA_L
        self.start = start
        self.end = end
        self.results = None
        
        self.get_data()
    
    def get_data(self):
        """ Retrieves and prepare the data
        """
        df = web.get_data_yahoo(self.symbol, start=self.start, end=self.end)
        df['returns'] = np.log(df['Adj Close'].div(df['Adj Close'].shift(1)))
        df['SMA_S'] = df['Adj Close'].rolling(self.SMA_S).mean()
        df['SMA_L'] = df['Adj Close'].rolling(self.SMA_L).mean()
        self.data = df
        return df
    
    def set_parameters(self, SMA_S = None, SMA_L = None):
        """ Update SMA parameters and resp. time series.
        """
        if SMA_S is not None:
            self.SMA_S = SMA_S
            self.data['SMA_S'] = self.data['Adj Close'].rolling(self.SMA_S).mean()
        
        if SMA_L is not None:
            self.SMA_L = SMA_L
            self.data['SMA_L'] = self.data['Adj Close'].rolling(self.SMA_L).mean()
    
    def test_strategy(self):
        """ Backtesting the trading strategy
        """
        data = self.data.copy().dropna()
        
        data['position'] = np.where(data['SMA_S'] > data['SMA_L'], 1, -1)
        data['strategy'] = data['position'].shift(1) * data['returns']

        data.dropna(inplace=True)
        
        data['creturns'] = data['returns'].cumsum().apply(np.exp)
        data['cstrategy'] = data['strategy'].cumsum().apply(np.exp)
        
        self.results = data
        
        perf = data['cstrategy'].iloc[-1]
        outperf = perf - data['creturns'].iloc[-1]
        
        # print('{} testing sma_s={} sma_l={} with perf={}'.format(self.symbol, self.SMA_S, self.SMA_L, perf))

        insert_strategy('./database/strategies.db', self.symbol, 'SMA', '{}, {}'.format(self.SMA_S, self.SMA_L), perf)

        return round(perf, 6), round(outperf, 6)
    
    def plot_results(self):
        """ Plots the cumulative perfomance of the trading strategy compared to buy and hold.
        """
        if self.results is None:
            print("No results to plot yet. Run a strategy.")
        else:
            title = "{} | SMA_S = {} | SMA_L = {}".format(self.symbol, self.SMA_S, self.SMA_L)
            self.results[['creturns', 'cstrategy']].plot(title=title, figsize=(12, 8))
            plt.show()
    
    def update_and_run(self, SMA):
        """ Updates SMA parameters and returns the negative absolute performance.
        
        Parameters:
        ==========
        SMA: tuple
            SMA parameter tuple
        """
        self.set_parameters(int(SMA[0]), int(SMA[1]))
        return -self.test_strategy()[0]
    
    def optimize_parameters(self, SMA_S_range, SMA_L_range):
        """ Finds global maximum given the SMA parameter ranges.
        
        Parameters
        ==========
        SMA_S_range, SMA_L_range: tuple
            tuples of the form (start, end, step size)
        """
        opt = brute(self.update_and_run, (SMA_S_range, SMA_L_range), finish=None)
        return opt, -self.update_and_run(opt)