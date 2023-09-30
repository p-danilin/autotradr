import unittest
from backtesting.backtester import Backtester
from strategies.moving_average_strategy import MovingAverageStrategy
import pandas as pd

class TestBacktester(unittest.TestCase):
    
    def setUp(self):
        self.strategy = MovingAverageStrategy(tickers=['AAPL'], interval='1d', short_window=2, long_window=3)
        self.backtester = Backtester(strategy=self.strategy, initial_capital=100)
        
        # Create a simple DataFrame with price data and precomputed buy/sell signals.
    data = pd.DataFrame({
        'price': [100, 101, 102, 103, 104],
        'positions': [1, 0, -1, 1, 0]
    }, index=pd.date_range(start='2023-01-01', periods=5))


    def test_buy_order(self):
        self.backtester.run(self.data)
        results = self.backtester.get_results()
        
        # Assuming transaction costs are not included
        expected_cash = 100 - (100 * 1 * (1 + 0.001))  # Started with 100, bought one share at price 2
        expected_position = 1  # One share bought
        expected_portfolio_value = 103  # 98 cash + 1 share * price 5
        
        self.assertEqual(results['Final Cash'], expected_cash)
        self.assertEqual(results['Final Position'], expected_position)
        self.assertEqual(results['Final Portfolio Value'], expected_portfolio_value)
        
    def test_sell_order(self):
        self.backtester.run(self.data)
        results = self.backtester.get_results()
        
        # Assuming transaction costs are not included
        expected_cash = (102 * 1 * (1 - 0.001))  # Sold one share at price 4
        expected_position = 0  # All shares sold
        expected_portfolio_value = 102  # All in cash
        
        self.assertEqual(results['Final Cash'], expected_cash)
        self.assertEqual(results['Final Position'], expected_position)
        self.assertEqual(results['Final Portfolio Value'], expected_portfolio_value)
        
    def test_insufficient_cash(self):
        self.backtester.cash = 1  # Set cash to an amount insufficient to buy a share
        self.backtester.run(self.data)
        results = self.backtester.get_results()
        
        expected_cash = 1  # No share bought, so cash remains the same
        expected_position = 0  # No share bought
        expected_portfolio_value = 1  # All in cash
        
        self.assertEqual(results['Final Cash'], expected_cash)
        self.assertEqual(results['Final Position'], expected_position)
        self.assertEqual(results['Final Portfolio Value'], expected_portfolio_value)
        
    def test_no_position_to_sell(self):
        self.data.at[3, 'signal'] = -1  # Change to sell signal when no position is held
        self.backtester.run(self.data)
        results = self.backtester.get_results()
        
        expected_cash = 100  # No share sold, so cash remains the same
        expected_position = 0  # No position to sell
        expected_portfolio_value = 100  # All in cash
        
        self.assertEqual(results['Final Cash'], expected_cash)
        self.assertEqual(results['Final Position'], expected_position)
        self.assertEqual(results['Final Portfolio Value'], expected_portfolio_value)
        
    def test_correct_transactions_recorded(self):
        self.backtester.run(self.data)
        results = self.backtester.get_results()
        
        # Check if transactions are recorded correctly
        expected_transactions = [
            {'Date': 1, 'Type': 'BUY', 'Price': 100, 'Shares': 1},
            {'Date': 3, 'Type': 'SELL', 'Price': 102, 'Shares': 1}
        ]
        
        self.assertEqual(results['Transactions'], expected_transactions)

if __name__ == '__main__':
    unittest.main()
