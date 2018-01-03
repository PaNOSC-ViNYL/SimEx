##########################################################################
#                                                                        #
# Copyright (C) 2015 Carsten Fortmann-Grote                              #
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

from . import paths
import unittest

# Import classes to test.
from .AbstractBaseCalculatorTest import AbstractBaseCalculatorTest
from .AbstractBaseCalculatorTest import AbstractCalculatorParametersTest
from .AbstractPhotonSourceTest import AbstractPhotonSourceTest
from .AbstractPhotonPropagatorTest import AbstractPhotonPropagatorTest
from .AbstractPhotonInteractorTest import AbstractPhotonInteractorTest
from .AbstractPhotonDiffractorTest import AbstractPhotonDiffractorTest
from .AbstractPhotonDetectorTest import AbstractPhotonDetectorTest

# Setup the suite.
def suite():
    suites = (
             unittest.makeSuite(AbstractBaseCalculatorTest,          'test'),
             unittest.makeSuite(AbstractCalculatorParametersTest,    'test'),
             unittest.makeSuite(AbstractPhotonSourceTest,            'test'),
             unittest.makeSuite(AbstractPhotonPropagatorTest,        'test'),
             unittest.makeSuite(AbstractPhotonInteractorTest,        'test'),
             unittest.makeSuite(AbstractPhotonDiffractorTest,        'test'),
             unittest.makeSuite(AbstractPhotonDetectorTest,          'test'),
             )

    return unittest.TestSuite(suites)

# If called as script, run the suite.
if __name__=="__main__":
    unittest.main(defaultTest="suite")

