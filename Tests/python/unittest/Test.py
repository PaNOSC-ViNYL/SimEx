##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 Carsten Fortmann-Grote                         #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This file is part of simex_platform.                                   #
# simex_platform is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# simex_platform is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

import unittest
import os, sys

# Import suites to run.
from SimExTest.Calculators import CalculatorsTests
from SimExTest.Calculators import AbstractCalculatorsTests
from SimExTest.Utilities import UtilitiesTests
from SimExTest.Parameters import ParametersTests
from SimExTest.PhotonExperimentSimulation import PhotonExperimentSimulationTests

# Are we running on CI server?
is_travisCI = ("TRAVIS_BUILD_DIR" in os.environ.keys()) and (os.environ["TRAVIS_BUILD_DIR"] != "")


# Define the test suite.
def suite():
    suites = [
               AbstractCalculatorsTests.suite(),
               CalculatorsTests.suite(),
               UtilitiesTests.suite(),
               ParametersTests.suite(),
             ]

    # Append if NOT on CI server.
    if not is_travisCI:
        suites.append(PhotonExperimentSimulationTests.suite())

    return unittest.TestSuite(suites)

# Run the top level suite and return a success status code. This enables running an automated git-bisect.
if __name__=="__main__":

    result = unittest.TextTestRunner(verbosity=2).run(suite())

    if result.wasSuccessful():
        print '---> OK <---'
        sys.exit(0)

    sys.exit(1)
