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

import unittest

# Import classes to test.
from .CrystFELPhotonDiffractorParametersTest import CrystFELPhotonDiffractorParametersTest
from .DMPhasingParametersTest import DMPhasingParametersTest
from .DetectorGeometryTest import DetectorGeometryTest, DetectorPanelTest
from .EMCOrientationParametersTest import EMCOrientationParametersTest
from .EstherPhotonMatterInteractorParametersTest import EstherPhotonMatterInteractorParametersTest
from .PhotonBeamParametersTest import PhotonBeamParametersTest
from .PlasmaXRTSCalculatorParametersTest import PlasmaXRTSCalculatorParametersTest
from .SingFELPhotonDiffractorParametersTest import SingFELPhotonDiffractorParametersTest
from .WavePropagatorParametersTest import WavePropagatorParametersTest
from .PhotonMatterInteractorParametersTest import PhotonMatterInteractorParametersTest
from .XCSITPhotonDetectorParametersTest import XCSITPhotonDetectorParametersTest

# Setup the suite.
def suite():
    suites = [
             unittest.makeSuite(CrystFELPhotonDiffractorParametersTest,     'test'),
             unittest.makeSuite(DetectorGeometryTest,                       'test'),
             unittest.makeSuite(DetectorPanelTest,                          'test'),
             unittest.makeSuite(PlasmaXRTSCalculatorParametersTest,         'test'),
             unittest.makeSuite(SingFELPhotonDiffractorParametersTest,      'test'),
             unittest.makeSuite(EMCOrientationParametersTest,               'test'),
             unittest.makeSuite(DMPhasingParametersTest,                    'test'),
             unittest.makeSuite(WavePropagatorParametersTest,               'test'),
             unittest.makeSuite(PhotonBeamParametersTest,                   'test'),
             unittest.makeSuite(EstherPhotonMatterInteractorParametersTest, 'test'),
             unittest.makeSuite(PhotonMatterInteractorParametersTest,       'test'),
             unittest.makeSuite(XCSITPhotonDetectorParametersTest,       'test'),
             ]

    return unittest.TestSuite(suites)

# If called as script, run the suite.
if __name__=="__main__":
    unittest.main(defaultTest="suite")
