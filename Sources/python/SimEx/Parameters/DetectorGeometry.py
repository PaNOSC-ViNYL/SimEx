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

import numpy

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.Units import Metre, ElectronVolt
from SimEx.Utilities.EntityChecks import checkAndSetInstance, checkAndSetIterable, checkAndSetNumber
from SimEx import PhysicalQuantity

class DetectorPanel(object):
    """ Class representing one detector panel (contiguous array of pixels, i.e. not separated by gaps).  """

    def __init__(self,
            dimensions                      = None,
            ranges                          = None,
            pixel_size                      = None,
            adu_response                    = None,
            badrow_direction                = None,
            distance_from_interaction_plane = None,
            distance_offset                 = None,
            fast_scan_xyz                   = None,
            slow_scan_xyz                   = None,
            corners                         = None,
            saturation_adu                  = None,
            mask                            = None,
            good_bit_mask                   = None,
            bad_bit_mask                    = None,
            saturation_map                  = None,
            badregion_flag                  = None,
            **kwargs
            ):
        """
        Constructor of the DetectorPanel.

        :param dimensions: The dimensions of the panel: Tuple or list with two or three elements indicating the scan axis of the detector data.
        :type  dimensions: list or tuple
        :example dimensions: ['fs','ss'] # first axis is fast scan, second axis is slow scan
        :example dimensions: ['event', 'ss', 'fs'] # first axis encodes event number scan, second axis encodes slow scan, third axis encodes fast scan.

        :param ranges: The minimum and maximum values pixel numbers on the respective transverse axis.
        :type  ranges: List of tuples or tuple of tuples.
        :example ranges: [[11,20],[1,20]] # First axis from 11 to 20 and second axis from 1 to 20.

        :param pixel_size: The physical size of the pixel (assuming quadratic shape) (SI units).
        :type  pixel_size: PhysicalQuantity with unit Metre.

        :param adu_response: Number of detector units (ADU) arising from one eV or one photon (depending on the unit).
        :type  adu_response: PhysicalQuantity with unit 1/eV (adu_per_eV) or float (adu_per_photon).

        :param badrow_direction: Direction in which to apply a bad row (x || y).
        :type  badrow_direction: str

        :param distance_from_interaction_plane: Distance in z of this panel from the plane of interaction (transverse plane that contains the sample).
        :type  distance_from_interaction_plane: PhysicalQuantity with unit Metre.

        :param distance_offset: Offset from distance_from_interaction_plane.
        :type  distance_offset: PhysicalQuantity with unit Metre.

        :param fast_scan_xyz: Formula that lab frame coordinates to panel axes.
        :type  fast_scan_xyz: str

        :param slow_scan_xyz: Formula that lab frame coordinates to panel axes.
        :type  slow_scan_xyz: str

        :param corners: [x,y] coordinates of lower left pixel of this panel in the globale detector geometry.
        :type  corners: list, tuple

        :param saturation_adu: Saturation level for this panel.
        :type  saturation_adu: float.

        :param mask: Mask to apply to this panel.
        :type  mask: numpy.array of same shape as panel data.

        :param good_bit_mask: Bitmask indicating the good pixels
        :type  good_bit_mask: ???

        :param bad_bit_mask: Bitmask indicating the bad pixels.
        :type  bad_bit_mask: ???

        :param saturation_map: Pixel map indicating saturated pixels.
        :type  saturation_map: numpy.array of same shape as panel data.

        :param badregion_flag: Flag to indicate this panel as a bad region.
        :type  badregion_flag: bool

        """

        # Store on object using setters.
        self.dimensions                      = dimensions
        self.ranges                          = ranges
        self.pixel_size                      = pixel_size
        self.adu_response                    = adu_response
        self.badrow_direction                = badrow_direction
        self.distance_from_interaction_plane = distance_from_interaction_plane
        self.distance_offset                 = distance_offset
        self.fast_scan_xyz                   = fast_scan_xyz
        self.slow_scan_xyz                   = slow_scan_xyz
        self.corners                         = corners
        self.saturation_adu                  = saturation_adu
        self.mask                            = mask
        self.good_bit_mask                   = good_bit_mask
        self.bad_bit_mask                    = bad_bit_mask
        self.saturation_map                  = saturation_map
        self.badregion_flag                  = badregion_flag


    ### Query and set methods.
    # dimensions
    @property
    def dimensions(self):
        """ Query the panel dimensions. """
        return self.__dimensions
    @dimensions.setter
    def dimensions(self, val):
        """ Set the panel dimensions. """
        self.__dimensions = checkAndSetIterable( val, ["ss","fs"] )

    # ranges
    @property
    def ranges(self):
        """ Query the panel ranges. """
        return self.__ranges
    @ranges.setter
    def ranges(self, val):
        """ Set the panel ranges. """
        self.__ranges = checkAndSetIterable( val, None )

    # pixel_size
    @property
    def pixel_size(self):
        """ Query the panel pixel_size. """
        return self.__pixel_size
    @pixel_size.setter
    def pixel_size(self, val):
        """ Set the panel pixel_size. """
        self.__pixel_size = checkAndSetInstance( PhysicalQuantity,  val, 1.0e-4*Metre)

    # adu_response
    @property
    def adu_response(self):
        """ Query the panel adu_response. """
        return self.__adu_response
    @adu_response.setter
    def adu_response(self, val):
        """ Set the panel adu_response. """
        if isinstance(val, PhysicalQuantity):
            val = checkAndSetInstance( PhysicalQuantity, val, 1.0/ElectronVolt )
            self.__adu_per_eV = val
            self.__adu_response = val
            self.__adu_per_photon = None
        else:
            val = checkAndSetNumber( val, 1.0 )
            self.__adu_per_photon = val
            self.__adu_response = val
            self.__adu_per_eV = None

    # badrow_direction
    @property
    def badrow_direction(self):
        """ Query the panel badrow_direction. """
        return self.__badrow_direction
    @badrow_direction.setter
    def badrow_direction(self, val):
        """ Set the panel badrow_direction. """
        if val is not None:
            val = checkAndSetInstance( str, val  )
        else:
            val = None
        self.__badrow_direction = val

    # distance_from_interaction_plane
    @property
    def distance_from_interaction_plane(self):
        """ Query the panel distance_from_interaction_plane. """
        return self.__distance_from_interaction_plane
    @distance_from_interaction_plane.setter
    def distance_from_interaction_plane(self, val):
        """ Set the panel distance_from_interaction_plane. """
        self.__distance_from_interaction_plane = checkAndSetInstance( PhysicalQuantity, val, 0.1*Metre )

    # distance_offset
    @property
    def distance_offset(self):
        """ Query the panel distance_offset. """
        return self.__distance_offset
    @distance_offset.setter
    def distance_offset(self, val):
        """ Set the panel distance_offset. """
        self.__distance_offset = checkAndSetInstance( PhysicalQuantity, val, 0.0*Metre )

    # fastscan_xyz
    @property
    def fast_scan_xyz(self):
        """ Query the panel fast_scan_xyz. """
        return self.__fast_scan_xyz
    @fast_scan_xyz.setter
    def fast_scan_xyz(self, val):
        """ Set the panel fast_scan_xyz. """
        self.__fast_scan_xyz = checkAndSetInstance( str, val, "1.0*x" )

    # slow_scan_xyz
    @property
    def slow_scan_xyz(self):
        """ Query the panel slow_scan_xyz. """
        return self.__slow_scan_xyz
    @slow_scan_xyz.setter
    def slow_scan_xyz(self, val):
        """ Set the panel slow_scan_xyz. """
        self.__slow_scan_xyz = checkAndSetInstance( str, val, "1.0*y" )

    # cornes
    @property
    def cornes(self):
        """ Query the panel cornes. """
        return self.__cornes
    @cornes.setter
    def corners(self, val):
        """ Set the panel cornes. """
        self.__cornes = checkAndSetIterable( val, [0.0,0.0] )

    # saturation_adu
    @property
    def saturation_adu(self):
        """ Query the panel saturation_adu. """
        return self.__saturation_adu
    @saturation_adu.setter
    def saturation_adu(self, val):
        """ Set the panel saturation_adu. """
        self.__saturation_adu = checkAndSetNumber( val, 1.0e4 )

    # mask
    @property
    def mask(self):
        """ Query the panel mask. """
        return self.__mask
    @mask.setter
    def mask(self, val):
        """ Set the panel mask. """
        self.__mask = checkAndSetInstance( numpy.array, None )

    # good_bit_mask
    @property
    def good_bit_mask(self):
        """ Query the panel good_bit_mask. """
        return self.__good_bit_mask
    @good_bit_mask.setter
    def good_bit_mask(self, val):
        """ Set the panel good_bit_mask. """
        self.__good_bit_mask = checkAndSetInstance( int, None )

    # bad_bit_mask
    @property
    def bad_bit_mask(self):
        """ Query the panel bad_bit_mask. """
        return self.__bad_bit_mask
    @bad_bit_mask.setter
    def bad_bit_mask(self, val):
        """ Set the panel bad_bit_mask. """
        self.__bad_bit_mask = checkAndSetInstance( int, val, None )

    # saturation_map
    @property
    def saturation_map(self):
        """ Query the panel saturation_map. """
        return self.__saturation_map
    @saturation_map.setter
    def saturation_map(self, val):
        """ Set the panel saturation_map. """
        self.__saturation_map = checkAndSetInstance( numpy.array, val, None )

    # badregion_flag
    @property
    def badregion_flag(self):
        """ Query the panel badregion_flag. """
        return self.__badregion_flag
    @badregion_flag.setter
    def badregion_flag(self, val):
        """ Set the panel badregion_flag. """
        self.__badregion_flag = checkAndSetInstance( bool, val, False )

    ## XXX
    #@property
    #def XXX(self):
        #""" Query the panel XXX. """
        #return self.__XXX
    #@XXX.setter
    #def XXX(self, val):
        #""" Set the panel XXX. """
        #self.__XXX = checkAndSetIterable( val, ["ss","fs"] )
    ## XXX
    #@property
    #def XXX(self):
        #""" Query the panel XXX. """
        #return self.__XXX
    #@XXX.setter
    #def XXX(self, val):
        #""" Set the panel XXX. """
        #self.__XXX = checkAndSetIterable( val, ["ss","fs"] )

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
