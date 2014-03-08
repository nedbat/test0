# portfolio3.py

import urllib
import csv


class Portfolio(object):
    """A simple stock portfolio

    >>> p = Portfolio()
    >>> p.cost()
    0.0

    >>> p.buy("IBM", 100, 176.48)
    >>> p.cost()
    17648.0

    >>> p.buy("HPQ", 100, 36.15)
    >>> p.cost()
    21263.0

    """
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

    def sell(self, name, shares):
        """Sell some number of shares of `name`."""
        for holding in self.stocks:
            if holding[0] == name:
                if holding[1] < shares:
                    raise ValueError("Not enough shares")
                holding[1] -= shares
                break
        else:
            raise ValueError("You don't own that stock")

    #(((value)))
    def current_prices(self):
        """Return a dict mapping names to current prices."""
        # http://download.finance.yahoo.com/d/quotes.csv?f=sl1&s=ibm,hpq
        # returns comma-separated values:
        #   "IBM",174.23
        #   "HPQ",35.13
        url = "http://download.finance.yahoo.com/d/quotes.csv?f=sl1&s="
        names = [name for name, shares, price in self.stocks]
        url += ",".join(sorted(names))
        data = urllib.urlopen(url)
        prices = { sym: float(last) for sym, last in csv.reader(data) }
        return prices

    def value(self):
        """Return the current value of the portfolio."""
        prices = self.current_prices()
        total = 0.0
        for name, shares, price in self.stocks:
            total += shares * prices[name]
        return total
    #(((end)))
