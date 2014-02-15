# test_port5.py

import unittest
from portfolio2 import Portfolio

class PortfolioTest(unittest.TestCase):
    def test_empty(self):
        p = Portfolio()
        self.assertEqual(p.cost(), 0.0)

    def test_ibm(self):
        p = Portfolio()
        p.buy("IBM", 100, 176.48)
        self.assertEqual(p.cost(), 17648.0)

    def test_ibm_hpq(self):
        p = Portfolio()
        p.buy("IBM", 100, 176.48)
        p.buy("HPQ", 100, 36.15)
        self.assertEqual(p.cost(), 21263.0)

    def test_bad_input(self):
        p = Portfolio()
        self.assertRaises(TypeError, p.buy, "IBM")

class PortfolioSellTest(unittest.TestCase):
    def test_sell(self):
        p = Portfolio()
        p.buy("MSFT", 100, 27.0)
        p.buy("DELL", 100, 17.0)
        p.buy("ORCL", 100, 34.0)
        p.sell("MSFT", 50)
        self.assertEqual(p.cost(), 6450)

    def test_not_enough(self):
        p = Portfolio()
        p.buy("MSFT", 100, 27.0)
        p.buy("DELL", 100, 17.0)
        p.buy("ORCL", 100, 34.0)
        with self.assertRaises(ValueError):
            p.sell("MSFT", 200)

    def test_dont_own_it(self):
        p = Portfolio()
        p.buy("MSFT", 100, 27.0)
        p.buy("DELL", 100, 17.0)
        p.buy("ORCL", 100, 34.0)
        with self.assertRaises(ValueError):
            p.sell("IBM", 1)

    
if __name__ == '__main__':
    unittest.main()
