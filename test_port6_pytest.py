# test_port6_pytest.py

import pytest

from portfolio2 import Portfolio

def assert_cost_equal(p, cost):
    """Assert that `p`'s cost is equal to `cost`."""
    assert p.cost() == cost


def test_empty():
    p = Portfolio()
    assert_cost_equal(p, 0.0)

def test_buy_one_stock():
    p = Portfolio()
    p.buy("IBM", 100, 176.48)
    assert_cost_equal(p, 17648.0)

def test_buy_two_stocks():
    p = Portfolio()
    p.buy("IBM", 100, 176.48)
    p.buy("HPQ", 100, 36.15)
    assert_cost_equal(p, 21263.0)

def test_bad_input():
    p = Portfolio()
    with pytest.raises(TypeError):
        p.buy("IBM")


@pytest.fixture()
def simple_portfolio():
    p = Portfolio()
    p.buy("MSFT", 100, 27.0)
    p.buy("DELL", 100, 17.0)
    p.buy("ORCL", 100, 34.0)
    return p

def test_sell(simple_portfolio):
    simple_portfolio.sell("MSFT", 50)
    assert_cost_equal(simple_portfolio, 6450)

def test_not_enough(simple_portfolio):
    with pytest.raises(ValueError):
        simple_portfolio.sell("MSFT", 200)

def test_dont_own_it(simple_portfolio):
    with pytest.raises(ValueError):
        simple_portfolio.sell("IBM", 1)
