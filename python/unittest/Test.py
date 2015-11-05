import unittest
import sys

# Import suites to run.
from XXXTest.Calculators import CalculatorsTests
from XXXTest.Utilities import UtilitiesTests
from XXXTest.PhotonExperimentSimulation import PhotonExperimentSimulationTests

# Define the encapsulating test suite.
def suite():
    suites = [ CalculatorsTests.suite(),
               UtilitiesTests.suite(),
               PhotonExperimentSimulationTests.suite(),
             ]

    return unittest.TestSuite(suites)

# Run the top level suite and return a success status code. This enables running an automated git-bisect.
if __name__=="__main__":

    result = unittest.TextTestRunner(verbosity=2).run(suite())

    if result.wasSuccessful():
        print '---> OK <---'
        sys.exit(0)

    sys.exit(1)
