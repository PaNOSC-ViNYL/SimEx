""" :module OpenPMDToolsTest: Test module for the openpmd tools.  """
##########################################################################
#                                                                        #
# Copyright (C) 2015-2019 Carsten Fortmann-Grote                         #
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

import numpy
import os
import unittest
import openpmd_api as opmd

import wpg
from SimEx.Utilities import checkOpenPMD_h5 as opmd_validator
from SimEx.Utilities.hydro_txt_to_opmd import convertTxtToOPMD
from SimEx.Utilities.wpg_to_opmd import convertToOPMD, convertToOPMDLegacy
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

    def testWpgToOPMDLegacyConverter(self):
        """ Test the conversion of wpg output to openPMD conform file, omitting the openpmd-api."""

        # Get sample file.
        h5_input = generateTestFilePath('prop_out/prop_out_0000011.h5')

        # Convert.
        convertToOPMDLegacy(h5_input)

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

        # Go through all the iterations, checking both the particles and the meshes
        extensions = {'ED-PIC': False, 'HYDRO1D': False}
        result_array += opmd_validator.check_iterations(g,False,extensions)

        # Assert that no errors nor warnings were issued.
        self.assertEqual( result_array[0], 0 )
        self.assertEqual( result_array[1], 0 )

    def testWpgToOPMDConverter(self):
        """ Test the conversion of wpg output to openPMD conform file."""

        # Get sample file.
        h5_input = generateTestFilePath('prop_out/prop_out_0000011.h5')

        # Convert.
        convertToOPMD(h5_input)

        # New file name.
        opmd_h5_file = h5_input.replace(".h5", ".opmd.h5")
        self.__files_to_remove.append(opmd_h5_file)

        # Check new file was generated.
        self.assertTrue( os.path.isfile( opmd_h5_file ) )

        # Read the file back in through the API.
        series = opmd.Series(opmd_h5_file, opmd.Access_Type.read_only)

        self.assertIsInstance(series, opmd.Series)

        # Check attributes are present.
        try:
            series.author
            series.date
            series.software
            series.software_version
            series.get_attribute("radius of curvature in x")
            series.get_attribute("z coordinate")
            series.get_attribute("Rx_Unit_Dimension")
            series.get_attribute("Rx_UnitSI")
            series.get_attribute("radius of curvature in y")
            series.get_attribute("Ry_Unit_Dimension")
            series.get_attribute("Ry_UnitSI")
            series.get_attribute("Delta radius of curvature in x")
            series.get_attribute("DRx_Unit_Dimension")
            series.get_attribute("DRx_UnitSI")
            series.get_attribute("Delta radius of curvature in y")
            series.get_attribute("DRy_Unit_Dimension")
            series.get_attribute("DRy_UnitSI")
            series.get_attribute("photon energy")
            series.get_attribute("photon energy unit dimension")
            series.get_attribute("photon energy UnitSI")

        except RuntimeError:
            self.fail("Error while querying attribute.")
        except:
            raise

        # Check the beamline serialization
        self.assertIsInstance(series.get_attribute("beamline"), str)

    def testLoadOPMDWavefront(self):
        """ Test if loading a wavefront from openpmd-hdf into a WPG structure works."""

        # Get sample file.
        h5_input = generateTestFilePath('prop_out/prop_out_0000011.h5')

        # Convert.
        convertToOPMD(h5_input)

        # New file name.
        opmd_h5_file = h5_input.replace(".h5", ".opmd.h5")
        self.__files_to_remove.append(opmd_h5_file)
        
        # Reconstruct the series.
        series = opmd.Series(opmd_h5_file, opmd.Access_Type.read_only)
        wavefront = wpg.Wavefront()

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
