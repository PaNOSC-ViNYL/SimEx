""" :module: for the XMDYNPhotonMatterAnalysis."""
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
RENDER_PLOT=False # Set to True or use environment variable to show plots.


import numpy
import os
import shutil
import unittest

# Import the class to test.
from SimEx.Analysis.AbstractAnalysis import AbstractAnalysis, plt
from SimEx.Analysis.XMDYNPhotonMatterAnalysis import XMDYNPhotonMatterAnalysis
from SimEx.Analysis.XMDYNPhotonMatterAnalysis import read_h5_dataset
from SimEx.Analysis.XMDYNPhotonMatterAnalysis import load_sample
from SimEx.Analysis.XMDYNPhotonMatterAnalysis import calculate_ion_charge
from SimEx.Analysis.XMDYNPhotonMatterAnalysis import calculate_displacement

from TestUtilities import TestUtilities

if 'RENDER_PLOT' in os.environ:
    RENDER_PLOT=bool(os.environ['RENDER_PLOT'])


class XMDYNPhotonMatterAnalysisTest(unittest.TestCase):
    """
    Test class for the XMDYNPhotonMatterAnalysis class.
    """

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

        self.__test_data = TestUtilities.generateTestFilePath('pmi_out_0000001.h5')

    def tearDown(self):
        """ Tearing down a test. """

        for f in self.__files_to_remove:
            if os.path.isfile(f): os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d): shutil.rmtree(d)

        if RENDER_PLOT:
            plt.show()

    def testDefaultConstruction(self):
        """ Testing the default construction of the class. """

        # Constructing the object without input fails.
        self.assertRaises(TypeError, XMDYNPhotonMatterAnalysis )

    def testShapedConstruction(self):
        """ Testing the construction of the class with non-default parameters. """

        # Construct the object.
        analyzer = XMDYNPhotonMatterAnalysis(input_path=self.__test_data)

        self.assertIsInstance(analyzer, XMDYNPhotonMatterAnalysis)
        self.assertIsInstance(analyzer, AbstractAnalysis)
        self.assertIsInstance(analyzer, object)

        self.assertIsInstance( analyzer.input_path, str )
        self.assertEqual( analyzer.input_path, self.__test_data)

    def test_load_snapshot(self) :
        """ Test loading a snapshot's content. """

        analysis = XMDYNPhotonMatterAnalysis(input_path=self.__test_data)
        snapshot = analysis.load_snapshot(1)

        self.assertIsInstance(snapshot, dict)

        expected_keys = set(['Nph', 'q', 'r', 'T', 'ff', 'Z', 'snp', 'xyz'])
        present_keys = set(snapshot.keys())
        self.assertLessEqual(expected_keys, present_keys)

    def test_load_sample(self) :
        """ Test loading a sample file. """

        sample = load_sample(TestUtilities.generateTestFilePath('sample.h5'))
        self.assertIsInstance(sample, dict)

        # Check all keys are present.
        expected_keys = set(['Z', 'selZ', 'r'])
        present_keys = set(sample.keys())
        self.assertLessEqual(expected_keys, present_keys)

    def test_number_of_snapshots(self):
        """ Test querying the number of snapshots. """

        analysis = XMDYNPhotonMatterAnalysis(input_path=self.__test_data)
        number_of_snapshots = analysis.number_of_snapshots()

        self.assertEqual(number_of_snapshots, 102)

    def test_read_h5_dataset(self):
        """ Test reading a dataset from an hdf5 file. """

        f0 = read_h5_dataset(self.__test_data, 'data/snp_0000001/ff')

        self.assertEqual(f0.shape, (6,101))

    def test_calculate_displacement(self):
        """ Test evaluating the average displacement. """

        analysis = XMDYNPhotonMatterAnalysis(input_path=self.__test_data)
        snapshot = analysis.load_snapshot(1)

        sample = load_sample(TestUtilities.generateTestFilePath('sample.h5'))
        r0 = sample['r']
        displacement = calculate_displacement(snapshot, r0, sample)

        print(displacement)

        self.assertIsInstance(displacement, numpy.ndarray)

    def test_calculate_ion_charge(self):
        """ Test evaluating the number of electrons. """

        analysis = XMDYNPhotonMatterAnalysis(input_path=self.__test_data)
        snapshot = analysis.load_snapshot(56)

        sample = load_sample(TestUtilities.generateTestFilePath('sample.h5'))
        E = calculate_ion_charge(snapshot, sample)

        self.assertIsInstance(E, numpy.ndarray)


if __name__ == '__main__':
    unittest.main()
