# test_port2.py

import unittest
from portfolio1 import Portfolio

class PortfolioTest(unittest.TestCase):
    def test_empty(self):
        p = Portfolio()
        assert p.cost() == 0.0

    def test_ibm(self):
        p = Portfolio()
        p.buy("IBM", 100, 176.48)
        assert p.cost() == 17648.0

    def test_ibm_hpq(self):
        p = Portfolio()
        p.buy("IBM", 100, 176.48)
        p.buy("HPQ", 100, 36.15)
        assert p.cost() == 21263.0
