import backtrader as bt

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.days_in_trade = 0
        self.profit_take_levels_long = 1.02  # changed to a single value
        self.profit_take_levels_short = 0.99  # changed to a single value
        self.initial_stop_loss = 0
        self.trailing_stop = 0
        self.trail_stop_activated = False
        self.risk_percent = 0.50

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        # After buy order execution
        if order.status in [order.Completed] and order.isbuy():
            self.log('BUY EXECUTED, Price: %.2f' % order.executed.price)
            self.days_in_trade = 1
            # Set initial stop loss after buy
            self.initial_stop_loss = order.executed.price * 0.95  # 5% stop loss
            # Set profit take level (can be adjusted based on your requirements)
            self.take_profit = order.executed.price * self.profit_take_levels_long

        # After sell order execution (short)
        elif order.status in [order.Completed] and order.issell():
            self.log('SELL EXECUTED, Price: %.2f' % order.executed.price)
            self.days_in_trade = 1
            # Set initial stop loss after short sell
            self.initial_stop_loss = order.executed.price * 1.05  # 5% stop loss
            # Set profit take level (can be adjusted based on your requirements)
            self.take_profit = order.executed.price * self.profit_take_levels_short

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
            if self.position:
                self.days_in_trade = 0
                self.trail_stop_activated = False

        self.order = None


    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:  # check if order is pending
            return

        risk_amount = self.broker.getvalue() * self.risk_percent
        price_difference = abs(self.dataclose[0] - (self.dataclose[0] * 0.95))  # considering 5% stop loss for both buy/sell for simplicity
        size = risk_amount / price_difference
        
        # If no open position, check the entry conditions
        if not self.position:
            # Check for long position entry (3 day buy rule)
            if self.dataclose[0] < self.dataclose[-1] and \
            self.dataclose[-1] < self.dataclose[-2]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
                self.trail_stop_activated = False

            # Check for short position entry (3 day sell rule)
            elif self.dataclose[0] > self.dataclose[-1] and \
                self.dataclose[-1] > self.dataclose[-2]:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()
                self.trail_stop_activated = False

        # Check stop loss and take profit for long positions
        if self.position.size > 0:
            if self.dataclose[0] <= self.initial_stop_loss:
                self.log('SELL CREATE due to Stop Loss, %.2f' % self.dataclose[0])
                self.order = self.sell()
            elif not self.trail_stop_activated and self.dataclose[0] >= self.take_profit:
                self.log('Trailing Stop Activated due to Take Profit, %.2f' % self.dataclose[0])
                self.trail_stop_activated = True
                self.take_profit = None  # reset take profit
            elif self.trail_stop_activated and self.dataclose[0] > self.initial_stop_loss / 0.95:
                self.initial_stop_loss = self.dataclose[0] * 0.95

        # Check stop loss and take profit for short positions
        elif self.position.size < 0:
            if self.dataclose[0] >= self.initial_stop_loss:
                self.log('BUY CREATE due to Stop Loss, %.2f' % self.dataclose[0])
                self.order = self.buy()
            elif not self.trail_stop_activated and self.dataclose[0] <= self.take_profit:
                self.log('Trailing Stop Activated due to Take Profit, %.2f' % self.dataclose[0])
                self.trail_stop_activated = True
                self.take_profit = None  # reset take profit
            elif self.trail_stop_activated and self.dataclose[0] < self.initial_stop_loss / 1.05:
                self.initial_stop_loss = self.dataclose[0] * 1.05

        # Check for exit conditions based on days in trade
        if self.position:
            if self.position.size > 0 and self.days_in_trade == 2:  # long position exit
                self.log('SELL CREATE due to 2 days in trade, %.2f' % self.dataclose[0])
                self.order = self.sell()
            elif self.position.size < 0 and self.days_in_trade == 1:  # short position exit
                self.log('BUY CREATE due to 1 day in trade, %.2f' % self.dataclose[0])
                self.order = self.buy()

            self.days_in_trade += 1