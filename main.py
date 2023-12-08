from strategies.sma_simple_crossover import SMABacktester
from strategies.ema_crossover import EMABacktester

from database.create_database import create_database

database_url = './database/strategies.db'

create_database(database_url)

TICKET = 'VALE3.SA'

EMA_S = 80
EMA_L = 90

tester = EMABacktester(TICKET, EMA_S, EMA_L, "2017-01-01", "2022-12-31")

tester.test_strategy()

opt, perf = tester.optimize_parameters((1, 100, 1), (101, 250, 1))

tester.plot_results()
