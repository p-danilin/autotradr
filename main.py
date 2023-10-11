from backtesting.backtester import Backtester
import config  # assuming you have configurations here

def main():
    backtester = Backtester(config.start_date, config.end_date, config.tickers)
    backtester.run()

if __name__ == '__main__':
    main()
