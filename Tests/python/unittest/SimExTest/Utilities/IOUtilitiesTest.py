""" Test module for the IO Utilities.  """
##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 Carsten Fortmann-Grote                         #
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

import exceptions
import os
import shutil
import numpy
import paths
import unittest
from wpg import Wavefront

from TestUtilities.TestUtilities import generateTestFilePath
from SimEx.Utilities import IOUtilities

class IOUtilitiesTest(unittest.TestCase):
    """ Test class for the IOUtilities. """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__paths_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """
        # Clean up.
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for p in self.__paths_to_remove:
            if os.path.isdir(p):
                shutil.rmtree(p)

    def testLoadPDB(self):
        """ Check that we can load a pdb and convert it to a dict. """

        # Setup path to pdb file.
        pdb_path = generateTestFilePath("2nip.pdb")

        self.__paths_to_remove.append('obsolete')

        # Attempt to load it.
        return_dict = IOUtilities.loadPDB(pdb_path)

        # Check items on dict.
        self.assertIsInstance( return_dict['Z'], numpy.ndarray )
        self.assertIsInstance( return_dict['r'], numpy.ndarray )
        self.assertIsInstance( return_dict['selZ'], dict )
        self.assertIsInstance( return_dict['N'], int )
        self.assertEqual( return_dict['Z'].shape, (4728,) )
        self.assertEqual( return_dict['r'].shape, (4728,3) )

        # Check that return type is a dict.
        self.assertIsInstance( return_dict, dict )

        # Check exception on wrong input type.
        self.assertRaises( IOError, IOUtilities.loadPDB, [1,2] )

        # Check exception on wrong file type.
        self.assertRaises( IOError, IOUtilities.loadPDB, generateTestFilePath("sample.h5") )

    def testLoadXYZ(self):
        """ Check that we can load a xyz file and convert it to a dict. """

        # Setup path to xyz file.
        xyz_path = generateTestFilePath("Fe2O3_poly_test.xyz")

        # Attempt to load it.
        return_dict = IOUtilities.loadXYZ(xyz_path)

        # Check that return type is a dict.
        self.assertIsInstance( return_dict, dict )

        # Check items on dict.
        self.assertIsInstance( return_dict['Z'], numpy.ndarray )
        self.assertIsInstance( return_dict['r'], numpy.ndarray )
        self.assertIsInstance( return_dict['selZ'], dict )
        self.assertIsInstance( return_dict['N'], int )
        self.assertEqual( return_dict['Z'].shape, (100,) )
        self.assertEqual( return_dict['r'].shape, (100,3) )

    def testQueryNonexisitngPDB(self):
        """ Check exception if querying a non-existing pdb """
        # Check exception on wrong input type.
        self.assertRaises( IOError, IOUtilities.checkAndGetPDB, 'xyz.pdb' )


    def testQueryPDB(self):
        """ Check that we can query a non-existing pdb from pdb.org and convert it to a dict. """
        # Setup path to pdb file.
        pdb_path = '5UDC.pdb'
        self.__files_to_remove.append(pdb_path)
        self.__paths_to_remove.append('obsolete')

        # Attempt to load it.
        pdb_path = IOUtilities.checkAndGetPDB(pdb_path)

        # Check it's there.
        self.assertTrue( os.path.isfile( pdb_path ) )

        # Check exception on wrong input type.
        #self.assertRaises( IOError, IOUtilities.checkAndGetPDB, 'xyz.pdb' )

    def testQueryPDBTwice(self):
        """ Check that we can do two subsequent queries (fails if urllib.urlcleanup is not called.) """
        # Setup path to pdb file.
        pdb_path = '5loy.pdb'
        self.__files_to_remove.append(pdb_path)
        self.__paths_to_remove.append('obsolete')

        # Attempt to load it.
        pdb_path = IOUtilities.checkAndGetPDB(pdb_path)

        # Check it's there.
        self.assertTrue( os.path.isfile( pdb_path ) )

        # Remove it.
        os.remove(pdb_path)

        # Query again.
        pdb_path = IOUtilities.checkAndGetPDB(pdb_path)

        # Check it's there.
        self.assertTrue( os.path.isfile( pdb_path ) )


    def testPdbToS2ESampleDict(self):
        """ Check the utility that converts a pdb file to an s2e sample dict.
        """

        # Setup path to pdb file.
        pdb_path = generateTestFilePath("2nip.pdb")

        # Attempt to load it.
        return_dict = IOUtilities._pdbToS2ESampleDict(pdb_path)

        # Check that return type is a dict.
        self.assertIsInstance( return_dict, dict )

        # Check items on dict.
        self.assertIsInstance( return_dict['Z'], numpy.ndarray )
        self.assertIsInstance( return_dict['r'], numpy.ndarray )
        self.assertIsInstance( return_dict['selZ'], dict )
        self.assertIsInstance( return_dict['N'], int )
        self.assertEqual( return_dict['Z'].shape, (4728,) )
        self.assertEqual( return_dict['r'].shape, (4728,3) )

    def testPdbToS2ESampleDictExceptions(self):
        """ Check that improper input raises in converter utility. """

        self.assertRaises( IOError, IOUtilities._pdbToS2ESampleDict, None )
        self.assertRaises( IOError, IOUtilities._pdbToS2ESampleDict, "xyz.pdb" )
        self.assertRaises( IOError, IOUtilities._pdbToS2ESampleDict, 1234 )

    def testGenesisDFLToWPGWavefront(self):
        """ Check the conversion from genesis dfl to wpg readable hdf5. """

        genesis_out_file = generateTestFilePath("genesis/lcls/lcls.out")
        genesis_dfl_file = generateTestFilePath("genesis/lcls/lcls.out.dfl")

        wf = IOUtilities.genesis_dfl_to_wavefront(genesis_out_file, genesis_dfl_file)

        self.assertIsInstance(wf, Wavefront)




if __name__ == '__main__':
    unittest.main()
