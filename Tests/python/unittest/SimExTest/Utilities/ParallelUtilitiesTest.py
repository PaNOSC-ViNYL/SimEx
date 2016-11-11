##########################################################################
#                                                                        #
# Copyright (C) 2016 Carsten Fortmann-Grote                              #
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

""" Test module for the parallel utilities.
    @author SY
    @institution DESY
    @creation 20161111
"""
import exceptions
import os
import unittest

from SimEx.Utilities import ParallelUtilities

class ParallelUtilitiesTest(unittest.TestCase):
    """ Test class for the ParallelUtilities. """

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
        try:
            del os.environ['SIMEX_NNODES']
            del os.environ['SIMEX_NCORES']
        except:
            pass
        try:
            del os.environ['SLURM_NNODES']
            del os.environ['SLURM_CPUS_PER_NODE']
        except:
            pass



        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for p in self.__paths_to_remove:
            if os.path.isdir(p):
                shutil.rmtree(p)

    def testResourceInfoFromMPIWorks(self):

        resource = ParallelUtilities.getParallelResourceInfo()
        self.assertGreater(resource['NCores'],0)
        self.assertEqual(resource['NNodes'],1)

    def testResourceInfoNothingWorked(self):
# we set SIMEX_MPICOMMAND so that it call return error
        os.environ["SIMEX_MPICOMMAND"]='blabla'

        resource = ParallelUtilities.getParallelResourceInfo()

        self.assertEqual(resource['NCores'],0)
        self.assertEqual(resource['NNodes'],1)

        del os.environ["SIMEX_MPICOMMAND"]


    def testResourceInfoFromSimexWorks(self):

        os.environ["SIMEX_NNODES"]='1'
        os.environ["SIMEX_NCORES"]='1'

        resource = ParallelUtilities.getParallelResourceInfo()
        
        self.assertEqual( resource['NCores'],1)
        self.assertEqual( resource['NNodes'],1)

        os.environ["SIMEX_NNODES"]='-1'
        os.environ["SIMEX_NCORES"]='-1'

        self.assertRaises( IOError, ParallelUtilities.getParallelResourceInfo)

    def testResourceInfoFromSlurm_WorksForSingleNode(self):

        os.environ['SLURM_NNODES']='1'
        os.environ['SLURM_CPUS_PER_NODE']='40'

        resource = ParallelUtilities.getParallelResourceInfo()

        self.assertEqual( resource['NCores'],40)
        self.assertEqual( resource['NNodes'],1)

    def testResourceInfoFromSlurm_WorksForMultipleNodeWithSameAmountOfCores(self):

        os.environ['SLURM_NNODES']='3'
        os.environ['SLURM_CPUS_PER_NODE']='40x(3)'

        resource = ParallelUtilities.getParallelResourceInfo()

        self.assertEqual( resource['NCores'],120)
        self.assertEqual( resource['NNodes'],3)

    def testResourceInfoFromSlurm_WorksForMultipleNodeWithDifferentAmountOfCores(self):

        os.environ['SLURM_NNODES']='3'
        os.environ['SLURM_CPUS_PER_NODE']='40x(2),20x(1),10x(10)'

        resource = ParallelUtilities.getParallelResourceInfo()

        self.assertEqual(resource['NCores'],200)
        self.assertEqual(resource['NNodes'],3)



if __name__ == '__main__':
    unittest.main()
