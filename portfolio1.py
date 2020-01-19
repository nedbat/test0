# portfolio1.py

class Portfolio:
    """A simple stock portfolio"""
    def __init__(self):
        # stocks is a list of lists:
        #   [[name, shares, price], ...]
        self.stocks = []

    def buy(self, name, shares, price):
        """Buy `name`: `shares` shares at `price`."""
        self.stocks.append([name, shares, price])

    def cost(self):
        """What was the total cost of this portfolio?"""
        amt = 0.0
        for name, shares, price in self.stocks:
            amt += shares * price
        return amt
