from strategies.sma_simple_crossover import SMABacktester

from database.create_database import create_database
from database.insert_strategy import insert_strategy

database_url = './database/strategies.db'

create_database(database_url)

TICKET = 'TAEE3.SA'
SMA_S = 80
SMA_L = 90

sma_backtest = SMABacktester(TICKET, SMA_S, SMA_L, '2018-01-01', '2022-12-31')

sma_backtest.optimize_parameters((1, 50, 1), (51, 250, 1))
