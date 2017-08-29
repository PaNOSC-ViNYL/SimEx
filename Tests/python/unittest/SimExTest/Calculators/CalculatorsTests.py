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

import os
import paths
import unittest

# Import classes to test.
from XFELPhotonSourceTest import XFELPhotonSourceTest
from XFELPhotonPropagatorTest import XFELPhotonPropagatorTest
from XMDYNDemoPhotonMatterInteractorTest import XMDYNDemoPhotonMatterInteractorTest
from SingFELPhotonDiffractorTest import SingFELPhotonDiffractorTest
from CrystFELPhotonDiffractorParametersTest import CrystFELPhotonDiffractorParametersTest
from CrystFELPhotonDiffractorTest import CrystFELPhotonDiffractorTest
from S2EReconstructionTest import S2EReconstructionTest
#from GenesisPhotonSourceTest import GenesisPhotonSourceTest

is_travisCI = ("TRAVIS_BUILD_DIR" in os.environ.keys()) and (os.environ["TRAVIS_BUILD_DIR"] != "")
if not is_travisCI:
    from XCSITPhotonDetectorTest import XCSITPhotonDetectorTest
    from XCSITPhotonDetectorParametersTest import XCSITPhotonDetectorParametersTest

# Setup the suite.
def suite():
    if not is_travisCI:
        suites = (
                 unittest.makeSuite(XFELPhotonSourceTest,                   'test'),
                 unittest.makeSuite(XFELPhotonPropagatorTest,               'test'),
                 unittest.makeSuite(XMDYNDemoPhotonMatterInteractorTest,    'test'),
                 unittest.makeSuite(SingFELPhotonDiffractorTest,            'test'),
                 unittest.makeSuite(S2EReconstructionTest,                  'test'),
                 unittest.makeSuite(CrystFELPhotonDiffractorParametersTest, 'test'),
                 unittest.makeSuite(XCSITPhotonDetectorParameters,          'test'),
                 unittest.makeSuite(XCSITPhotonDetectorParametersTest,      'test'),
                 ### Disabled since CrystFEL not added to external libraries.
                 #unittest.makeSuite(CrystFELPhotonDiffractorTest,                  'test'),
                 #unittest.makeSuite(GenesisPhotonSourceTest,                'test'),
                 )
    else:
        suites = (
                 unittest.makeSuite(XFELPhotonSourceTest,                   'test'),
                 unittest.makeSuite(XFELPhotonPropagatorTest,               'test'),
                 unittest.makeSuite(XMDYNDemoPhotonMatterInteractorTest,    'test'),
                 unittest.makeSuite(SingFELPhotonDiffractorTest,            'test'),
                 unittest.makeSuite(S2EReconstructionTest,                  'test'),
                 unittest.makeSuite(CrystFELPhotonDiffractorParametersTest, 'test'),
                 )

    return unittest.TestSuite(suites)

# If called as script, run the suite.
if __name__=="__main__":
    unittest.main(defaultTest="suite")

