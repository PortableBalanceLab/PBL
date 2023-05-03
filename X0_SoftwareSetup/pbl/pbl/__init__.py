import pbl.common
import pbl.l2
import pbl.l3
import pbl.s1
import pbl.s2
import pbl.s3
import pbl.s4

# all modules that should be configured, installed, and tested
all_modules = {pbl.common, pbl.l2, pbl.l3, pbl.s1, pbl.s2, pbl.s3, pbl.s4}

# so that callers can just write `pbl.install(modules)`
from pbl.install import install
