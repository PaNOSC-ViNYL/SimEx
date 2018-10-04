""" :module  AbstractPhotonDiffractorParameters: Hosts the abstract base class for all PhotonDiffractors."""
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

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance
from SimEx.Utilities import IOUtilities
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters

class AbstractPhotonDiffractorParameters(AbstractCalculatorParameters):
    """
    :class AbstractPhotonDiffractorParameters: Abstract base class for all PhotonDiffractors.
    """
    def __init__(self,
                sample=None,
                uniform_rotation=None,
                number_of_diffraction_patterns=None,
                beam_parameters=None,
                geometry=None,
                **kwargs
                ):
        """
        :param sample: Location of file that contains the sample definition (pdb or crystfel format)
        :type sample: str

        :param uniform_rotation: Whether to perform uniform sampling of rotation space.
        :type uniform_rotation: bool, default True

        :param number_of_diffraction_patterns: Number of diffraction patterns to calculate from each trajectory.
        :type number_of_diffraction_patterns: int, default 1

        :param beam_parameters: Path of the beam parameter file.
        :type beam_parameters: str

        :param geometry: Path of the beam geometry file.
        :type geometry: str

        :param kwargs: Key-value pairs to pass to the parent class.
        """


        # Check all parameters.
        self.sample = sample
        self.uniform_rotation = uniform_rotation
        self.beam_parameters = beam_parameters
        self.geometry = geometry
        self.number_of_diffraction_patterns = number_of_diffraction_patterns

        super(AbstractPhotonDiffractorParameters, self).__init__(**kwargs)

    def _setDefaults(self):
        """ Set default for required inherited parameters. """
        self._AbstractCalculatorParameters__cpus_per_task_default = 1

    ### Setters and queries.
    @property
    def sample(self):
        """ Query the 'sample' parameter. """
        return self.__sample
    @sample.setter
    def sample(self, val):
        """ Set the 'sample' parameter to val."""
        if val is None:
            raise ValueError( "A sample must be defined.")
        if val.split(".")[-1] == "pdb":
            self.__sample = IOUtilities.checkAndGetPDB(val)

    @property
    def uniform_rotation(self):
        """ Query for the 'uniform_rotation' parameter. """
        return self.__uniform_rotation
    @uniform_rotation.setter
    def uniform_rotation(self, value):
        """ Set the 'uniform_rotation' parameter to a given value.
        :param value: The value to set 'uniform_rotation' to.
        """
        self.__uniform_rotation = checkAndSetInstance( bool, value, True )

    @property
    def beam_parameters(self):
        """ Query for the 'beam_parameters' parameter. """
        return self.__beam_parameters
    @beam_parameters.setter
    def beam_parameters(self, value):
        """ Set the 'beam_parameters' parameter to a given value.
        :param value: The value to set 'beam_parameters' to.
        """
        if value is None:
            print ("WARNING: Beam parameters not set, will use crystFEL/pattern_sim defaults.")

        self.__beam_parameters = checkAndSetInstance( (str, PhotonBeamParameters), value, None )

        if isinstance(self.__beam_parameters, str):
            if not os.path.isfile( self.__beam_parameters):
                raise IOError("The beam_parameters %s is not a valid file or filename." % (self.__beam_parameters) )

    @property
    def geometry(self):
        """ Query for the 'geometry' parameter. """
        return self.__geometry
    @geometry.setter
    def geometry(self, value):
        """ Set the 'geometry' parameter to a given value.
        :param value: The value to set 'geometry' to.
        """
        self.__geometry = checkAndSetInstance( str, value, None )

        if self.__geometry is not None:
            if not os.path.isfile( self.__geometry):
                raise IOError("The geometry %s is not a valid file or filename." % (self.__geometry) )
        else:
            print ("WARNING: Geometry file not set, calculation will most probably fail.")


    @property
    def number_of_diffraction_patterns(self):
        """ Query for the 'number_of_diffraction_patterns_file' parameter. """
        return self.__number_of_diffraction_patterns
    @number_of_diffraction_patterns.setter
    def number_of_diffraction_patterns(self, value):
        """ Set the 'number_of_diffraction_patterns' parameter to a given value.
        :param value: The value to set 'number_of_diffraction_patterns' to.
        """
        number_of_diffraction_patterns = checkAndSetInstance( int, value, 1 )

        if number_of_diffraction_patterns > 0:
            self.__number_of_diffraction_patterns = number_of_diffraction_patterns
        else:
            raise ValueError("The parameters 'number_of_diffraction_patterns' must be a positive integer.")
