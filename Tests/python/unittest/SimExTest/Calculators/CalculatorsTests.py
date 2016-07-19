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

import paths
import unittest

# Import classes to test.
from XFELPhotonSourceTest import XFELPhotonSourceTest
from XFELPhotonPropagatorTest import XFELPhotonPropagatorTest
from WavePropagatorTest import WavePropagatorTest
from SingFELPhotonDiffractorTest import SingFELPhotonDiffractorTest
from S2EReconstructionTest import S2EReconstructionTest

# Setup the suite.
def suite():
    suites = (
             unittest.makeSuite(XFELPhotonSourceTest,          'test'),
             unittest.makeSuite(XFELPhotonPropagatorTest,      'test'),
             unittest.makeSuite(WavePropagatorTest,            'test'),
             unittest.makeSuite(SingFELPhotonDiffractorTest,   'test'),
             unittest.makeSuite(S2EReconstructionTest,         'test'),
             )

    return unittest.TestSuite(suites)

# If called as script, run the suite.
if __name__=="__main__":
    unittest.main(defaultTest="suite")

