##########################################################################
#                                                                        #
# Copyright (C) 2015-2018 Carsten Fortmann-Grote                         #
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
import unittest

from TestUtilities.TestUtilities import runs_on_travisCI

# Import classes to test.
from .CrystFELPhotonDiffractorTest import CrystFELPhotonDiffractorTest
from .FEFFPhotonMatterInteractorTest import FEFFPhotonMatterInteractorParametersTest
from .FEFFPhotonMatterInteractorTest import FEFFPhotonMatterInteractorTest
from .GenesisPhotonSourceTest import GenesisPhotonSourceTest
from .PlasmaXRTSCalculatorTest import PlasmaXRTSCalculatorTest
from .S2EReconstructionTest import S2EReconstructionTest
from .SingFELPhotonDiffractorTest import SingFELPhotonDiffractorTest
from .XCSITPhotonDetectorTest import XCSITPhotonDetectorTest
from .XFELPhotonPropagatorTest import XFELPhotonPropagatorTest
from .XFELPhotonSourceTest import XFELPhotonSourceTest
from .XMDYNDemoPhotonMatterInteractorTest import XMDYNDemoPhotonMatterInteractorTest
from .XMDYNPhotonMatterInteractorTest import XMDYNPhotonMatterInteractorTest
from .EstherPhotonMatterInteractorTest import EstherPhotonMatterInteractorTest

# Setup the suite.
def suite():
    suites = [
             unittest.makeSuite(CrystFELPhotonDiffractorTest,               'test'),
             unittest.makeSuite(FEFFPhotonMatterInteractorParametersTest,   'test'),
             unittest.makeSuite(FEFFPhotonMatterInteractorTest,             'test'),
             unittest.makeSuite(S2EReconstructionTest,                      'test'),
             unittest.makeSuite(SingFELPhotonDiffractorTest,                'test'),
             unittest.makeSuite(XFELPhotonPropagatorTest,                   'test'),
             unittest.makeSuite(XFELPhotonSourceTest,                       'test'),
             unittest.makeSuite(XMDYNDemoPhotonMatterInteractorTest,        'test'),
             unittest.makeSuite(XMDYNPhotonMatterInteractorTest,            'test'),
             ]

    if not runs_on_travisCI():
        suites.append(unittest.makeSuite(GenesisPhotonSourceTest,           'test'))
        suites.append(unittest.makeSuite(PlasmaXRTSCalculatorTest,          'test'))
        suites.append(unittest.makeSuite(XCSITPhotonDetectorTest,           'test'))
        suites.append(unittest.makeSuite(EstherPhotonMatterInteractorTest,  'test'))

    return unittest.TestSuite(suites)

# If called as script, run the suite.
if __name__=="__main__":
    unittest.main(defaultTest="suite")

