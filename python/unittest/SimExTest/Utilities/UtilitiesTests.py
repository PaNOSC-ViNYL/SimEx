import paths
import unittest

# Import classes to test.
from EntityChecksTest import EntityChecksTest

# Setup the suite.
def suite():
    suites = (
             unittest.makeSuite(EntityChecksTest,    'test'),
             )

    return unittest.TestSuite(suites)

# If called as script, run the suite.
if __name__=="__main__":
    unittest.main(defaultTest="suite")

