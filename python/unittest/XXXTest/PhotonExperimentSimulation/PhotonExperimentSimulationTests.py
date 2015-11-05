import paths
import unittest

# Import classes to test.
from PhotonExperimentSimulationTest import PhotonExperimentSimulationTest

# Setup the suite.
def suite():
    suites = (
             unittest.makeSuite(PhotonExperimentSimulationTest,    'test'),
             )

    return unittest.TestSuite(suites)

# If called as script, run the suite.
if __name__=="__main__":
    unittest.main(defaultTest="suite")

