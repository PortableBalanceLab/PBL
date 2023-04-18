import pbl

import unittest

def test():
    # gather all tests
    loader = unittest.TestLoader()
    suite_list = []
    for module in pbl.all_modules:
        if hasattr(module, 'Tests'):
            suite_list.append(loader.loadTestsFromTestCase(getattr(module, 'Tests')))
    
    master_suite = unittest.TestSuite(suite_list)
    runner = unittest.TextTestRunner()
    runner.run(master_suite)