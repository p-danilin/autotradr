import pandas as pd
from backtesting.backtester import Backtester
from strategies.moving_average_strategy import MovingAverageStrategy
from data.data_manager import DataManager

def load_data():
    data_manager = DataManager()
    data = data_manager.get_candles('AAPL', '2023-01-01', '2023-12-31', interval='60m')
    
    strategy = MovingAverageStrategy(tickers=['AAPL'], interval='1d', short_window=2, long_window=3)
    data_with_signals = strategy.generate_signals(data)
    
    return data_with_signals


def optimize_strategy(data):
    best_result = None
    best_params = None
    
    for short_window in range(1, 20):
        for long_window in range(short_window + 1, 21):  
            strategy = MovingAverageStrategy(tickers=['AAPL'], interval='1d', short_window=short_window, long_window=long_window)
            backtester = Backtester(strategy=strategy, initial_capital=100)
            backtester.run(data)
            result = backtester.get_results()

            if best_result is None or result['Final Portfolio Value'] > best_result['Final Portfolio Value']:
                best_result = result
                best_params = (short_window, long_window)

    return best_result, best_params


def main():
    data_with_signals = load_data()
    
    best_result, best_params = optimize_strategy(data_with_signals)
    
    print(f"Best Parameters: {best_params}")
    print(f"Best Result: {best_result}")

    strategy = MovingAverageStrategy(tickers=['AAPL'], interval='1d', short_window=best_params[0], long_window=best_params[1])
    backtester = Backtester(strategy=strategy, initial_capital=100)
    backtester.run(data_with_signals)
    results = backtester.get_results()

    print("Final Results with Best Parameters:")
    print(results)

if __name__ == "__main__":
    main()
