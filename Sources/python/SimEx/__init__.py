##########################################################################
#                                                                        #
# Copyright (C) 2015-2020 Carsten Fortmann-Grote                         #
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
# Include needed directories in sys.path.                                #
#                                                                        #
##########################################################################

# Set up physical units system.
# All units are defined in SimEx.Utilities.Units.
# NOTE: There must be no other import of pint submodules.
from pint import UnitRegistry
ureg = UnitRegistry()
PhysicalQuantity = ureg.Quantity


from .version import __version__

from .Analysis.DiffractionAnalysis import DiffractionAnalysis
from .Analysis.XFELPhotonAnalysis import XFELPhotonAnalysis

from .AbstractBaseClass import AbstractBaseClass
from .Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from .Calculators.CrystFELPhotonDiffractor import CrystFELPhotonDiffractor
from .Calculators.DMPhasing import DMPhasing
from .Calculators.EMCCaseGenerator import EMCCaseGenerator
from .Calculators.EMCOrientation import EMCOrientation
from .Calculators.EstherPhotonMatterInteractor import EstherPhotonMatterInteractor
from .Calculators.GaussianPhotonSource import GaussianPhotonSource
from .Calculators.GenesisPhotonSource import GenesisPhotonSource
from .Calculators.IdealPhotonDetector import IdealPhotonDetector
from .Calculators.PlasmaXRTSCalculator import PlasmaXRTSCalculator
from .Calculators.S2EReconstruction import S2EReconstruction
from .Calculators.SingFELPhotonDiffractor import SingFELPhotonDiffractor
from .Calculators.XFELPhotonPropagator import XFELPhotonPropagator
from .Calculators.XFELPhotonSource import XFELPhotonSource
from .Calculators.XMDYNDemoPhotonMatterInteractor import XMDYNDemoPhotonMatterInteractor
from .Calculators.XMDYNPhotonMatterInteractor import XMDYNPhotonMatterInteractor

from .Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from .Parameters.CrystFELPhotonDiffractorParameters import CrystFELPhotonDiffractorParameters
from .Parameters.DMPhasingParameters import DMPhasingParameters
from .Parameters.DetectorGeometry import DetectorGeometry
from .Parameters.DetectorGeometry import DetectorPanel
from .Parameters.EMCOrientationParameters import EMCOrientationParameters
from .Parameters.EstherPhotonMatterInteractorParameters import EstherPhotonMatterInteractorParameters
from .Parameters.GaussWavefrontParameters import GaussWavefrontParameters
from .Parameters.PhotonBeamParameters import PhotonBeamParameters
from .Parameters.PlasmaXRTSCalculatorParameters import PlasmaXRTSCalculatorParameters
from .Parameters.SingFELPhotonDiffractorParameters import SingFELPhotonDiffractorParameters
from .Parameters.WavePropagatorParameters import WavePropagatorParameters
from .PhotonExperimentSimulation.PhotonExperimentSimulation import PhotonExperimentSimulation
from .PhotonExperimentSimulation.EstherExperiment import EstherExperiment

from . import Utilities
from .Utilities.Units import *

