""" Test module for module PhotonExperimentSimulation from SimEx
    @author : CFG
    @creation : 20151005
"""

import unittest
import paths

from TestUtilities import TestUtilities
from SimEx.Calculators.XFELPhotonSource import XFELPhotonSource
from SimEx.Calculators.XFELPhotonPropagator import XFELPhotonPropagator
from SimEx.Calculators.FakePhotonMatterInteractor import FakePhotonMatterInteractor
from SimEx.Calculators.SingFELPhotonDiffractor import SingFELPhotonDiffractor

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

    def tearDown(self):
        """ Tearing down a test. """

    def notestMinimalWorkflow(self):
        """ Testing that a minimal workflow works. """

        #source_input = TestUtilities.generateTestFilePath('FELsource_out_0000001.h5')
        source_input = TestUtilities.generateTestFilePath('FELsource_out.h5')
        diffr_input =  TestUtilities.generateTestFilePath('pmi_out.h5')
        pmi_input = TestUtilities.generateTestFilePath('prop_out.h5')
        photon_source = XFELPhotonSource(parameters=None, input_path=source_input, output_path='FELsource_out.h5')
        photon_propagator = XFELPhotonPropagator(parameters=None, input_path='FELsource_out.h5', output_path='prop_out.h5')
        photon_interactor = FakePhotonMatterInteractor(parameters=None, input_path=pmi_input, output_path='pmi_out.h5')
        photon_diffractor = SingFELPhotonDiffractor(parameters=None, input_path=diffr_input, output_path='diffr_out.h5')

        pxs = PhotonExperimentSimulation(photon_source=photon_source,
                                         photon_propagator=photon_propagator,
                                         photon_interactor=photon_interactor,
                                         photon_diffractor=photon_diffractor)

        pxs.run()

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

        pxs = PhotonExperimentSimulation(photon_source=photon_source,
                                         photon_propagator=photon_propagator,
                                         photon_interactor=photon_interactor,
                                         photon_diffractor=photon_diffractor)

        interfaces_are_consistent = pxs._checkInterfaceConsistency()

        self.assertTrue( interfaces_are_consistent )





if __name__ == '__main__':
    unittest.main()
