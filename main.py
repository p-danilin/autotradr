import pandas as pd
from backtesting.backtester import Backtester
from strategies.moving_average_strategy import MovingAverageStrategy
from data.data_manager import DataManager

class Main:
    def __init__(self):
        self.data_manager = DataManager()
        self.initial_capital = 100000
    
    def load_data(self, ticker, start_date, end_date, interval='60m'):
        return self.data_manager.get_candles(ticker, start_date, end_date, interval)
    
    def optimize_strategy(self, data):
        results = [
            self.run_backtest(short, long, data.copy()) 
            for short in range(1, 20) 
            for long in range(short + 1, 21)
        ]
        return sorted(results, key=lambda x: x['result']['Final Portfolio Value'], reverse=True)
    
    def run_backtest(self, short_window, long_window, data):
        strategy = MovingAverageStrategy(tickers=['AAPL'], interval='60m', short_window=short_window, long_window=long_window)
        data_with_signals = strategy.generate_signals(data)
        backtester = Backtester(strategy=strategy, initial_capital=self.initial_capital)
        backtester.run(data_with_signals)
        return {'params': (short_window, long_window), 'result': backtester.get_results()}
    
    def print_results(self, sorted_results):
        print("Top 5 Strategies:")
        for res in sorted_results[:5]:
            print(f"Parameters: {res['params']}, Final Portfolio Value: {res['result']['Final Portfolio Value']}")
        
        print("\nBottom 5 Strategies:")
        for res in sorted_results[-5:]:
            print(f"Parameters: {res['params']}, Final Portfolio Value: {res['result']['Final Portfolio Value']}")
    
    def main(self):
        data = self.load_data('AAPL', '2023-01-01', '2023-12-31')
        sorted_results = self.optimize_strategy(data)
        self.print_results(sorted_results)
        
        # Run backtester again with best parameters
        best_params = sorted_results[0]['params']
        results = self.run_backtest(best_params[0], best_params[1], data.copy())['result']
        
        print("\nFinal Results with Best Parameters:")
        print(f"Final Portfolio Value: {results['Final Portfolio Value']}")
        
if __name__ == "__main__":
    Main().main()
