""" Test module for the GAPDPhotonDiffractor."""
##########################################################################
# 
# Modified by Juncheng E in 2020                                         #
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

import os, shutil
import subprocess
import tempfile
import unittest

from TestUtilities import TestUtilities

class GAPDPhotonDiffractorTest(unittest.TestCase):
    """
    Test class for the GAPDPhotonDiffractor class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        pass

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        pass

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)


    def testGAPDInstallation(self):
        """ Make a test run of GAPD using the CLI and a config shipped with the GAPD package. """

        # Make a tmpdir
        tmp_dir = tempfile.mkdtemp(prefix='gapd_')

        # Copy input file to tmp_dir
        shutil.copy2( TestUtilities.generateTestFilePath( "in.GAPD"), tmp_dir)
        shutil.copy2( TestUtilities.generateTestFilePath( "single-cu.cfg"), tmp_dir)
        # Chdir to tmp directory.
        old_pwd = os.getcwd()
        os.chdir(tmp_dir)

        proc = subprocess.Popen( ["GAPD.cuda", "-i", "in.GAPD"] )
        proc.wait()

        self.assertIn( "cu.00-1.kspace.dat", os.listdir(tmp_dir))

        os.chdir(old_pwd)
   def testConstructionParameters(self):
    """ Check we can construct with a parameter object. """
    parameters=GAPDPhotonDiffractorParameters(beam_parameters=self.beam,
                                              detector_geometry=self.detector_geometry,
                                              )

if __name__ == '__main__':
    unittest.main()

