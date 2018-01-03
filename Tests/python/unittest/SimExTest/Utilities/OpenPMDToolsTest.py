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

""" Test module for the openpmd tools.
    @author CFG
    @institution XFEL
    @creation 20160517
"""
import exceptions
import h5py
import numpy
import os
from . import paths
import unittest

from SimEx.Utilities import OpenPMDTools as opmd
from SimEx.Utilities.wpg_to_opmd import convertToOPMD
from SimEx.Utilities.hydro_txt_to_opmd import convertTxtToOPMD

from SimEx.Utilities import checkOpenPMD_h5 as opmd_validator

from TestUtilities.TestUtilities import generateTestFilePath

class OpenPMDToolsTest(unittest.TestCase):
    """ Test class for the openpmd tools. """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """

        # Remove temporary files.
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)

    def testWpgToOPMDConverter(self):
        """ Test the conversion of wpg output to openPMD conform file."""

        # Get sample file.
        h5_input = generateTestFilePath('prop_out_0000001.h5')

        # Convert.
        convertToOPMD(h5_input)

        # New file name.
        opmd_h5_file = h5_input.replace(".h5", ".opmd.h5")

        # Make sure we clean up after test.
        self.__files_to_remove.append(opmd_h5_file)

        # Check new file was generated.
        self.assertTrue( os.path.isfile( opmd_h5_file ) )

        # Validate the new file.
        g = opmd_validator.open_file(opmd_h5_file)

        # Setup result array.
        result_array = numpy.array([0, 0])
        result_array += opmd_validator.check_root_attr(g, False)

        # Go through all the iterations, checking both the particles.
        # and the meshes
        extensions = {'ED-PIC': False, 'HYDRO1D': False}
        result_array += opmd_validator.check_iterations(g,False,extensions)

        # Assert that no errors nor warnings were issued.
        self.assertEqual( result_array[0], 0 )
        self.assertEqual( result_array[1], 0 )


    def testHydroTxtToOPMDConverter(self):
        """ Test the conversion of esther output to openPMD conform hdf5 file."""

        # Get sample file.
        esther_output = generateTestFilePath('hydroTests')

        # Convert.
        convertTxtToOPMD(esther_output)

        # New file name.
        opmd_h5_file = esther_output + '/output.opmd.h5'

        # Make sure we clean up after test.
        self.__files_to_remove.append(opmd_h5_file)

        # Check new file was generated.
        self.assertTrue( os.path.isfile( opmd_h5_file ) )

        # Validate the new file.
        g = opmd_validator.open_file(opmd_h5_file)

        # Setup result array.
        result_array = numpy.array([0, 0])
        result_array += opmd_validator.check_root_attr(g, False)

        # Go through all the iterations, checking both the particles.
        # and the meshes.
        extensions = {'ED-PIC': False, 'HYDRO1D': True}
        result_array += opmd_validator.check_iterations(g,False,extensions)

        # Assert that no errors nor warnings were issued.
        self.assertEqual( result_array[0], 0 )
        self.assertEqual( result_array[1], 0 )


if __name__ == '__main__':
    unittest.main()
