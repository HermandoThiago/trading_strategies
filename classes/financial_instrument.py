import yfinance as yf
import pandas_datareader.data as web
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

yf.pdr_override()
plt.style.use("seaborn")

class FinancialInstrument():
    """" Class for analyse financial instruments.

    Attributes
    ==========
    symbol: str
        ticket symbol with which to work
    start: str
        start date for data retrieval
    end: str
        end date fot data retrieval

    """
    def __init__(self, symbol, start, end):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.get_data()
    
    def get_data(self):
        """ Retrieves the data
        """
        df = web.get_data_yahoo(self.symbol, start=self.start, end=self.end)
        self.data = df

        return df

    def plot_price(self):
        """ Plot price the stock
        """
        self.data['Adj Close'].plot(title=f'{self.symbol} {self.start} | {self.end}', figsize=(20, 10))
        plt.show()
    
    def plot_returns(self):
        """ Plot returns the stock
        """
        df = self.data
        df['returns'] = np.log(df['Adj Close'].div(df['Adj Close'].shift(1)))
        self.data = df
        self.data['returns'].plot(title=f'{self.symbol} returns', figsize=(20, 10))
        plt.show()
