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
from SimEx.Calculators.XMDYNDemoPhotonMatterInteractor import XMDYNDemoPhotonMatterInteractor
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

        self.__sample_path = TestUtilities.generateTestFilePath('sample.h5')

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f) or os.path.islink(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

    def testConstruction(self):
        """ Test the default constructor of this class. """
        # Setup a minimal experiment simulation.
        source_input = TestUtilities.generateTestFilePath('FELsource_out.h5')
        diffr_input =  TestUtilities.generateTestFilePath('pmi_out.h5')
        pmi_input = TestUtilities.generateTestFilePath('prop_out.h5')
        photon_source = XFELPhotonSource(parameters=None, input_path=source_input, output_path='FELsource_out.h5')
        photon_propagator = XFELPhotonPropagator(parameters=None, input_path='FELsource_out.h5', output_path='prop_out.h5')
        photon_interactor = XMDYNDemoPhotonMatterInteractor(parameters=None,
                                                            input_path=pmi_input,
                                                            output_path='pmi_out.h5',
                                                            sample_path=self.__sample_path
                                                            )

        diffraction_parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameter_file' : TestUtilities.generateTestFilePath('s2e.beam'),
                     'beam_geometry_file' : TestUtilities.generateTestFilePath('s2e.geom'),
                   }
        photon_diffractor = SingFELPhotonDiffractor(parameters=diffraction_parameters, input_path=diffr_input, output_path='diffr_out.h5')

        photon_detector = PerfectPhotonDetector(parameters = None, input_path='diffr_out.h5', output_path='detector_out.h5')
        photon_analyzer = S2EReconstruction(parameters=None, input_path='detector_out.h5', output_path='analyzer_out.h5')

        pxs = PhotonExperimentSimulation(photon_source=photon_source,
                                         photon_propagator=photon_propagator,
                                         photon_interactor=photon_interactor,
                                         photon_diffractor=photon_diffractor,
                                         photon_detector=photon_detector,
                                         photon_analyzer=photon_analyzer,
                                         )

        # Check instance.
        self.assertIsInstance( pxs, PhotonExperimentSimulation )

    def testCalculatorQueries(self):
        """ Test that the calculator queries return the correct calculators. """
        # Setup a minimal experiment simulation.
        source_input = TestUtilities.generateTestFilePath('FELsource_out.h5')
        diffr_input =  TestUtilities.generateTestFilePath('pmi_out.h5')
        pmi_input = TestUtilities.generateTestFilePath('prop_out.h5')
        photon_source = XFELPhotonSource(parameters=None, input_path=source_input, output_path='FELsource_out.h5')
        photon_propagator = XFELPhotonPropagator(parameters=None, input_path='FELsource_out.h5', output_path='prop_out.h5')
        photon_interactor = XMDYNDemoPhotonMatterInteractor(parameters=None,
                                                            input_path=pmi_input,
                                                            output_path='pmi_out.h5',
                                                            sample_path=self.__sample_path
                                                            )

        diffraction_parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameter_file' : TestUtilities.generateTestFilePath('s2e.beam'),
                     'beam_geometry_file' : TestUtilities.generateTestFilePath('s2e.geom'),
                   }
        photon_diffractor = SingFELPhotonDiffractor(parameters=diffraction_parameters, input_path=diffr_input, output_path='diffr_out.h5')

        photon_detector = PerfectPhotonDetector(parameters = None, input_path='diffr_out.h5', output_path='detector_out.h5')
        photon_analyzer = S2EReconstruction(parameters=None, input_path='detector_out.h5', output_path='analyzer_out.h5')

        pxs = PhotonExperimentSimulation(photon_source=photon_source,
                                         photon_propagator=photon_propagator,
                                         photon_interactor=photon_interactor,
                                         photon_diffractor=photon_diffractor,
                                         photon_detector=photon_detector,
                                         photon_analyzer=photon_analyzer,
                                         )

        # Check queries.
        self.assertIs( pxs.photon_source, photon_source )
        self.assertIs( pxs.photon_propagator, photon_propagator )
        self.assertIs( pxs.photon_interactor, photon_interactor )
        self.assertIs( pxs.photon_diffractor, photon_diffractor )
        self.assertIs( pxs.photon_detector, photon_detector )
        self.assertIs( pxs.photon_analyzer, photon_analyzer )

    def testConstructionExceptions(self):
        """ Test that the appropriate exceptions are thrown if the object is constructed incorrectly. """
        # Setup a minimal experiment simulation.
        source_input = TestUtilities.generateTestFilePath('FELsource_out.h5')
        diffr_input =  TestUtilities.generateTestFilePath('pmi_out.h5')
        pmi_input = TestUtilities.generateTestFilePath('prop_out.h5')
        photon_source = XFELPhotonSource(parameters=None, input_path=source_input, output_path='FELsource_out.h5')
        photon_propagator = XFELPhotonPropagator(parameters=None, input_path='FELsource_out.h5', output_path='prop_out.h5')
        photon_interactor = XMDYNDemoPhotonMatterInteractor(parameters=None,
                                                            input_path=pmi_input,
                                                            output_path='pmi_out.h5',
                                                            sample_path=self.__sample_path
                                                            )

        diffraction_parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameter_file' : TestUtilities.generateTestFilePath('s2e.beam'),
                     'beam_geometry_file' : TestUtilities.generateTestFilePath('s2e.geom'),
                   }
        photon_diffractor = SingFELPhotonDiffractor(parameters=diffraction_parameters, input_path=diffr_input, output_path='diffr_out.h5')

        photon_detector = PerfectPhotonDetector(parameters = None, input_path='diffr_out.h5', output_path='detector_out.h5')
        photon_analyzer = S2EReconstruction(parameters=None, input_path='detector_out.h5', output_path='analyzer_out.h5')

        # Check wrong source.
        self.assertRaises( TypeError, PhotonExperimentSimulation,
                                                                  photon_source=None,
                                                                  photon_propagator=photon_propagator,
                                                                  photon_interactor=photon_interactor,
                                                                  photon_diffractor=photon_diffractor,
                                                                  photon_detector=photon_detector,
                                                                  photon_analyzer=photon_analyzer,
                         )
        self.assertRaises( TypeError, PhotonExperimentSimulation,
                                                                  photon_source=photon_propagator,
                                                                  photon_propagator=photon_propagator,
                                                                  photon_interactor=photon_interactor,
                                                                  photon_diffractor=photon_diffractor,
                                                                  photon_detector=photon_detector,
                                                                  photon_analyzer=photon_analyzer,
                         )


        # Check wrong propagator.
        self.assertRaises( TypeError, PhotonExperimentSimulation,
                                                                  photon_source=photon_source,
                                                                  photon_propagator=None,
                                                                  photon_interactor=photon_interactor,
                                                                  photon_diffractor=photon_diffractor,
                                                                  photon_detector=photon_detector,
                                                                  photon_analyzer=photon_analyzer,
                         )
        self.assertRaises( TypeError, PhotonExperimentSimulation,
                                                                  photon_source=photon_source,
                                                                  photon_propagator=photon_source,
                                                                  photon_interactor=photon_interactor,
                                                                  photon_diffractor=photon_diffractor,
                                                                  photon_detector=photon_detector,
                                                                  photon_analyzer=photon_analyzer,
                         )



        # Check wrong interactor.
        self.assertRaises( TypeError, PhotonExperimentSimulation,
                                                                  photon_source=photon_source,
                                                                  photon_propagator=photon_propagator,
                                                                  photon_interactor=None,
                                                                  photon_diffractor=photon_diffractor,
                                                                  photon_detector=photon_detector,
                                                                  photon_analyzer=photon_analyzer,
                         )
        self.assertRaises( TypeError, PhotonExperimentSimulation,
                                                                  photon_source=photon_source,
                                                                  photon_propagator=photon_propagator,
                                                                  photon_interactor=photon_source,
                                                                  photon_diffractor=photon_diffractor,
                                                                  photon_detector=photon_detector,
                                                                  photon_analyzer=photon_analyzer,
                         )



        # Check wrong diffractor.
        self.assertRaises( TypeError, PhotonExperimentSimulation,
                                                                  photon_source=photon_source,
                                                                  photon_propagator=photon_propagator,
                                                                  photon_interactor=photon_interactor,
                                                                  photon_diffractor=None,
                                                                  photon_detector=photon_detector,
                                                                  photon_analyzer=photon_analyzer,
                         )
        self.assertRaises( TypeError, PhotonExperimentSimulation,
                                                                  photon_source=photon_source,
                                                                  photon_propagator=photon_propagator,
                                                                  photon_interactor=photon_interactor,
                                                                  photon_diffractor=photon_source,
                                                                  photon_detector=photon_detector,
                                                                  photon_analyzer=photon_analyzer,
                         )

        # Check wrong analyzer.
        self.assertRaises( TypeError, PhotonExperimentSimulation,
                                                                  photon_source=photon_source,
                                                                  photon_propagator=photon_propagator,
                                                                  photon_interactor=photon_interactor,
                                                                  photon_diffractor=photon_diffractor,
                                                                  photon_detector=photon_detector,
                                                                  photon_analyzer=None,
                         )
        self.assertRaises( TypeError, PhotonExperimentSimulation,
                                                                  photon_source=photon_source,
                                                                  photon_propagator=photon_propagator,
                                                                  photon_interactor=photon_interactor,
                                                                  photon_diffractor=photon_diffractor,
                                                                  photon_detector=photon_detector,
                                                                  photon_analyzer=photon_diffractor,
                         )

    def testCheckInterfaceConsistency(self):
        """ Test if the check for interface consistency works correctly. """

        # Setup a minimal experiment simulation.
        source_input = TestUtilities.generateTestFilePath('FELsource_out.h5')
        diffr_input =  TestUtilities.generateTestFilePath('pmi_out.h5')
        pmi_input = TestUtilities.generateTestFilePath('prop_out.h5')
        photon_source = XFELPhotonSource(parameters=None, input_path=source_input, output_path='FELsource_out.h5')
        photon_propagator = XFELPhotonPropagator(parameters=None, input_path='FELsource_out.h5', output_path='prop_out.h5')
        pmi_parameters= {'sample_path' :TestUtilities.generateTestFilePath('sample.h5')}
        photon_interactor = XMDYNDemoPhotonMatterInteractor(parameters=None,
                                                            input_path=pmi_input,
                                                            output_path='pmi_out.h5',
                                                            sample_path=self.__sample_path
                                                            )

        diffraction_parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameter_file' : TestUtilities.generateTestFilePath('s2e.beam'),
                     'beam_geometry_file' : TestUtilities.generateTestFilePath('s2e.geom'),
                   }
        photon_diffractor = SingFELPhotonDiffractor(parameters=diffraction_parameters, input_path=diffr_input, output_path='diffr_out.h5')

        photon_detector = PerfectPhotonDetector(parameters = None, input_path='diffr_out.h5', output_path='detector_out.h5')
        photon_analyzer = S2EReconstruction(parameters=None, input_path='detector_out.h5', output_path='analyzer_out.h5')

        pxs = PhotonExperimentSimulation(photon_source=photon_source,
                                         photon_propagator=photon_propagator,
                                         photon_interactor=photon_interactor,
                                         photon_diffractor=photon_diffractor,
                                         photon_detector=photon_detector,
                                         photon_analyzer=photon_analyzer,
                                         )

        interfaces_are_consistent = pxs._checkInterfaceConsistency()

        self.assertTrue( interfaces_are_consistent )





    def testSimS2EWorkflowTwoDiffractionPatterns(self):
        """ Testing that a workflow akin to the simS2E example workflow works. """

        # These directories and files are expected to be present after a successfull calculation.
        expected_dirs = [ 'pmi',
                          'diffr',
                          ]

        expected_symlinks = ['detector']

        expected_files = ['FELsource_out_0000001.h5',
                          'prop_out_0000001.h5',
                          'pmi/pmi_out_0000001.h5',
                          'diffr/diffr_out_0000001.h5',
                          'diffr/diffr_out_0000002.h5',
                          'detector/diffr_out_0000001.h5',
                          'detector/diffr_out_0000002.h5',
                          'orient_out.h5',
                          ]

        # Ensure proper cleanup.
        self.__files_to_remove = expected_files+expected_symlinks+['recon.h5']
        self.__dirs_to_remove = expected_dirs


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
                                                             sample_path=self.__sample_path)

        #  Diffraction with parameters.
        diffraction_parameters={ 'uniform_rotation': True,
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
                               'max_number_of_iterations'      : 3,
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

        # Check that all output files and directories are present.
        for directory in expected_dirs+expected_symlinks:
            self.assertTrue( os.path.isdir( directory ) )
        for f in expected_files:
            print f
            self.assertTrue( os.path.isfile( f ) )

    def testSimS2EWorkflowDirectories(self):
        """ Testing that a workflow akin to the simS2E example workflow works.
            Two sources, two diffraction patterns."""

        # Setup directories.
        working_directory = 'SPI'
        self.__dirs_to_remove.append(working_directory)
        source_dir = os.path.join( working_directory, 'FELsource' )
        prop_dir = os.path.join( working_directory, 'prop' )
        pmi_dir = os.path.join( working_directory, 'pmi' )
        diffr_dir = os.path.join( working_directory, 'diffr' )
        detector_dir = os.path.join( working_directory, 'detector' )
        recon_dir = os.path.join( working_directory, 'recon' )

        # Make directories.
        os.mkdir(working_directory)
        os.mkdir(source_dir)
        os.mkdir(prop_dir)
        os.mkdir(pmi_dir)
        os.mkdir(diffr_dir)
        os.mkdir(detector_dir)
        os.mkdir(recon_dir)

        # Ensure proper cleanup.
        self.__dirs_to_remove.append(working_directory)

        # Location of the FEL source file.
        source_input = TestUtilities.generateTestFilePath('FELsource_out')

        # Photon source.
        photon_source = XFELPhotonSource(parameters=None, input_path=source_input, output_path=source_dir)

        # Photon propagator, default parameters.
        photon_propagator = XFELPhotonPropagator(parameters=None, input_path=source_dir, output_path=prop_dir)

        # Photon interactor with default parameters.
        photon_interactor = XMDYNDemoPhotonMatterInteractor( parameters=None,
                                                             input_path=prop_dir,
                                                             output_path=pmi_dir,
                                                             sample_path=self.__sample_path)

        #  Diffraction with parameters.
        diffraction_parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 2,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameter_file' : TestUtilities.generateTestFilePath('s2e.beam'),
                     'beam_geometry_file' : TestUtilities.generateTestFilePath('s2e.geom'),
                     }

        photon_diffractor = SingFELPhotonDiffractor(
                parameters=diffraction_parameters,
                input_path=pmi_dir,
                output_path=diffr_dir)

        # Reconstruction: EMC+DM
        emc_parameters = {'initial_number_of_quaternions' : 1,
                               'max_number_of_quaternions'     : 9,
                               'max_number_of_iterations'      : 3,
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
                                          input_path=diffr_dir,
                                          output_path = recon_dir
                                          )

        # Setup the photon experiment.
        pxs = PhotonExperimentSimulation(photon_source=photon_source,
                                         photon_propagator=photon_propagator,
                                         photon_interactor=photon_interactor,
                                         photon_diffractor=photon_diffractor,
                                         photon_detector=None,
                                         photon_analyzer=reconstructor,
                                         )

        # Run the experiment.
        pxs.run()

        ## Check that all output files and directories are present.
        #for directory in expected_dirs+expected_symlinks:
            #self.assertTrue( os.path.isdir( directory ) )
        #for f in expected_files:
            #print f
            #self.assertTrue( os.path.isfile( f ) )



    def testSimS2EWorkflowSingleFile(self):
        """ Testing that a workflow akin to the simS2E example workflow works. Only one I/O file per calculator. """

        # These directories and files are expected to be present after a successfull calculation.
        expected_dirs = [ 'pmi',
                          'diffr',
                          ]

        expected_files = ['FELsource_out.h5',
                          'prop_out.h5',
                          'pmi/pmi_out_0000001.h5',
                          'diffr/diffr_out_0000001.h5',
                          'orient_out.h5',
                          'recon.h5'
                          ]

        # Ensure proper cleanup.
        self.__files_to_remove = expected_files
        self.__dirs_to_remove = expected_dirs


        # Location of the FEL source file.
        source_input = TestUtilities.generateTestFilePath('FELsource_out/FELsource_out_0000001.h5')

        # Photon source.
        photon_source = XFELPhotonSource(parameters=None, input_path=source_input, output_path='FELsource_out.h5')

        # Photon propagator, default parameters.
        photon_propagator = XFELPhotonPropagator(parameters=None, input_path='FELsource_out.h5', output_path='prop_out.h5')

        # Photon interactor with default parameters.
        photon_interactor = XMDYNDemoPhotonMatterInteractor( parameters=None,
                                                             input_path='prop_out.h5',
                                                             output_path='pmi',
                                                             sample_path=self.__sample_path)

        #  Diffraction with parameters.
        diffraction_parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 1,
                     'beam_parameter_file' : TestUtilities.generateTestFilePath('s2e.beam'),
                     'beam_geometry_file' : TestUtilities.generateTestFilePath('s2e.geom'),
                     }

        photon_diffractor = SingFELPhotonDiffractor(
                parameters=diffraction_parameters,
                input_path='pmi',
                output_path='diffr')


        # Reconstruction: EMC+DM
        emc_parameters = {'initial_number_of_quaternions' : 1,
                               'max_number_of_quaternions'     : 2,
                               'max_number_of_iterations'      : 10,
                               'min_error'                     : 1.0e-6,
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
                                          input_path=TestUtilities.generateTestFilePath('diffr'),  # Cheeting here to provide more realistic data for emc.
                                          output_path = 'recon.h5'
                                          )

        # Setup the photon experiment.
        pxs = PhotonExperimentSimulation(photon_source=photon_source,
                                         photon_propagator=photon_propagator,
                                         photon_interactor=photon_interactor,
                                         photon_diffractor=photon_diffractor,
                                         photon_detector=None,
                                         photon_analyzer=reconstructor,
                                         )

        # Run the experiment.
        pxs.run()

        # Check that all output files and directories are present.
        for directory in expected_dirs:
            self.assertTrue( os.path.isdir( directory ) )
        for f in expected_files:
            print f
            self.assertTrue( os.path.isfile( f ) )


if __name__ == '__main__':
    unittest.main()
