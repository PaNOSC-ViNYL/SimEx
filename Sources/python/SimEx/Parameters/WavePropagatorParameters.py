""" :module WavePropagatorParameters: Module that holds the WavePropagatorParameters class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2016-2020 Carsten Fortmann-Grote                         #
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

import prop.exfel_spb_kb_beamline as default_beamline

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance

class WavePropagatorParameters(AbstractCalculatorParameters):
    """
    :class WavePropagatorParameters: Class representing parameters for the WavePropagator.
    """

    def __init__(self,
                 use_opmd = None,
                 beamline = None,
                 **kwargs
                ):
        """
        :param use_opmd: Whether to use the openPMD output format.
        :type use_opmd: bool, default False

        :param beamline: The WPG beamline to use in the propagation.
        :type beamline: WPG.Beamline instance.
        """

        # Check all parameters.
        self.use_opmd = use_opmd
        self.beamline = beamline

        # Initialize base class.
        super(WavePropagatorParameters, self).__init__(**kwargs)

    def _setDefaults(self):
        """ Sets defaults for parameters that must be defined. """
        self._AbstractCalculatorParameters__cpus_per_task_default = "MAX"

    ### Setters and queries.
    @property
    def use_opmd(self):
        """ Query for the 'use_opmd' parameter. """
        return self.__use_opmd
    @use_opmd.setter
    def use_opmd(self, value):
        """ Set the 'use_opmd' parameter to a given value.
        @param value : The value to set 'use_opmd' to.
        """
        self.__use_opmd = checkAndSetInstance( bool, value, False )

    @property
    def beamline(self):
        """ Query for the 'beamline' parameter. """
        return self.__beamline
    @beamline.setter
    def beamline(self, value):
        """ Set the 'beamline' parameter.
        @param value : The value to set 'beamline' to.
        """
        if value is None:
            value = default_beamline
        if not hasattr(value, "get_beamline"):
            raise AttributeError('The beamline module must define a function "get_beamline()".')

        # Ok, store on object.
        self.__beamline = value
