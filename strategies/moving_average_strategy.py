import pandas as pd
from .base_strategy import BaseStrategy
import numpy as np

class MovingAverageStrategy(BaseStrategy):
    """
    MovingAverageStrategy Class
    
    A concrete implementation of the BaseStrategy class that generates trading signals based on moving average crossovers.
    
    """
    
    def __init__(self, tickers: list, interval: str, short_window: int, long_window: int):
        """
        Initializes the MovingAverageStrategy object with a set of tickers, an interval, and window lengths for short and long moving averages.
        
        Parameters:
        tickers (list): A list of stock symbols (str) to be considered by the strategy.
        interval (str): The frequency of the trading signals.
        short_window (int): The window length for the short moving average.
        long_window (int): The window length for the long moving average.
        """
        super().__init__(tickers, interval)
        self.short_window = short_window
        self.long_window = long_window
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generates trading signals based on moving average crossovers.
        
        Parameters:
        data (pd.DataFrame): A DataFrame containing the financial data needed to generate the trading signals.
        
        Returns:
        pd.DataFrame: A DataFrame containing the generated trading signals.
        """
        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['Close']
        signals['short_mavg'] = data['Close'].rolling(window=self.short_window, min_periods=1, center=False).mean()
        signals['long_mavg'] = data['Close'].rolling(window=self.long_window, min_periods=1, center=False).mean()
        signals['signal'] = 0.0
        signals.iloc[self.short_window:, signals.columns.get_loc('signal')] = np.where(signals['short_mavg'].iloc[self.short_window:] > signals['long_mavg'].iloc[self.short_window:], 1.0, 0.0)
        signals['positions'] = signals['signal'].diff()
        
        return signals
