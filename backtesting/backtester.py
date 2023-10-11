import datetime
from data.data_manager import fetch_data
from strategies.mean_reversion_strategy import TestStrategy
import backtrader as bt

class Backtester:
    def __init__(self, start_date, end_date, tickers):
        self.start_date = start_date
        self.end_date = end_date
        self.tickers = tickers

    def run(self):
        class PandasData(bt.feeds.PandasData):
            pass

        for ticker in self.tickers:
            print("Running for ticker:", ticker)

            cerebro = bt.Cerebro()

            cerebro.addstrategy(TestStrategy)

            df = fetch_data(ticker, self.start_date, self.end_date)

            data = PandasData(dataname=df, 
                              fromdate=self.start_date,
                              todate=self.end_date)

            cerebro.adddata(data)

            cerebro.broker.setcash(100000.0)

            cerebro.addsizer(bt.sizers.FixedSize, stake=10)

            cerebro.broker.setcommission(commission=0.0)

            print('Starting Portfolio Value for %s: %.2f' % (ticker, cerebro.broker.getvalue()))

            cerebro.run()

            print('Final Portfolio Value for %s: %.2f' % (ticker, cerebro.broker.getvalue()))

            cerebro.plot()
