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
# Include needed directories in sys.path.                                #
#                                                                        #
##########################################################################

import paths

# Import SimEx modules.
from TestUtilities import TestUtilities
from SimEx.Calculators.XFELPhotonSource import XFELPhotonSource
from SimEx.Calculators.XFELPhotonPropagator import XFELPhotonPropagator
from SimEx.Calculators.XMDYNDemoPhotonMatterInteractor import XMDYNDemoPhotonMatterInteractor
from SimEx.Calculators.SingFELPhotonDiffractor import SingFELPhotonDiffractor
from SimEx.Calculators.PerfectPhotonDetector import PerfectPhotonDetector
from SimEx.Calculators.S2EReconstruction import S2EReconstruction
from SimEx.PhotonExperimentSimulation.PhotonExperimentSimulation import PhotonExperimentSimulation


# Location of the FEL source file.
source_input = TestUtilities.generateTestFilePath('FELsource_out/FELsource_out_0000001.h5')

# Photon source.
photon_source = XFELPhotonSource(parameters=None, input_path=source_input, output_path='FELsource_out_0000001.h5')

# Photon propagator, default parameters.
photon_propagator = XFELPhotonPropagator(parameters=None, input_path='FELsource_out_0000001.h5', output_path='prop_out_0000001.h5')

# Photon interactor with default parameters.
photon_interactor = XMDYNDemoPhotonMatterInteractor( parameters=None,
                                                     input_path='prop_out_0000001.h5',
                                                     output_path='pmi',
                                                     sample_path=TestUtilities.generateTestFilePath('sample.h5') )

#  Diffraction with parameters.
diffraction_parameters={ 'uniform_rotation': 1,
             'calculate_Compton' : False,
             'slice_interval' : 100,
             'number_of_slices' : 2,
             'pmi_start_ID' : 1,
             'pmi_stop_ID'  : 1,
             'number_of_diffraction_patterns' : 2,
             'beam_parameter_file' : TestUtilities.generateTestFilePath('s2e.beam'),
             'beam_geometry_file' : TestUtilities.generateTestFilePath('s2e.geom'),
             }

photon_diffractor = SingFELPhotonDiffractor(
        parameters=diffraction_parameters,
        input_path='pmi',
        output_path='diffr')

# Perfect detector.
photon_detector = PerfectPhotonDetector(
        parameters = None,
        input_path='diffr',
        output_path='detector')

# Reconstruction: EMC+DM
emc_parameters = {'initial_number_of_quaternions' : 1,
                       'max_number_of_quaternions'     : 9,
                       'max_number_of_iterations'      : 100,
                       'min_error'                     : 1.0e-8,
                       'beamstop'                      : 1.0e-5,
                       'detailed_output'               : False
                       }

dm_parameters = {'number_of_trials'        : 5,
                 'number_of_iterations'    : 2,
                 'averaging_start'         : 15,
                 'leash'                   : 0.2,
                 'number_of_shrink_cycles' : 2,
                 }

reconstructor = S2EReconstruction(parameters={'EMC_Parameters' : emc_parameters, 'DM_Parameters' : dm_parameters},
                                  input_path='detector',
                                  output_path = 'recon.h5'
                                  )

# Setup the photon experiment.
pxs = PhotonExperimentSimulation(photon_source=photon_source,
                                 photon_propagator=photon_propagator,
                                 photon_interactor=photon_interactor,
                                 photon_diffractor=photon_diffractor,
                                 photon_detector=photon_detector,
                                 photon_analyzer=reconstructor,
                                 )

# Run the experiment.
pxs.run()
