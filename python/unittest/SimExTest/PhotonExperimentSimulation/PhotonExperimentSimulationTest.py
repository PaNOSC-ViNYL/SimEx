""" Test module for module PhotonExperimentSimulation from SimEx
    @author : CFG
    @creation : 20151005
"""
import os, shutil
import unittest
import paths

from TestUtilities import TestUtilities
from SimEx.Calculators.XFELPhotonSource import XFELPhotonSource
from SimEx.Calculators.XFELPhotonPropagator import XFELPhotonPropagator
from SimEx.Calculators.FakePhotonMatterInteractor import FakePhotonMatterInteractor
from SimEx.Calculators.SingFELPhotonDiffractor import SingFELPhotonDiffractor
from SimEx.Calculators.PerfectPhotonDetector import PerfectPhotonDetector
from SimEx.Calculators.S2EReconstruction import S2EReconstruction

from SimEx.PhotonExperimentSimulation.PhotonExperimentSimulation import PhotonExperimentSimulation

class PhotonExperimentSimulationTest( unittest.TestCase):
    """ Test class for the PhotonExperimentSimulation class. """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile and not os.path.isdir(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir:
                shutil.rmtree(d)

    def testSimS2EWorkflow(self):
        """ Testing that a minimal workflow works. """

        source_input = TestUtilities.generateTestFilePath('FELsource_out_0000001.h5')

        photon_source = XFELPhotonSource(parameters=None, input_path=source_input, output_path='FELsource_out_0000001.h5')

        photon_propagator = XFELPhotonPropagator(parameters=None, input_path='FELsource_out_0000001.h5', output_path='prop_out_0000001.h5')
        photon_interactor = FakePhotonMatterInteractor(parameters=None, input_path='prop_out_0000001.h5', output_path='pmi_out_0000001.h5')

        diffraction_parameters={ 'number_of_uniform_rotations': 10,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameter_file' : TestUtilities.generateTestFilePath('s2e.beam'),
                     'beam_geometry_file' : TestUtilities.generateTestFilePath('s2e.geom'),
                     }

        # Construct the object.
        photon_diffractor = SingFELPhotonDiffractor(
                parameters=diffraction_parameters,
                input_path='pmi_out_0000001.h5',
                output_path='diffr_out_0000001.h5')

        photon_detector = PerfectPhotonDetector(
                parameters = None,
                input_path='diffr_out_0000001.h5',
                output_path='detector_out_0000001.h5')

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
                                          input_path='detector_out_0000001.h5',
                                          output_path = 'recon_out_0000001.h5'
                                          )

        pxs = PhotonExperimentSimulation(photon_source=photon_source,
                                         photon_propagator=photon_propagator,
                                         photon_interactor=photon_interactor,
                                         photon_diffractor=photon_diffractor,
                                         photon_detector=photon_detector,
                                         photon_analyzer=reconstructor,
                                         )

        pxs.run()

        ## Check that all output was generated.
        #expected_files = [ 'FELsource_out.h5',
                           #'prop_out.h5',
                           #'pmi',
                           #'diffr_out_0000001.h5',
                           #'diffr_out_0000002.h5',
                           #]

        #for ex in expected_files:
            #self.assertTrue (ex in os.listdir('.') )
            #self.__files_to_remove.append(ex)

        ## Check pmi output was written.
        #self.assertTrue ('pmi_out_0000001.h5' in os.listdir('pmi') )

        ## Cleanup.
        #self.__files_to_remove.append('prepHDF5.py')
        #self.__dirs_to_remove.append('pmi')

        # Cleanup.
    def testCheckInterfaceConsistency(self):
        """ Test if the check for interface consistency works correctly. """

        # Setup a minimal experiment simulation.
        source_input = TestUtilities.generateTestFilePath('FELsource_out.h5')
        diffr_input =  TestUtilities.generateTestFilePath('pmi_out.h5')
        pmi_input = TestUtilities.generateTestFilePath('prop_out.h5')
        photon_source = XFELPhotonSource(parameters=None, input_path=source_input, output_path='FELsource_out.h5')
        photon_propagator = XFELPhotonPropagator(parameters=None, input_path='FELsource_out.h5', output_path='prop_out.h5')
        photon_interactor = FakePhotonMatterInteractor(parameters=None, input_path=pmi_input, output_path='pmi_out.h5')
        photon_diffractor = SingFELPhotonDiffractor(parameters=None, input_path=diffr_input, output_path='diffr_out.h5')
        photon_detector = PerfectPhotonDetector(parameters = None, input_path='diffr_out.h5', output_path='detector_out.h5')
        photon_analyzer = OrientAndPhasePhotonAnalyzer(parameters=None, input_path='detector_out.h5', output_path='analyzer_out.h5')

        pxs = PhotonExperimentSimulation(photon_source=photon_source,
                                         photon_propagator=photon_propagator,
                                         photon_interactor=photon_interactor,
                                         photon_diffractor=photon_diffractor,
                                         photon_detector=photon_detector,
                                         photon_analyzer=photon_analyzer,
                                         )

        interfaces_are_consistent = pxs._checkInterfaceConsistency()

        self.assertTrue( interfaces_are_consistent )





if __name__ == '__main__':
    unittest.main()
