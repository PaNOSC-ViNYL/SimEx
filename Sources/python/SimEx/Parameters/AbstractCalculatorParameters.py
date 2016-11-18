##########################################################################
#                                                                        #
# Copyright (C) 2015 Carsten Fortmann-Grote                              #
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

""" Module for AbstractCalculatorParameters class

    @author : CFG
    @institution : XFEL
    @creation 20160219

"""
from abc import ABCMeta, abstractmethod

from SimEx.Utilities.EntityChecks import checkAndSetPositiveInteger, checkAndSetInstance


class AbstractCalculatorParameters(object):
    """
    Abstract class for all calculator parameters.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, cpus_per_task=None, forced_mpi_command=None, parameters_dict=None, **kwargs):
        """
        Constructor for the Abstract Calculator Parameters.

        :param cpus_per_task: How many CPUs per simulation task to request from the compute environment.
        :type cpus_per_task: (int | str)
        :note cpus_per_task: Only "MAX" is accepted as a str.

        :param forced_mpi_command: Overrides the default system command to launch an mpi calculation. Default "".
        :type forced_mpi_command: str

        :parameters_dict: Dictionary of parameters.
        :type parameters_dict: dict

        :param **kwargs:  key=value pairs for further calculator specific parameters.
        """

        # Check and set parameters.
        self.cpus_per_task = cpus_per_task
        self.forced_mpi_command = forced_mpi_command

    # Queries and
    @property
    def cpus_per_task(self):
        """ Query for the number of cpus per task. """
        return self.__cpus_per_task

    @cpus_per_task.setter
    def cpus_per_task(self, value):
        """ Set the number of cpus per task."""
        self.__cpus_per_task = _checkAndSetCPUsPerTask(value)

    @property
    def forced_mpi_command(self):
        """ Query for the number of cpus per task. """
        return self.__forced_mpi_command

    @forced_mpi_command.setter
    def forced_mpi_command(self, value):
        """ Set the number of cpus per task."""
        self.__forced_mpi_command = _checkAndSetForcedMPICommand(value)

def _checkAndSetCPUsPerTask(value=None):
    """ """
    """ Utility function to check validity of input for number of cpus per task.

    :param value: The value to check.
    :type value: (int | str)

    :return: The checked value, default 1.
    """

    # Check type
    if isinstance(value, str):
        if not value == "MAX":
            raise ValueError( 'cpus_per_task must be a positive integer or string "MAX".')
        return value

    return checkAndSetPositiveInteger(value, 1)

def _checkAndSetForcedMPICommand(value):
    """ """
    """ Utility function to check validity of input for forced MPI command.

    :param value: The value to check.
    :type value: str
    """

    return checkAndSetInstance( str, value, "")

