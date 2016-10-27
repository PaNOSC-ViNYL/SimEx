##########################################################################
#                                                                        #
# Copyright (C) 2015, 2016 Carsten Fortmann-Grote                        #
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

""" Functional test for WPG.

    @author : CFG
    @institution : XFEL
    @creation 20160915

"""

import h5py
import math
import numpy
import os, shutil
import paths
import unittest

from TestUtilities import TestUtilities

from SimEx.Calculators.SingFELPhotonDiffractor import SingFELPhotonDiffractor
from SimEx.Parameters.SingFELPhotonDiffractorParameters import SingFELPhotonDiffractorParameters

class singfelTest(unittest.TestCase):
    """
    Test class for the singfel backengine.
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

    def tearDown(self):
        """ Tearing down a test. """

        for f in self.__files_to_remove:
            if os.path.isfile(f): os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d): shutil.rmtree(d)

    def testReference(self, debug=False):
        """ Check that singfel reproduces a given set of reference data. """

        self.__dirs_to_remove.append('diffr')

        beam_file = TestUtilities.generateTestFilePath('s2e.beam')
        geom_file = TestUtilities.generateTestFilePath('s2e.geom')
        # Setup diffraction parameters (no rotation because reference test).
        parameters = SingFELPhotonDiffractorParameters(
                                                       uniform_rotation=False,
                                                       calculate_Compton=True,
                                                       slice_interval=100,
                                                       number_of_slices=100,
                                                       pmi_start_ID=1,
                                                       pmi_stop_ID =1,
                                                       number_of_diffraction_patterns=1,
                                                       beam_parameter_file=beam_file,
                                                       beam_geometry_file=geom_file,
                                                       number_of_MPI_processes=2,
                                                        )

        # Setup diffraction calculator.
        diffractor = SingFELPhotonDiffractor(
                parameters=parameters,
                input_path=TestUtilities.generateTestFilePath('pmi_out'),
                output_path='diffr'
                )

        # Run (reads input and write output, as well).
        diffractor.backengine()

        # Open results file.
        h5_handle = h5py.File(os.path.join(diffractor.output_path,'diffr_out_0000001.h5'),'r')

        # Get data (copy).
        diffraction_data = h5_handle['/data/diffr'].value

        h5_handle.close()

        # Get total intensity.
        intensity = diffraction_data.sum()

        # Get hash of the data.
        this_hash = hash( diffraction_data.tostring() )

        if debug:
            print "%15.14e" % (intensity)

            # Save wavefront data for reference.
            #########################################################################################
            ## ATTENTION: Overwrites reference data, use only if you're sure you want to do this. ###
            #########################################################################################
            #with open(TestUtilities.generateTestFilePath("singfel_reference.hash.txt"), 'w') as hashfile:
                #hashfile.write(str(this_hash))
                #hashfile.close()
            #########################################################################################

            self.assertEqual(math.pi, 22./7.)

        # Load reference hash.
        with open( TestUtilities.generateTestFilePath("singfel_reference.hash.txt"), 'r') as hashfile:
            ref_hash = hashfile.readline()
            hashfile.close()

        # Weak test.
        reference_intensity = '5.18647193908691e+01'
        self.assertEqual( "%15.14e" % (intensity), reference_intensity)

        # Strong test.
        self.assertEqual( ref_hash, str(this_hash) )

if __name__ == '__main__':
    unittest.main()
