import pbl

import unittest

def _run_tests(suite_class_name):
     # gather all tests
    loader = unittest.TestLoader()
    suite_list = []
    for module in pbl.all_modules:
        if hasattr(module, suite_class_name):
            suite_list.append(loader.loadTestsFromTestCase(getattr(module, suite_class_name)))
    
    master_suite = unittest.TestSuite(suite_list)
    runner = unittest.TextTestRunner()
    runner.run(master_suite)


def test():
    _run_tests('Tests')

def test_hardware():
    _run_tests('HardwareTests')

