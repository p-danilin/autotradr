import yfinance as yf
import pandas as pd

class DataManager:
    """
    DataManager Class
    
    A class used to manage the acquisition of financial data using yfinance.
    
    Methods
    -------
    get_candles(ticker: str, start_date: str, end_date: str, interval: str = '15m') -> pd.DataFrame
        Fetches historical price data (OHLC) for a given ticker, date range, and interval.
    """
    
    def __init__(self):
        """
        Initializes the DataManager object.
        
        Currently, no instance variables or connections are initialized in this method.
        """
        pass
    
    def get_candles(self, ticker: str, start_date: str, end_date: str, interval: str = '15m') -> pd.DataFrame:
        """
        Fetches historical price data (OHLC) for a given ticker, date range, and interval using yfinance.
        
        Parameters:
        ticker (str): The stock symbol for which to fetch the historical price data.
        start_date (str): The start date of the data in the 'YYYY-MM-DD' format.
        end_date (str): The end date of the data in the 'YYYY-MM-DD' format.
        interval (str): The frequency of the data. Default is '15m'. Valid periods are: “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”
        
        Returns:
        pd.DataFrame: A DataFrame containing the historical price data (OHLC).
        
        Raises:
        ValueError: If no data is available for the given ticker in the specified date range or if any other error occurs while fetching the data.
        """
        
        try:
            candles = yf.download(ticker, start=start_date, end=end_date, interval=interval)
            
            if isinstance(candles, pd.DataFrame) and candles.empty:
                raise ValueError(f"No data available for {ticker} in the given date range.")
                
        except Exception as e:
            raise ValueError(str(e))
        
        return candles
