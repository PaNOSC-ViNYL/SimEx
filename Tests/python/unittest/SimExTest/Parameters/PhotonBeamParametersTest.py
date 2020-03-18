""" :module PhotonBeamParametersTest: Test module for the PhotonBeamParameters class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2016-2017 Carsten Fortmann-Grote                         #
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

import os
import shutil
import io

# Include needed directories in sys.path.
import unittest

from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Parameters.PhotonBeamParameters import propToBeamParameters
from SimEx.Utilities.Units import meter, electronvolt, joule, radian
from TestUtilities import TestUtilities

class PhotonBeamParametersTest(unittest.TestCase):
    """
    Test class for the PhotonBeamParameters class.
    """

    @classmethod
    def setUpClass(cls):
        cls.beam = PhotonBeamParameters(photon_energy=8.6e3*electronvolt,
                                    beam_diameter_fwhm=1.0e-6*meter,
                                    pulse_energy=1.0e-3*joule,
                                    photon_energy_relative_bandwidth=0.001,
                                    divergence=None,
                                    photon_energy_spectrum_type="SASE",
                                    )
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

    def testDefaultConstruction(self):
        """ Testing the default construction. """

        # Attempt to construct an instance of the class.
        self.assertRaises(TypeError, PhotonBeamParameters)

    def testShapedConstruction(self):
        """ Testing the construction of the class with parameters. """

        # Attempt to construct an instance of the class.
        parameters = PhotonBeamParameters(
                photon_energy=4.96e3*electronvolt,
                photon_energy_relative_bandwidth=2e-2,
                photon_energy_spectrum_type="SASE",
                pulse_energy = 2e-3*joule,
                beam_diameter_fwhm = 2e-6*meter,
                divergence = 1e-6*radian,
                )

        # Check all parameters are set as intended.
        self.assertEqual( parameters.photon_energy, 4.96e3*electronvolt )
        self.assertEqual( parameters.photon_energy_relative_bandwidth, 2e-2 )
        self.assertEqual( parameters.photon_energy_spectrum_type, "SASE" )
        self.assertEqual( parameters.pulse_energy, 2e-3*joule )
        self.assertEqual( parameters.beam_diameter_fwhm, 2e-6*meter )
        self.assertEqual( parameters.divergence, 1e-6*radian )

    def testSettersAndQueries(self):
        """ Testing the default construction of the class using a dictionary. """
        # Attempt to construct an instance of the class.
        parameters = PhotonBeamParameters(
                photon_energy=4.96e3*electronvolt,
                pulse_energy = 2e-3*joule,
                beam_diameter_fwhm = 2e-6*meter,
                )

        # Set via methods.
        parameters.photon_energy = 8.0e3*electronvolt
        parameters.pulse_energy = 2.5e-3*joule
        parameters.beam_diameter_fwhm = 100e-9*meter
        parameters.photon_energy_relative_bandwidth = 1e-3
        parameters.divergence = 5e-6*radian
        parameters.photon_energy_spectrum_type="tophat"

        # Check all parameters are set as intended.
        self.assertEqual( parameters.photon_energy, 8.0e3*electronvolt )
        self.assertEqual( parameters.photon_energy_relative_bandwidth, 1e-3 )
        self.assertEqual( parameters.pulse_energy.magnitude, 2.5e-3 )
        self.assertEqual( parameters.beam_diameter_fwhm.magnitude, 1e-7 )
        self.assertEqual( parameters.divergence.magnitude, 5e-6 )
        self.assertEqual( parameters.photon_energy_spectrum_type, "tophat" )

    def testSerializeToFileName(self):
        """ Test the serialization of a PhotonBeamParameters instance to file given the filename. """

        parameters = self.beam

        # Setup IO file and cleanup.
        ofile = 'tmp.beam'
        self.__files_to_remove.append(ofile)

        parameters.serialize(stream=ofile)

        reference_serial = """; [Photon beam parameters]

; photon energy (eV)
beam/photon_energy = 8.6000000e+03

; Number of photons per pulse
beam/fluence = 7.2575687e+11

; Radius of X-ray beam (m)
beam/radius = 5.0000000e-07
"""

        with open(ofile, 'r') as stream:
            serial = "".join(stream.readlines())

        self.assertEqual( serial, reference_serial )


    def testSerializeToFile(self):
        """ Test the serialization of a PhotonBeamParameters instance to file. """

        parameters = self.beam

        # Setup IO file and cleanup.
        ofile = 'tmp.beam'
        self.__files_to_remove.append(ofile)

        with open(ofile,'w') as  stream:
            parameters.serialize(stream=stream)

        reference_serial = """; [Photon beam parameters]

; photon energy (eV)
beam/photon_energy = 8.6000000e+03

; Number of photons per pulse
beam/fluence = 7.2575687e+11

; Radius of X-ray beam (m)
beam/radius = 5.0000000e-07
"""

        with open(ofile, 'r') as stream:
            serial = "".join(stream.readlines())

        self.assertEqual( serial, reference_serial )


    def testSerialize(self):
        """ Test the serialization of a PhotonBeamParameters instance. """
        parameters = self.beam

        stream = io.StringIO()
        parameters.serialize(stream=stream)


        reference_serial = """; [Photon beam parameters]

; photon energy (eV)
beam/photon_energy = 8.6000000e+03

; Number of photons per pulse
beam/fluence = 7.2575687e+11

; Radius of X-ray beam (m)
beam/radius = 5.0000000e-07
"""

        self.assertEqual( stream.getvalue(), reference_serial)

        stream.close()

    def testPropToBeamParameters(self):
        """ Test the utility function to construct a PhotonBeamParameters instance from prop output (wavefront file). """

        beam_parameters = propToBeamParameters(TestUtilities.generateTestFilePath("prop_out/prop_out_0000011.h5"))

        self.assertIsInstance( beam_parameters, PhotonBeamParameters )
        self.assertAlmostEqual( beam_parameters.photon_energy.magnitude,
                4972.065708*electronvolt.magnitude, 5 )
if __name__ == '__main__':
    unittest.main()

