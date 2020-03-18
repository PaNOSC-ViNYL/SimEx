""" :module DetectorGeometry: Module holding the DetectorGeometry class. """
##########################################################################
#                                                                        #
# Copyright (C) 2015-2020 Carsten Fortmann-Grote                         #
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
from SimEx.AbstractBaseClass import AbstractBaseClass
from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance, checkAndSetNumber, checkAndSetPhysicalQuantity
from SimEx.Utilities.Units import meter, electronvolt

import numpy
import sys


class DetectorPanel(AbstractBaseClass):
    """:class DetectorPanel: Represents one detector panel (contiguous array of pixels, i.e. not separated by gaps).  """

    def __init__(self,
            ranges                          = None,
            pixel_size                      = None,
            energy_response                 = None,
            photon_response                 = None,
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
        :param ranges: The minimum and maximum values pixel numbers on the respective transverse axis.
        :type  ranges: Dictionary
        ":example ranges: {"fast_scan_min : 11, "fast_scan_max" : 20, "slow_scan_min" : 1, "fast_scan_max" : 20} # First axis from 11 to 20 and second axis from 1 to 20."

        :param pixel_size: The physical size of the pixel (assuming quadratic shape) (SI units).
        :type  pixel_size: PhysicalQuantity with unit meter.

        :param energy_response: Number of detector units (ADU) arising from one eV.
        :type  energy_response: PhysicalQuantity with unit 1/eV (adu_per_eV)

        :param photon_response: Number of detector units (ADU) arising from one photon.
        :type  photon_response: float

        :param distance_from_interaction_plane: Distance in z of this panel from the plane of interaction (transverse plane that contains the sample).
        :type  distance_from_interaction_plane: PhysicalQuantity with unit meter.

        :param distance_offset: Offset from distance_from_interaction_plane.
        :type  distance_offset: PhysicalQuantity with unit meter.

        :param fast_scan_xyz: Formula that lab frame coordinates to panel axes.
        :type  fast_scan_xyz: str

        :param slow_scan_xyz: Formula that lab frame coordinates to panel axes.
        :type  slow_scan_xyz: str

        :param corners: [x,y] coordinates of lower left pixel of this panel in the globale detector geometry.
        :type  corners: dict
        :example corners: corners={"x" : -10, "y" : 10 }

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

        # Handle case that neither photon nor energy response is set.
        self.__photon_response = 1.0
        self.__energy_response = None

        # Store on object using setters.
        self.ranges                          = ranges
        self.pixel_size                      = pixel_size
        self.energy_response                 = energy_response
        self.photon_response                 = photon_response
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

        self.number_of_pixels_fast = int(self.ranges["fast_scan_max"] - self.ranges["fast_scan_min"]) + 1
        self.number_of_pixels_slow = int(self.ranges["slow_scan_max"] - self.ranges["slow_scan_min"]) + 1

    ### Accessors.
    # ranges
    @property
    def ranges(self):
        """ Query the panel ranges. """
        return self.__ranges
    @ranges.setter
    def ranges(self, val):
        """ Set the panel ranges. """
        if val is None:
            raise ValueError( "The parameters 'ranges' must not be None." )
        self.__ranges = checkAndSetInstance( dict, val, None )

    # pixel_size
    @property
    def pixel_size(self):
        """ Query the panel pixel_size. """
        return self.__pixel_size
    @pixel_size.setter
    def pixel_size(self, val):
        """ Set the panel pixel_size. """
        self.__pixel_size = checkAndSetPhysicalQuantity( val, 1.0e-4*meter, meter)

    # energy_response
    @property
    def energy_response(self):
        """ Query the panel energy_response. """
        return self.__energy_response
    @energy_response.setter
    def energy_response(self, val):
        """ Set the panel energy_response. """
        if val is not None:
            val = checkAndSetPhysicalQuantity( val, None, 1./electronvolt)
        self.__energy_response = val

        # Invalidate photon response.
        if val is not None and self.__photon_response is not None:
            self.__photon_response = None

    # photon_response
    @property
    def photon_response(self):
        """ Query the panel photon_response. """
        return self.__photon_response
    @photon_response.setter
    def photon_response(self, val):
        """ Set the panel photon_response. """
        if val is not None:
            val = checkAndSetInstance( float, val, None)

        self.__photon_response = val

        # Invalidate energy response.
        if val is not None and self.__energy_response is not None:
            self.__energy_response = None

     # Distance_from_interaction_plane
    @property
    def distance_from_interaction_plane(self):
        """ Query the panel distance_from_interaction_plane. """
        return self.__distance_from_interaction_plane
    @distance_from_interaction_plane.setter
    def distance_from_interaction_plane(self, val):
        """ Set the panel distance_from_interaction_plane. """
        self.__distance_from_interaction_plane = checkAndSetPhysicalQuantity( val, 0.1*meter, meter )

    # distance_offset
    @property
    def distance_offset(self):
        """ Query the panel distance_offset. """
        return self.__distance_offset
    @distance_offset.setter
    def distance_offset(self, val):
        """ Set the panel distance_offset. """
        self.__distance_offset = checkAndSetPhysicalQuantity( val, 0.0*meter, meter)

    # fastscan_xyz
    @property
    def fast_scan_xyz(self):
        """ Query the panel fast_scan_xyz. """
        return self.__fast_scan_xyz
    @fast_scan_xyz.setter
    def fast_scan_xyz(self, val):
        """ Set the panel fast_scan_xyz. """
        self.__fast_scan_xyz = checkAndSetInstance( str, val, "1.0x" )

    # slow_scan_xyz
    @property
    def slow_scan_xyz(self):
        """ Query the panel slow_scan_xyz. """
        return self.__slow_scan_xyz
    @slow_scan_xyz.setter
    def slow_scan_xyz(self, val):
        """ Set the panel slow_scan_xyz. """
        self.__slow_scan_xyz = checkAndSetInstance( str, val, "1.0y" )

    # corners
    @property
    def corners(self):
        """ Query the panel cornes. """
        return self.__corners
    @corners.setter
    def corners(self, val):
        """ Set the panel corners. """
        self.__corners = checkAndSetInstance( dict, val, {"x" : 0.0, "y" : 0.0} )

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
        self.__mask = checkAndSetInstance( numpy.array, val, None )

    # good_bit_mask
    @property
    def good_bit_mask(self):
        """ Query the panel good_bit_mask. """
        return self.__good_bit_mask
    @good_bit_mask.setter
    def good_bit_mask(self, val):
        """ Set the panel good_bit_mask. """
        self.__good_bit_mask = checkAndSetInstance( int, val, None )

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
    ### End accessors

    def _serialize(self, stream=None, panel_id=None, caller=None):
        """ Serialize the panel.

        :param stream: The stream to write the serialized panel to.
        :type stream: file like (default sys.stdout)

        """
        # Check stream parameter.
        if stream is None:
            stream = sys.stdout

        if not hasattr(stream, "write"):
            raise IOError( "The given stream is not writable." )

        # Check panel_id parameter.
        panel_id = checkAndSetInstance( int, panel_id, 0 )

        # Get panel id as a string.
        panel_id_str = str(panel_id)

        # Initialize the string to be written to.
        serialization = ";panel %s\n" % (panel_id_str)
        serialization += "panel%s/min_fs         = %d\n" %  (panel_id_str, self.ranges["fast_scan_min"])
        serialization += "panel%s/max_fs         = %d\n" %  (panel_id_str, self.ranges["fast_scan_max"])
        serialization += "panel%s/min_ss         = %d\n" %  (panel_id_str, self.ranges["slow_scan_min"])
        serialization += "panel%s/max_ss         = %d\n" %  (panel_id_str, self.ranges["slow_scan_max"])
        serialization += "panel%s/corner_y       = %d\n" % (panel_id_str, self.corners["y"])
        serialization += "panel%s/fs             = %s\n" % (panel_id_str, self.fast_scan_xyz)
        serialization += "panel%s/ss             = %s\n" % (panel_id_str, self.slow_scan_xyz)
        serialization += "panel%s/clen           = %8.7e\n" % (panel_id_str, self.distance_from_interaction_plane.m_as(meter))
        serialization += "panel%s/res            = %8.7e\n" % (panel_id_str, 1./self.pixel_size.m_as(meter))
        serialization += "panel%s/coffset        = %8.7e\n" % (panel_id_str, self.distance_offset.m_as(meter))
        if self.energy_response is not None:
            serialization += "panel%s/adu_per_eV     = %8.7e\n" % (panel_id_str, self.energy_response.m_as(1/electronvolt))
        if self.photon_response is not None:
            serialization += "panel%s/adu_per_photon = %8.7e\n" % (panel_id_str, self.photon_response)
        if self.saturation_adu is not None:
            serialization += "panel%s/max_adu        = %8.7e\n" % (panel_id_str, self.saturation_adu)
        if self.mask is not None:
            serialization += "panel%s/badpixmap     = %s\n" % (panel_id_str, str(self.mask.magnitude))
            serialization += "panel%s/badpixmap     = %s\n" % (panel_id_str, str(self.mask.magnitude))
        if self.good_bit_mask is not None:
            serialization += "panel%s/mask_good     = %d\n" % (panel_id_str, self.good_bit_mask.magnitude)
        if self.bad_bit_mask is not None:
            serialization += "panel%s/mask_bad      = %d\n" % (panel_id_str, self.bad_bit_mask.magnitude)
        if self.saturation_map is not None:
            serialization += "panel%s/saturation_map = %s\n" % (panel_id_str, str(self.saturation_map.magnitude) )

        if 'CrystFELPhotonDiffractorParameters' not in caller.__str__():
            serialization += "panel%s/px             = %d\n" % (panel_id_str, self.number_of_pixels_fast)
            serialization += "panel%s/py             = %d\n" % (panel_id_str, self.number_of_pixels_slow)
            serialization += "panel%s/pix_width      = %8.7e\n" % (panel_id_str, self.pixel_size.m_as(meter))
            serialization += "panel%s/d              = %8.7e\n" % (panel_id_str, self.distance_from_interaction_plane.m_as(meter))
        serialization += "panel%s/corner_x       = %d\n" % (panel_id_str, self.corners["x"])
        serialization += "\n"

        # Finally write the serialized panel.
        stream.write(serialization)


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

    def serialize(self, stream=None, caller=None):
        """ Serialize the geometry.

        :param stream: The stream to write the serialized geometry to (default sys.stdout).
        :type  stream: File like object.

        """

        # Handle default case.
        if stream is None:
            stream = sys.stdout

        # If this is a string, open a corresponding file.
        if isinstance( stream,  str):
            with open(stream, 'w') as fstream:
                self._serialize(fstream, caller=caller)
                return

        if not hasattr(stream, "write"):
            raise IOError("The stream % is not writable." % (stream) )

        # Loop over all panels and serialize each one.
        self._serialize(stream, caller=caller)

    def _serialize(self, stream=sys.stdout, caller=None):
        """ Workhorse function for serialization. """

        for i,panel in enumerate(self.panels):
            panel._serialize( stream, panel_id=i, caller=caller)

def _detectorPanelFromString( input_string, common_block=None):
    """ Construct a DetectorPanel instance from a serialized panel.
    :param input_string: The string from which to construct the panel.
    :param common_block: String representing a block of common parameters for a group of panels.

    """
    # First treat common block
    common_dict = {}
    if common_block is not None:
        common_dict = _panelStringToDict(common_block)


    panel_dict = _panelStringToDict( input_string )

    # Loop over common dict and fill into panel dict if not present there.
    for key,val in common_dict.items():
        if panel_dict[key] is None:
            panel_dict[key] = val

    # Now put the data into the DetectorPanel instance.
    panel = DetectorPanel( ranges={"fast_scan_min" : float(panel_dict["min_fs"]),
                                   "fast_scan_max" : float(panel_dict["max_fs"]),
                                   "slow_scan_min" : float(panel_dict["min_ss"]),
                                   "slow_scan_max" : float(panel_dict["max_ss"]),
                                   },
                           corners={"x" : float(panel_dict["corner_x"]),
                                    "y" : float(panel_dict["corner_y"]),
                                   },
                           fast_scan_xyz=panel_dict["fs"],
                           slow_scan_xyz=panel_dict["ss"],
                           distance_from_interaction_plane=float(panel_dict["clen"])*meter,
                           pixel_size=1.0/float(panel_dict["res"])*meter,
                           )

    if panel_dict["adu_per_photon"] is not None:
        panel.photon_response = float(panel_dict["adu_per_photon"])
    if panel_dict["adu_per_eV"] is not None:
        panel.energy_response = float(panel_dict["adu_per_eV"])/electronvolt
    if panel_dict["coffset"] is not None:
       panel.distance_offset = float(panel_dict["coffset"])*meter
    else:
       panel.distance_offset=None
    if panel_dict["max_adu"] is not None:
        panel.saturation_adu = float(panel_dict["max_adu"])
    else:
        panel.saturation_adu = None
    if panel_dict["mask"] is not None:
        panel.mask = numpy.array( eval(panel_dict["mask"]) )
    else:
        panel.mask = None
    if panel_dict["mask_good"] is not None:
        panel.good_bit_mask = panel_dict["mask_good"]
    else:
        panel.good_bit_mask = None
    if panel_dict["mask_bad"] is not None:
        panel.bad_bit_mask = panel_dict["mask_bad"]
    else:
        panel.bad_bit_mask = None
    if panel_dict["saturation_map"] is not None:
        panel.saturation_map = panel_dict["saturation_map"]
    else:
        panel.saturation_map = None

    return panel


def _panelStringToDict( input_string ):
    """ Convert a panel block string to a dictionary. """
    # Get rid of panel prefix
    lines=input_string.split("\n")

    # Setup temporary dictionary.
    tmp_dict = {
            "min_fs"         : None,
            "max_fs"         : None,
            "min_ss"         : None,
            "max_ss"         : None,
            "corner_x"       : None,
            "corner_y"       : None,
            "fs"             : None,
            "ss"             : None,
            "clen"           : None,
            "res"            : None,
            "coffset"        : None,
            "adu_per_eV"     : None,
            "adu_per_photon" : None,
            "max_adu"        : None,
            "mask"           : None,
            "mask_good"      : None,
            "mask_bad"       : None,
            "saturation_map" : None,
            }

    # Loop over lines and extract data.
    for line in lines:
        # Bail out if not containing an assignment.
        if not "=" in line:
            continue
        # Get rid of white spaces.
        line = line.replace(" ","")
        line = line.replace("\t","")

        # Check for commented lines.
        if  line[0] == ";":
            continue

        key_val = line.split("=")
        key = key_val[0]
        val = key_val[1]

        # Check for comments after assignment.
        if ";" in val:
            val=val.split(";")[0]

        # Get rid of panel prefix.
        key = key.split("/")[-1]

        # Store on dict.
        tmp_dict[key] = val

    return tmp_dict


def _detectorGeometryFromString( input_string):
    """ Construct a DetectorGeometry instance from a serialized representation.
    :param input_string: The string from which to construct the panel.

    """
    # Separate out panel blocks and common block.
    # Get rid of empty lines.
    while "\n\n" in input_string:
        input_string = input_string.replace("\n\n", "\n")
    # Get rid of white space.
    input_string = input_string.replace(" ", "")

    # Split into lines.
    lines = input_string.split("\n")

    common_block = ""
    panel_blocks = ""
    for line in lines:
        if line == "":
            continue
        if line[0] == ";":
            continue
        if "/" in line:
            panel_blocks += line+"\n"
        else:
            common_block += "COMMON_BLOCK/"+line+"\n"

    # If no separate panels are defined, return.
    if panel_blocks == "":
        return DetectorGeometry(panels=_detectorPanelFromString(common_block))

    # Now separate the panel block into lines again and loop.
    lines = panel_blocks.split("\n")

    # Sort to make sure lines belonging to same block are adjacent.
    lines.sort()

    # Get panel identifiers.
    panel_identifiers = []
    for line in lines:
        if line == "":
            continue
        panel_identifiers.append(line.split("/")[0])

    # Turn into set of unique identifiers.
    panel_identifiers=list(set(panel_identifiers))
    panel_identifiers.sort()

    # Gather all panel blocks into a list of strings, separated by newline to make fit for _detectorPanelFromString().
    panel_blocks = ["",]*len(panel_identifiers)
    for line in lines:
        if line == "":
            continue
        # Get id.
        panel_identifier = line.split("/")[0]
        # Get index in list.
        block_index = panel_identifiers.index(panel_identifier)
        # Insert in correct position.
        panel_blocks[block_index] += line+"\n"

    # Deserialize the blocks.
    panels = [_detectorPanelFromString(block, common_block) for block in panel_blocks]

    # Return novel geometry instance.
    return DetectorGeometry(panels=panels)
