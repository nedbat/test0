# porttest2.py
from portfolio1 import Portfolio

p = Portfolio()
print "Empty portfolio cost: %s, should be 0.0" % p.cost()
p.buy("IBM", 100, 176)
print "With 100 IBM @ 176: %s, should be 17600.0" % p.cost()
p.buy("HPQ", 100, 36.15)
print "With 100 HPQ @ 36.15: %s, should be 21263.0" % p.cost()
