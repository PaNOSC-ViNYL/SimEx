""" :module DetectorGeometry: Module holding the DetectorGeometry class. """
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

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance

class DetectorPanel(object):
    """ Class representing one detector panel (contiguous array of pixels, i.e. not separated by gaps).  """

    def __init__(self,
            dimensions=None,
            ranges=None,
            pixel_size=None,
            adu_per_eV=None,
            adu_per_photon=None,
            badrow_direction=None,
            distance_from_interaction_plane=None,
            distance_offset=None,
            fast_scan_xyz=None,
            slow_scan_xyz=None,
            corners=None,
            saturation_adu=None,
            mask=None,
            good_bit_mask=None,
            bad_bit_mask=None,
            saturation_map=None,
            badregion_flag=None,
            **kwargs
            ):
        """
        Constructor of the DetectorPanel.

        :param <++>: <++>
        :type  <++>: <++>

        """
        pass

class DetectorGeometry(AbstractCalculatorParameters):
    """ Class representing the detector geometry. """

    def __init__(self,
            panels=None,
            **kwargs
            ):
        """
        Constructor of the DetectorGeometry class.

        :param panels: Single or list of detector panels that constitute the detector.
        :type  panels: list, tuple, or instance of DetectorPanel

        :param kwargs: Key-value pairs to be passed to the parent class constructor.
        :type kwargs: dict

        """

        super(DetectorGeometry, self).__init__(**kwargs)

        self.panels = panels

    @property
    def panels(self):
        return self.__panels
    @panels.setter
    def panels(self, val):
        # Check if single instance, convert to list if true.
        if not isinstance(val, (list, tuple)):
            val = [val]
        if not all([isinstance(v, DetectorPanel) for v in val]):
            raise TypeError( "Parameter 'panels' must be a list of instances, tuple of instances, or a single instance of the  DetectorPanel class.")
        self.__panels = val

    def _setDefaults(self):
        """ Set default for required inherited parameters. """
        self._AbstractCalculatorParameters__cpus_per_task_default = 1
