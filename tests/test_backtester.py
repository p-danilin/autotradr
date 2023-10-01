import unittest
from backtesting.backtester import Backtester
from strategies.moving_average_strategy import MovingAverageStrategy
import pandas as pd

class TestBacktester(unittest.TestCase):
    
    def setUp(self):
        self.backtester = Backtester(strategy=None, initial_capital=100)
        
    data = pd.DataFrame({
        'price': [100, 101, 102, 103, 104],
        'positions': [1, 0, -1, 0, 0]
    }, index=pd.date_range(start='2023-01-01', periods=5))
    
    def test_run_with_buy_and_sell_order(self):
        self.backtester.run(self.data)
        results = self.backtester.get_results()
        
        expected_cash = 102  # After selling the share
        expected_position = 0  # No shares, all are sold
        expected_portfolio_value = 102  # All in cash
        self.assertEqual(results['Final Cash'], expected_cash)
        self.assertEqual(results['Final Position'], expected_position)
        self.assertEqual(results['Final Portfolio Value'], expected_portfolio_value)
        
    def test_run_with_insufficient_cash(self):
        self.backtester.cash = 1
        self.backtester.run(self.data)
        results = self.backtester.get_results()
        
        expected_cash = 1  # Not enough cash to buy any share
        expected_position = 0  # No shares were bought
        expected_portfolio_value = 1  # All in cash
        self.assertEqual(results['Final Cash'], expected_cash)
        self.assertEqual(results['Final Position'], expected_position)
        self.assertEqual(results['Final Portfolio Value'], expected_portfolio_value)
        
    def test_run_with_no_position_to_sell(self):
        data_with_no_sell = self.data.copy()  # Create a copy to modify
        data_with_no_sell.at['2023-01-03', 'positions'] = 0  # No sell signal, so it's kept until the end
        
        self.backtester.run(data_with_no_sell)  # Run with the modified data
        results = self.backtester.get_results()
        
        expected_cash = 0  # All cash is used to buy 1 share
        expected_position = 1  # 1 share is kept until the end
        expected_portfolio_value = 104  # 1 share * 104 (last price)
        self.assertEqual(results['Final Cash'], expected_cash)
        self.assertEqual(results['Final Position'], expected_position)
        self.assertEqual(results['Final Portfolio Value'], expected_portfolio_value)

    def test_transactions_recorded_correctly(self):
        self.backtester.run(self.data)
        results = self.backtester.get_results()
        
        expected_transactions = [
            {'Date': 1, 'Type': 'BUY', 'Price': 100, 'Shares': 1},
            {'Date': 3, 'Type': 'SELL', 'Price': 102, 'Shares': 1}
        ]
        self.assertEqual(results['Transactions'], expected_transactions)

if __name__ == '__main__':
    unittest.main()
