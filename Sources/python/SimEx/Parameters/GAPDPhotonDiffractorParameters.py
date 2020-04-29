""" :module GAPDPhotonDiffractorParameters: Module that holds the GAPDPhotonDiffractorParameters class.  """
##########################################################################
#
# Modified by Juncheng E in 2020                                         #
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
import warnings

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Parameters.DetectorGeometry import DetectorGeometry
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance


class GAPDPhotonDiffractorParameters(AbstractCalculatorParameters):
    """
    :class GAPDPhotonDiffractorParameters: Class representing parameters for the GAPDPhotonDiffractor calculator.
    """
    def __init__(self,
                 sample=None,
                 quaternion_rotation=None,
                 random_rotation=None,
                 uniform_rotation=None,
                 calculate_Compton=None,
                 slice_interval=None,
                 number_of_slices=None,
                 number_of_spectrum_bins=None,
                 number_of_diffraction_patterns=None,
                 beam_parameters=None,
                 detector_geometry=None,
                 number_of_MPI_processes=None,
                 parameters_dictionary=None,
                 **kwargs):
        """
        :param sample: Name of file containing atomic sample geometry (default None).
        :type sample: str

        :param quaternion_rotation: The rotation quaternion for sample rotation.
                                    quaternion_rotation = None: No rotation by quaternion
                                    quaternion_rotation = [0.1, 0.1, 0.1, 0.1]: Rotation by input quaternion
                                    It will conflict with `uniform_rotation` and `random_rotation`.
        :type quaternion_rotation: list, default None

        :param random_rotation: Whether to rotate the sample randomly. 
                                It will conflict with `uniform_rotation` and `quaternion_rotation`.
        :type random_rotation: bool, default False

        :param uniform_rotation: Uniform sampling of rotation space. 
                                 It will conflict with `quaternion_rotation` and `random_rotation`.
        :type uniform_rotation: bool, default Flase

        :param calculate_Compton: Whether to calculate incoherent (Compton) scattering.
        :type calculate_Compton: bool, default False

        :param slice_interval: Length of time slice interval to extract from each beam temporal profile.
        :type slice_interval: int, default 100

        :param number_of_slices: Number of time slices to read from each beam temproral profile.
        :type number_of_slices: int, default 1

        :param number_of_spectrum_bins: Number of spectrum bins to read from each beam spectrum.
        :type number_of_spectrum_bins: int, default 1

        :param number_of_diffraction_patterns: Number of diffraction patterns to calculate from each trajectory.
        :type number_of_diffraction_patterns: int, default 1

        :param beam_parameters: Path of the beam parameter file or DetectorGeometry object.
        :type beam_parameters: str or DetectorGeometry object

        :param detector_geometry: Path of the beam geometry file or PhotonBeamParameters object.
        :type detector_geometry: str or PhotonBeamParameters object

        :param number_of_MPI_processes: Number of MPI processes
        :type number_of_MPI_processes: int, default 1

        """
        # Check all parameters.
        self.sample = sample
        self.uniform_rotation = uniform_rotation
        self.random_rotation = random_rotation
        self.quaternion_rotation = quaternion_rotation
        self.calculate_Compton = calculate_Compton
        self.slice_interval = slice_interval
        self.number_of_slices = number_of_slices
        self.number_of_spectrum_bins = number_of_spectrum_bins
        self.beam_parameters = beam_parameters
        self.detector_geometry = detector_geometry
        self.number_of_diffraction_patterns = number_of_diffraction_patterns

        # super to access the methods of the base class.
        super(GAPDPhotonDiffractorParameters, self).__init__(**kwargs)

    def _setDefaults(self):
        """ Set default for required inherited parameters. """
        self._AbstractCalculatorParameters__cpus_per_task_default = 1

    ### Setters and queries.
    @property
    def sample(self):
        """ Query for the 'sample' parameter. """
        return self.__sample

    @sample.setter
    def sample(self, value):
        """ Set the 'sample' parameter to a given value.
        :param value: The value to set 'sample' to.
        """
        if value is not None:
            value = checkAndSetInstance(str, value, None)
        self.__sample = value

    @property
    def random_rotation(self):
        """ Query for the 'random_rotation' parameter. """
        return self.__random_rotation

    @random_rotation.setter
    def random_rotation(self, value):
        """ Set the 'random_rotation' parameter to a given value.
        :param value: The value to set 'random_rotation' to.
        """
        self.__random_rotation = checkAndSetInstance(bool, value, False)

    @property
    def quaternion_rotation(self):
        """ Query for the 'quaternion_rotation' parameter. """
        return self.__quaternion_rotation

    @quaternion_rotation.setter
    def quaternion_rotation(self, value):
        """ Set the 'quaternion_rotation' parameter to a given value.
        :param value: The value to set 'quaternion_rotation' to.
        """
        self.__quaternion_rotation = checkAndSetInstance((list, tuple),value, None)
                                                        
    @property
    def uniform_rotation(self):
        """ Query for the 'uniform_rotation' parameter. """
        return self.__uniform_rotation

    @uniform_rotation.setter
    def uniform_rotation(self, value):
        """ Set the 'uniform_rotation' parameter to a given value.
        :param value: The value to set 'uniform_rotation' to.
        """
        self.__uniform_rotation = checkAndSetInstance(bool, value, False)

    @property
    def calculate_Compton(self):
        """ Query for the 'calculate_Compton' parameter. """
        return self.__calculate_Compton

    @calculate_Compton.setter
    def calculate_Compton(self, value):
        """ Set the 'calculate_Compton' parameter to a given value.
        :param value: The value to set 'calculate_Compton' to.
        """
        self.__calculate_Compton = checkAndSetInstance(bool, value, False)

    @property
    def number_of_slices(self):
        """ Query for the 'number_of_slices' parameter. """
        return self.__number_of_slices

    @number_of_slices.setter
    def number_of_slices(self, value):
        """ Set the 'number_of_slices' parameter to a given value.
        :param value: The value to set 'number_of_slices' to.
        """
        number_of_slices = checkAndSetInstance(int, value, 1)

        if number_of_slices > 0:
            self.__number_of_slices = number_of_slices
        else:
            raise ValueError(
                "The parameter 'slice_interval' must be a positive integer.")

    @property
    def slice_interval(self):
        """ Query for the 'slice_interval' parameter. """
        return self.__slice_interval

    @slice_interval.setter
    def slice_interval(self, value):
        """ Set the 'slice_interval' parameter to a given value.
        :param value: The value to set 'slice_interval' to.
        """
        slice_interval = checkAndSetInstance(int, value, 100)

        if slice_interval > 0:
            self.__slice_interval = slice_interval
        else:
            raise ValueError(
                "The parameter 'slice_interval' must be a positive integer.")

    @property
    def number_of_spectrum_bins (self):
        """ Query for the 'number_of_spectrum_bins' parameter. """
        return self.__number_of_spectrum_bins

    @number_of_spectrum_bins.setter
    def number_of_spectrum_bins(self, value):
        """ Set the 'number_of_spectrum_bins' parameter to a given value.
        :param value: The value to set 'number_of_spectrum_bins' to.
        """
        number_of_spectrum_bins = checkAndSetInstance(int, value, 1)

        if number_of_spectrum_bins > 0:
            self.__number_of_spectrum_bins = number_of_spectrum_bins
        else:
            raise ValueError(
                "The parameter 'slice_interval' must be a positive integer.")

    @property
    def beam_parameters(self):
        """ Query for the 'beam_parameters' parameter. """
        return self.__beam_parameters

    @beam_parameters.setter
    def beam_parameters(self, value):
        """ Set the 'beam_parameters' parameter to a given value.
        :param value: The value to set 'beam_parameters' to.
        """
        value = checkAndSetInstance((str, PhotonBeamParameters), value, None)

        if isinstance(value, str):
            if not os.path.isfile(value):
                raise IOError(
                    "The beam_parameters %s is not a valid file or filename." %
                    (value))
            print ("Passing beam parameters as a tratracing_out file.")

        self.__beam_parameters = value

    @property
    def detector_geometry(self):
        """ Query for the 'detector_geometry' parameter. """
        return self.__detector_geometry

    @detector_geometry.setter
    def detector_geometry(self, value):
        """ Set the 'detector_geometry' parameter to a given value.
        :param value: The value to set 'detector_geometry' to.
        """
        if value is None:
            print(
                "WARNING: Geometry not set, calculation will most probably fail."
            )

        else:
            # Check if it is a DetectorGeometry object / string
            value = checkAndSetInstance((str, DetectorGeometry), value, None)

            if isinstance(value, str):
                if not os.path.isfile(value):
                    raise IOError(
                        'The parameter "detector_geometry" %s is not a valid file or filename.'
                        % (value))

                value = DetectorGeometry(filename=value)

        # Store on object and return.
        self.__detector_geometry = value

    @property
    def number_of_diffraction_patterns(self):
        """ Query for the 'number_of_diffraction_patterns_file' parameter. """
        return self.__number_of_diffraction_patterns

    @number_of_diffraction_patterns.setter
    def number_of_diffraction_patterns(self, value):
        """ Set the 'number_of_diffraction_patterns' parameter to a given value.
        :param value: The value to set 'number_of_diffraction_patterns' to.
        """
        number_of_diffraction_patterns = checkAndSetInstance(int, value, 1)

        if number_of_diffraction_patterns > 0:
            self.__number_of_diffraction_patterns = number_of_diffraction_patterns
        else:
            raise ValueError(
                "The parameters 'number_of_diffraction_patterns' must be a positive integer."
            )

    

