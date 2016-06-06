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
import paths
import unittest

from SimEx.Utilities import OpenPMDTools as opmd
from SimEx.Utilities.wpg_to_opmd import convertToOPMD

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

    def testSampleScript(self):
        """ Testing the generic openpmd-Validator script from  https://github.com/openPMD/openPMD-validator/createExamples_h5.py """

        h5_name = "openpmd_example.h5"

        # Trigger cleanup.
        self.__files_to_remove.append(h5_name)

        # Open plain h5 file.
        f = h5py.File(h5_name, "w")

        # Setup the root attributes for iteration 0
        opmd.setup_root_attr(f)

        # Setup basepath
        opmd.setup_base_path(f, iteration=0)

        # Write the field records
        opmd.write_meshes(f, iteration=0)

        # Write the particle records
        opmd.write_particles(f, iteration=0)

        # Close the file
        f.close()

        # Assert file exists.
        self.assertIn( h5_name, os.listdir('.') )

    def testValidate(self):
        """ Test validation of an existing openpmd conformant file. """

        h5_name = "openpmd_example.h5"

        # Trigger cleanup.
        self.__files_to_remove.append(h5_name)

        # Get file handle.
        f = h5py.File(h5_name, "w")

        # Setup the root attributes for iteration 0
        opmd.setup_root_attr(f)

        # Setup basepath
        opmd.setup_base_path(f, iteration=0)

        # Write the field records
        opmd.write_meshes(f, iteration=0)

        # Write the particle records
        opmd.write_particles(f, iteration=0)

        f.close()

        g = opmd.open_file(h5_name)

        # root attributes at "/"
        result_array = numpy.array([0, 0])
        result_array += opmd.check_root_attr(g, False, False)

        # Go through all the iterations, checking both the particles.
        # and the meshes
        result_array += opmd.check_iterations(g,False,False)

        # Assert that no errors nor warnings were issued.
        self.assertEqual( result_array[0], 0 )
        self.assertEqual( result_array[1], 0 )


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
        self.assertIn( 'prop_out_0000001.opmd.h5', os.listdir( os.path.dirname(opmd_h5_file) ) )

        # Validate the new file.
        g = opmd.open_file(opmd_h5_file)

        # Setup result array.
        result_array = numpy.array([0, 0])
        result_array += opmd.check_root_attr(g, False, False)

        # Go through all the iterations, checking both the particles.
        # and the meshes
        result_array += opmd.check_iterations(g,False,False)

        # Assert that no errors nor warnings were issued.
        self.assertEqual( result_array[0], 0 )
        self.assertEqual( result_array[1], 0 )


if __name__ == '__main__':
    unittest.main()
