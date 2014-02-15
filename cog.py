""" Cog code generation tool.
    http://nedbatchelder.com/code/cog

    Copyright 2004-2005, Ned Batchelder.
"""

import sys
from cogapp import Cog

ret = Cog().main(sys.argv)

sys.exit(ret)
