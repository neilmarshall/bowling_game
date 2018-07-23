import doctest
import unittest

import main

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(main))
    return tests

