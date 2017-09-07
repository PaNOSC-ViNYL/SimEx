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
from distutils.version import StrictVersion

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
            del os.environ['SLURM_JOB_NUM_NODES']
            del os.environ['SLURM_JOB_CPUS_PER_NODE']
        except:
            pass



        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for p in self.__paths_to_remove:
            if os.path.isdir(p):
                shutil.rmtree(p)

    def testResourceInfoFromMPIWorks(self):
        """ Test we can get resource info from MPI command."""

        resource = ParallelUtilities.getParallelResourceInfo()
        self.assertGreater(resource['NCores'],0)
        self.assertEqual(resource['NNodes'],1)

    def testResourceInfoNothingWorked(self):
        """ Test that we if we cannot get info, the  default values are used."""

# we set SIMEX_MPICOMMAND so that it call return error
        os.environ["SIMEX_MPICOMMAND"]='blabla'

        resource = ParallelUtilities.getParallelResourceInfo()

        self.assertEqual(resource['NCores'],0)
        self.assertEqual(resource['NNodes'],1)

        del os.environ["SIMEX_MPICOMMAND"]


    def testResourceInfoFromSimexWorks(self):
        """ Test we can set resource info via environment variables."""
        os.environ["SIMEX_NNODES"]='1'
        os.environ["SIMEX_NCORES"]='1'

        resource = ParallelUtilities.getParallelResourceInfo()
        
        self.assertEqual( resource['NCores'],1)
        self.assertEqual( resource['NNodes'],1)

        os.environ["SIMEX_NNODES"]='-1'
        os.environ["SIMEX_NCORES"]='-1'

        self.assertRaises( IOError, ParallelUtilities.getParallelResourceInfo)

    def testResourceInfoFromSlurm_WorksForSingleNode(self):
        """ Test we can get resource info from SLURM for a single node."""
        os.environ['SLURM_JOB_NUM_NODES']='1'
        os.environ['SLURM_JOB_CPUS_PER_NODE']='40'

        resource = ParallelUtilities.getParallelResourceInfo()

        self.assertEqual( resource['NCores'],40)
        self.assertEqual( resource['NNodes'],1)

    def testResourceInfoFromSlurm_WorksForMultipleNodeWithSameAmountOfCores(self):
        """ Test we can get resource info from SLURM for multiple homogeneous nodes."""
        os.environ['SLURM_JOB_NUM_NODES']='3'
        os.environ['SLURM_JOB_CPUS_PER_NODE']='40x(3)'

        resource = ParallelUtilities.getParallelResourceInfo()

        self.assertEqual( resource['NCores'],120)
        self.assertEqual( resource['NNodes'],3)

    def testResourceInfoFromSlurm_WorksForMultipleNodeWithDifferentAmountOfCores(self):
        """ Test we can get resource info from SLURM for multiple heterogeneous nodes."""
        os.environ['SLURM_JOB_NUM_NODES']='3'
        os.environ['SLURM_JOB_CPUS_PER_NODE']='40x(2),20x(1),10x(10)'

        resource = ParallelUtilities.getParallelResourceInfo()

        self.assertEqual(resource['NCores'],200)
        self.assertEqual(resource['NNodes'],3)

    def testGetVersionInfo_ReturnsCorrectData(self):
        """ Test we can extract MPI version infromation."""

        version=ParallelUtilities._getMPIVersionInfo()

        self.assertIn('Vendor',version)
        self.assertIn('Version',version)
        self.assertIn(version['Vendor'],["OpenMPI","MPICH"])

        self.assertIsInstance(version['Version'],str)
        self.assertGreater(StrictVersion(version['Version']),StrictVersion("0.0.0"))

    def testMPICommandArguments_ExceptionWhenCannotDefine(self):
        """ Test we get exception when we cannot setup mpirun arguments."""
        os.environ["SIMEX_MPICOMMAND"]='blabla'

        self.assertRaises(IOError,ParallelUtilities.prepareMPICommandArguments,1)

        del os.environ["SIMEX_MPICOMMAND"]


    def testVendorSpecificMPIArguments_OpenMPIOldVersion(self):
        """ Test mpirun arguments for OpenMPi are set correctly for old version."""
        version=dict([("Vendor", "OpenMPI"),("Version",'1.6.0')])

        str=ParallelUtilities._getVendorSpecificMPIArguments(version,1)
        self.assertEqual(str," --bynode -x OMP_NUM_THREADS=1 -x OMPI_MCA_mpi_warn_on_fork=0 -x OMPI_MCA_btl_base_warn_component_unused=0")

    def testVendorSpecificMPIArguments_OpenMPINewVersion(self):
        """ Test mpirun arguments for OpenMPI are set correctly for new version."""
        version=dict([("Vendor", "OpenMPI"),("Version",'1.9.0')])

        str=ParallelUtilities._getVendorSpecificMPIArguments(version,1)
        self.assertEqual(str," --map-by node --bind-to none -x OMP_NUM_THREADS=1 -x OMPI_MCA_mpi_warn_on_fork=0 -x OMPI_MCA_btl_base_warn_component_unused=0")


    def testVendorSpecificMPIArguments_MPICH(self):
        """ Test mpirun arguments for MPICH are set correctly."""
        version=dict([("Vendor", "MPICH"),("Version",'1.9.0')])

        str=ParallelUtilities._getVendorSpecificMPIArguments(version,1)
        self.assertEqual(str," -map-by node -env OMP_NUM_THREADS 1")

    def testVendorSpecificMPIArguments_UseAllThreads(self):
        """ Test we don't set OMP_NUM_THREADS by default"""

        version=dict([("Vendor", "OpenMPI"),("Version",'1.6.0')])

        str=ParallelUtilities._getVendorSpecificMPIArguments(version,0)
        self.assertNotIn("OMP_NUM_THREADS",str)

    def testVendorSpecificMPIArguments_Exception_OnNoneVersion(self):
        """ Test we get exception when MPI version is not defined"""
        version=None
        self.assertRaises(IOError,ParallelUtilities._getVendorSpecificMPIArguments,version,0)

    def testPrepareMPICommandArguments_Exception_OnNegativeNTasks(self):
        """ Test we get exception on negative number of tasks"""
        self.assertRaises(IOError,ParallelUtilities.prepareMPICommandArguments,-1,0)

    def testPrepareMPICommandArguments_Adds_NumberOfTasks(self):
        """ Test we correctly set number of tasks"""
        self.assertIn("-np 10",ParallelUtilities.prepareMPICommandArguments(10,0))

    def testPrepareMPICommandArguments_Adds_ExtraMPIParameters(self):
        """ Test we correctly use SIMEX_EXTRA_MPI_PARAMETERS environment variable"""
        os.environ["SIMEX_EXTRA_MPI_PARAMETERS"]='blabla'

        self.assertIn("blabla",ParallelUtilities.prepareMPICommandArguments(10,0))

        del os.environ["SIMEX_EXTRA_MPI_PARAMETERS"]



if __name__ == '__main__':
    unittest.main()
