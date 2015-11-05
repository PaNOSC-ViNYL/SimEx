""" Test module for module PhotonExperimentSimulation from XXX
    @author : CFG
    @creation : 20151005
"""

import unittest
import paths

from TestUtilities import TestUtilities
from XXX.Calculators.XFELPhotonSource import XFELPhotonSource
from XXX.Calculators.XFELPhotonPropagator import XFELPhotonPropagator

from XXX.PhotonExperimentSimulation.PhotonExperimentSimulation import PhotonExperimentSimulation

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

    def tearDown(self):
        """ Tearing down a test. """

    def notestConstruction(self):
        """ Testing something stupid."""
        experiment_simulation_platform = PhotonExperimentSimulation()

        self.assertIsInstance( experiment_simulation_platform, PhotonExperimentSimulation )

    def testMinimalWorkflow(self):
        """ Testing that a minimal workflow works. """

        source_input = TestUtilities.generateTestFilePath('FELsource_out.h5')
        photon_source = XFELPhotonSource(parameters=None, input_path=source_input, output_path='FELsource_out.h5')
        photon_propagator = XFELPhotonPropagator(parameters=None, input_path='FELsource_out.h5', output_path='prop_out.h5')

        pxs = PhotonExperimentSimulation(photon_source=photon_source,
                                         photon_propagator=photon_propagator)

        pxs.run()

if __name__ == '__main__':
    unittest.main()
