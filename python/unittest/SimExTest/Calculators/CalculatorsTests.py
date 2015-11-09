import paths
import unittest

# Import classes to test.
from AbstractBaseCalculatorTest import AbstractBaseCalculatorTest
from AbstractPhotonSourceTest import AbstractPhotonSourceTest
from AbstractPhotonPropagatorTest import AbstractPhotonPropagatorTest
from AbstractPhotonInteractorTest import AbstractPhotonInteractorTest
from AbstractPhotonDiffractorTest import AbstractPhotonDiffractorTest
from AbstractPhotonDetectorTest import AbstractPhotonDetectorTest

from XFELPhotonSourceTest import XFELPhotonSourceTest
from XFELPhotonPropagatorTest import XFELPhotonPropagatorTest

# Setup the suite.
def suite():
    suites = (
             unittest.makeSuite(AbstractBaseCalculatorTest,    'test'),
             unittest.makeSuite(AbstractPhotonSourceTest,      'test'),
             unittest.makeSuite(AbstractPhotonPropagatorTest,  'test'),
             #unittest.makeSuite(AbstractPhotonInteractorTest,  'test'),
             #unittest.makeSuite(AbstractPhotonDiffractorTest,  'test'),
             #unittest.makeSuite(AbstractPhotonDetectorTest,    'test'),
             unittest.makeSuite(XFELPhotonSourceTest,          'test'),
             unittest.makeSuite(XFELPhotonPropagatorTest,      'test'),
             )

    return unittest.TestSuite(suites)

# If called as script, run the suite.
if __name__=="__main__":
    unittest.main(defaultTest="suite")

