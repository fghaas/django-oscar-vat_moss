#!/usr/bin/env python
import sys
import os
from coverage import coverage
from optparse import OptionParser

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")

from django_nose import NoseTestSuiteRunner

def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    c = coverage(source=['oscar_vat_moss'], omit=['*migrations*', '*tests*'],
                 auto_data=True)
    c.start()
    num_failures = test_runner.run_tests(test_args)
    c.stop()

    if num_failures > 0:
        sys.exit(num_failures)


if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    run_tests(*args)
