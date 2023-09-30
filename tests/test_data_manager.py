import unittest
from unittest.mock import patch
from data import DataManager

class TestDataManager(unittest.TestCase):
    
    @patch('data.data_manager.yf.download')
    def test_get_candles(self, mock_download):
        # Setup
        mock_data = 'Mock Data' 
        mock_download.return_value = mock_data
        
        # Exercise
        data_manager = DataManager()
        symbol = 'AAPL'
        start_date = '2022-01-01'
        end_date = '2022-12-31'
        interval = '1d'
        
        fetched_data = data_manager.get_candles(symbol, start_date, end_date, interval)
        
        # Verify
        mock_download.assert_called_once_with(symbol, start=start_date, end=end_date, interval=interval)
        self.assertEqual(fetched_data, mock_data)

    # Additional Tests
    def test_get_candles_invalid_symbol(self):
        data_manager = DataManager()
        with self.assertRaises(ValueError):  
            data_manager.get_candles('INVALID', '2022-01-01', '2022-12-31', '1d')

    def test_get_candles_invalid_date_range(self):
        data_manager = DataManager()
        with self.assertRaises(ValueError):  
            data_manager.get_candles('AAPL', '2022-12-31', '2022-01-01', '1d')

    @patch('data.data_manager.yf.download')
    def test_get_candles_network_error(self, mock_download):
        mock_download.side_effect = Exception("Network Error")
        
        data_manager = DataManager()
        with self.assertRaises(Exception):  
            data_manager.get_candles('AAPL', '2022-01-01', '2022-12-31', '1d')

    def test_get_candles_invalid_interval(self):
        data_manager = DataManager()
        with self.assertRaises(ValueError):  
            data_manager.get_candles('AAPL', '2022-01-01', '2022-12-31', 'invalid_interval')

    @patch('data.data_manager.yf.download')
    def test_get_candles_data_integrity(self, mock_download):
        mock_data = 'Mock Data' 
        mock_download.return_value = mock_data
        
        data_manager = DataManager()
        fetched_data = data_manager.get_candles('AAPL', '2022-01-01', '2022-12-31', '1d')
        
        # Validate the integrity and format of the data.
        self.assertEqual(fetched_data, mock_data)
