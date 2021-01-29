""" :module GromacsPhotonMatterInteractorParameters: Module that holds the GromacsPhotonMatterInteractorParameters class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2020, 2021 Ibrahim Dawod, Juncheng E                     #
# Contact:                                                               #
#       Ibrahim Dawod <ibrahim.dawod@physics.uu.se>                      #
#       Juncheng E <juncheng.e@xfel.eu>                                  #
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
###########################################################################

import numbers

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters


class GromacsPhotonMatterInteractorParameters(AbstractCalculatorParameters):
    """
    :class GromacsPhotonMatterInteractorParameters: Encapsulates parameters for the GromacsPhotonMatterInteractor calculator.
    """
    def __init__(self, rotations=None, pulse_indices=None, **kwargs):
        """
        :param rotation: Rotation list of quaternions to apply to the sample atoms' positions (Default: no rotation).
        :type random_rotation: List of 4-elements tuple giving the four coordinates of the rotation quaternion.

        :param pulse_indieces: Identify which X-ray pulses to include in the analysis (default "all").
        :type pulse_indieces: int || sequence of int || "all"
        :example pulse_indices: pulse_indices=1\n
                                  pulse_indices=[1,2,3]\n
                                  pulse_indices=range(1,10)\n
                                  pulse_indices="all"

        :param forced_mpi_command: User-defined mpi command for running the backengine (default "None").
        :type forced_mpi_command: str
        :example forced_mpi_command: "mpirun -np 4"
        """

        # Check all parameters.
        self.rotations = rotations
        self.pulse_indices = pulse_indices

        # Call the __init__ function in the super class.
        # forced_mpi_command is handled in the super class.
        super().__init__(**kwargs)

    def _setDefaults(self):
        """ Set default for required inherited parameters. """
        self._AbstractCalculatorParameters__cpus_per_task_default = 1

    @property
    def rotations(self):
        """ Query for the 'rotation' parameter. """
        return self.__rotations

    @rotations.setter
    def rotations(self, value):
        """ Set the 'rotations' parameter to a given value.
        :param value: The value to set 'rotation' to.
        """
        # Allow None.
        if value is None:
            value = [(1, 0, 0, 0)]

        # Convert single quaternion into a list
        if len(value) == 4 and all([isinstance(i, numbers.Number) for i in value]):
            value = [value]

        # Check all conditions.
        conditions = [
            hasattr(value, '__iter__'),
            len(value) > 0,
            all(len(q) == 4 for q in value),
            all([isinstance(i, numbers.Number) for i in value[0]])
        ]

        if not all(conditions):
            raise TypeError(
                "Rotations must be None or a list or tuple of quaternion(s). Example: [(1,0,0,0)]"
            )

        self.__rotations = value

    @property
    def pulse_indices(self):
        """ Query pattern indices attribute. """
        return self.__pulse_indices

    @pulse_indices.setter
    def pulse_indices(self, pulse_indices):
        """ Set the pattern indices. """

        indices = pulse_indices
        if indices is None:
            indices = 'all'

        if not (isinstance(indices, int) or indices == 'all'
                or hasattr(indices, '__iter__')):
            raise TypeError(
                'The parameter "pulse_indices" must be an int, iterable over ints, or "all".'
            )

        # Convert int to list.
        if isinstance(pulse_indices, int):
            indices = [pulse_indices]

        self.__pulse_indices = indices
