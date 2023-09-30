from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    """
    BaseStrategy Class
    
    An abstract base class to define the structure of a trading strategy.
    
    Methods
    -------
    generate_signals(self, data: pd.DataFrame) -> pd.DataFrame
        An abstract method that must be overridden by any concrete subclass to generate buy/sell signals based on the input data.
    """
    
    def __init__(self, tickers: list, interval: str):
        """
        Initializes the BaseStrategy object with a set of tickers and an interval.
        
        Parameters:
        tickers (list): A list of stock symbols (str) to be considered by the strategy.
        interval (str): The frequency of the trading signals.
        """
        self.tickers = tickers
        self.interval = interval
        
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generates trading signals based on the input data.
        
        This method must be overridden by any concrete subclass to define the logic of the trading strategy.
        
        Parameters:
        data (pd.DataFrame): A DataFrame containing the financial data needed to generate the trading signals.
        
        Returns:
        pd.DataFrame: A DataFrame containing the generated trading signals.
        """
        pass
