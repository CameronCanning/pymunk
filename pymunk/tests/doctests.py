import doctest
import pkgutil
import sys
import unittest

import pymunk


def load_tests(loader, tests, ignore):
    for importer, modname, ispkg in pkgutil.iter_modules(pymunk.__path__):
        # try:
        tests.addTests(doctest.DocTestSuite("pymunk." + modname))

        # except Exception as e:
        #    print("Skipping " + modname, e)
    tests.addTests(doctest.DocTestSuite(pymunk))
    return tests


if __name__ == "__main__":
    print("running doctests")
    suite = unittest.TestSuite()
    load_tests(None, suite, None)
    res = unittest.TextTestRunner().run(suite)
    sys.exit(not res.wasSuccessful())
