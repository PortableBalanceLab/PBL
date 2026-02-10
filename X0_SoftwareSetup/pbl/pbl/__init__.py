# `__init__`: initialization code for the top-level `pbl` Python package.

import pbl.common
import pbl.l2
import pbl.l3
import pbl.s1
import pbl.s2
import pbl.s3
import pbl.s4

# A set of all modules that can be tested by the top-level PBL system.
all_modules = {pbl.common, pbl.l2, pbl.l3, pbl.s1, pbl.s2, pbl.s3, pbl.s4}

# Utility aliases (e.g. so that `pbl.test(all_modules)` works)
from pbl.test import test
from pbl.test import hwtest
