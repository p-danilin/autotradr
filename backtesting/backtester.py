# backtester/backtester.py
import pandas as pd

class Backtester:
    def __init__(self, strategy, initial_capital=100000):
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.position = 0
        self.last_price = 0
        self.portfolio_value = initial_capital
        self.transactions = []

    def run(self, data, transaction_cost=0.0): 
        if 'price' not in data.columns or 'positions' not in data.columns:
            raise ValueError("Data must contain 'price' and 'positions' columns.")
        
        for index, row in data.iterrows():
            position = row.get('positions', 0)
            # print(f"Date: {index}, Position: {position}, Short Avg: {row.get('short_mavg', 'N/A')}, Long Avg: {row.get('long_mavg', 'N/A')}")
            # Buy logic
            if position == 1:
                shares_to_buy = self.cash // row['price']
                if shares_to_buy > 0:
                    cost = shares_to_buy * row['price'] * (1 + transaction_cost)
                    self.position += shares_to_buy
                    self.cash -= cost
                    self.transactions.append({
                        'Date': str(index), 
                        'Type': 'BUY',
                        'Price': row['price'],
                        'Shares': shares_to_buy
                    })
            # Sell logic
            elif position == -1 and self.position > 0:
                revenue = self.position * row['price'] * (1 - transaction_cost)
                self.cash += revenue
                self.transactions.append({
                    'Date': str(index),
                    'Type': 'SELL',
                    'Price': row['price'],
                    'Shares': self.position
                })
                self.position = 0

            # Update portfolio value
            self.last_price = row['price']
            self.portfolio_value = self.cash + self.position * row['price']

    def get_results(self):
        # Calculate performance metrics and return results
        total_return = (self.portfolio_value - self.initial_capital) / self.initial_capital
        return {
            'Total Return': total_return,
            'Transactions': self.transactions,
            'Final Portfolio Value': self.cash + self.position * (self.last_price if self.position != 0 else 1),
            'Final Cash': self.cash,
            'Final Position': self.position
        }

