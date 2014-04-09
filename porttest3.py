# porttest3.py
from portfolio1 import Portfolio

p = Portfolio()
print "Empty portfolio cost: %s, should be 0.0" % p.cost()
assert p.cost() == 0.0
p.buy("IBM", 100, 176.48)
print "With 100 IBM @ 176.48: %s, should be 17648.0" % p.cost()
assert p.cost() == 17648.0
p.buy("HPQ", 100, 36.15)
print "With 100 HPQ @ 36.15: %s, should be 21263.0" % p.cost()
assert p.cost() == 21215.0
