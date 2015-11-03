import paths
import unittest

from AbstractBaseCalculatorTest import AbstractBaseCalculatorTest
from AbstractPhotonSourceTest import AbstractPhotonSourceTest
from AbstractPhotonPropagatorTest import AbstractPhotonPropagatorTest
from AbstractPhotonInteractorTest import AbstractPhotonInteractorTest
from AbstractPhotonDiffractorTest import AbstractPhotonDiffractorTest
from AbstractPhotonDetectorTest import AbstractPhotonDetectorTest

def suite():
    suites = (
             unittest.makeSuite(AbstractBaseCalculatorTest,    'test'),
             unittest.makeSuite(AbstractPhotonSourceTest,      'test'),
             unittest.makeSuite(AbstractPhotonPropagatorTest,  'test'),
             unittest.makeSuite(AbstractPhotonInteractorTest,  'test'),
             unittest.makeSuite(AbstractPhotonDiffractorTest,  'test'),
             unittest.makeSuite(AbstractPhotonDetectorTest,    'test'),
             )
    # If the unittest are run under extensive mode, enable these tests as well.
    return unittest.TestSuite(suites)
if __name__=="__main__":
    unittest.main(defaultTest="suite")

