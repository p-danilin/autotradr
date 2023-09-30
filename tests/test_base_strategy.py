import unittest
from strategies.base_strategy import BaseStrategy
import pandas as pd

class ConcreteStrategy(BaseStrategy):
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        # This is a mock implementation just for testing
        return data


class TestBaseStrategy(unittest.TestCase):

    def test_init(self):
        strategy = ConcreteStrategy(tickers=['AAPL'], interval='1d')
        self.assertEqual(strategy.tickers, ['AAPL'])
        self.assertEqual(strategy.interval, '1d')
        
    def test_generate_signals(self):
        strategy = ConcreteStrategy(tickers=['AAPL'], interval='1d')
        data = pd.DataFrame({'Close': [1, 2, 3]})
        self.assertTrue(strategy.generate_signals(data).equals(data))

if __name__ == '__main__':
    unittest.main()
