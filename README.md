# Autotradr

Autotradr is a Python-based project aimed at automating trading strategies for stocks. It allows users to backtest different trading strategies using historical price data and helps evaluate the performance of these strategies over a specified period.

## Overview

This project is structured into distinct modules, each responsible for a specific function:

- **Data Manager**: Handles the acquisition and management of historical stock price data.
- **Strategies**: Houses the trading strategies. Currently, a Moving Average Crossover strategy is implemented.
- **Backtester**: Enables the backtesting of various trading strategies with historical price data, assessing the strategies' performance before real-world deployment.

## Installation

To get started with Autotradr, follow these steps:

1. **Clone the Repository**
   ```sh
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**
   ```sh
   cd autotradr
   ```

3. **Install the Required Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Configure the Project Settings** in the `config.py` file, specifying parameters like stock tickers and date ranges.
   
2. **Run the Main File** by navigating to the project directory and executing the following command:
   ```sh
   python3 main.py
   ```

3. **Backtesting Results**: After running the main file, the project will backtest the configured strategies and display the results, including total returns and transaction details.

4. **Modify or Implement Strategies**: Users can modify existing strategies or add new ones in the `strategies` directory.

## Notes

- Keep sensitive information such as API keys secure. Prefer using environment variables or other secure means to handle such data.
- To enable real trading, integration with a brokerage API and implementation of order execution logic are required, which are currently not included in this project.

## Disclaimer

This project is intended for educational purposes only and should not be construed as financial advice. Users are solely responsible for their trading decisions and the potential loss incurred from using this software. Trading stocks and other financial instruments involve risks, so trade responsibly.
