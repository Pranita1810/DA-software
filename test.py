"""Compatibility test entry point.

Prefer `python -m unittest discover -s tests` for normal test runs.
"""

import sys
import unittest


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
