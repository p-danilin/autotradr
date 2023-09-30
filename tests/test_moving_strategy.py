import unittest
from strategies.moving_average_strategy import MovingAverageStrategy
import pandas as pd

class TestMovingAverageStrategy(unittest.TestCase):
    
    def setUp(self):
        #sample DataFrame to run tests against
        self.data = pd.DataFrame({
            'Close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        })
        
        self.strategy = MovingAverageStrategy(tickers=['AAPL'], interval='1d', short_window=3, long_window=5)
    
    def test_generate_signals(self):
        # Run the strategy on sample data
        signals = self.strategy.generate_signals(self.data)

        expected_signals = pd.DataFrame({
            'signal': [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        }, index=signals.index) 
            
        if not signals['signal'].equals(expected_signals['signal']):
            print("Generated Signals:\n", signals['signal'])
            print("Expected Signals:\n", expected_signals['signal'])
        self.assertTrue(signals['signal'].equals(expected_signals['signal']))


    # Future test for a variety of scenarios, including edge cases...
if __name__ == '__main__':
    unittest.main()
