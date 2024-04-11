import pbl

import unittest

def _run_tests(modules, suite_classname):
     # gather all tests
    loader = unittest.TestLoader()
    suite_list = []
    for module in modules:
        if hasattr(module, suite_classname):
            suite_list.append(loader.loadTestsFromTestCase(getattr(module, suite_classname)))
    
    master_suite = unittest.TestSuite(suite_list)
    runner = unittest.TextTestRunner()
    runner.run(master_suite)

def test(modules=pbl.all_modules):
    _run_tests(modules, suite_classname='Tests')

def hwtest(modules=pbl.all_modules):
    _run_tests(modules, suite_classname='HardwareTests')

