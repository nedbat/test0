# test_port8.py

import unittest
from portfolio3 import Portfolio
import portfolio3
from cStringIO import StringIO

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
    def setUp(self):
        self.p = Portfolio()
        self.p.buy("MSFT", 100, 27.0)
        self.p.buy("DELL", 100, 17.0)
        self.p.buy("ORCL", 100, 34.0)

    def test_sell(self):
        self.p.sell("MSFT", 50)
        self.assertEqual(self.p.cost(), 6450)

    def test_not_enough(self):
        with self.assertRaises(ValueError):
            self.p.sell("MSFT", 200)

    def test_dont_own_it(self):
        with self.assertRaises(ValueError):
            self.p.sell("IBM", 1)

#(((fake)))
# A simple fake for urllib that implements only one method,
# and is only good for one request.  You can make this much
# more complex for your own needs.
class FakeUrllib(object):
    """An object that can stand in for the urllib module."""
    def urlopen(self, url):
        """A stub urllib.urlopen() implementation."""
        return StringIO('"IBM",140\n"HPQ",32\n')

class PortfolioValueTest(unittest.TestCase):
    def setUp(self):
        self.old_urllib = portfolio3.urllib
        portfolio3.urllib = FakeUrllib()

        self.p = Portfolio()
        self.p.buy("IBM", 100, 120.0)
        self.p.buy("HPQ", 100, 30.0)

    def tearDown(self):
        portfolio3.urllib = self.old_urllib

    def test_value(self):
        self.assertEqual(self.p.value(), 17200)
#(((end)))

if __name__ == '__main__':
    unittest.main()
