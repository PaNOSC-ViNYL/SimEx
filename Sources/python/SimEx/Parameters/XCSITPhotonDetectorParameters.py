""" :module XCSITPhotonDetectorParameters: Hosts the XCSITPhotonDetectorParameters class. """
##########################################################################
#                                                                        #
# Copyright (C) 2015-2018 Carsten Fortmann-Grote                         #
# Copyright (C) 2017 Jan-Philipp Burchert                                #
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

import sys

try:
    import libpy_detector_interface as lpdi

except ImportError:
    print("\nWARNING: Importing libpy_detector_interface failed. This is most probably due to XCSIT and/or Geant4 not being installed or not being found. Expect errors.\n")

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance

class XCSITPhotonDetectorParameters(AbstractCalculatorParameters):
    """
    :class XCSITPhotonDetectorParameters: Encapsulates all parameters for the XCSITPhotonDetector class. """

    def __init__(self,
                 detector_type=None,
                 plasma_search_flag=None,
                 plasma_simulation_flag=None,
                 point_simulation_method=None,
                 patterns=None,
                ):
        """
        :param detector_type: The detector type to simulate ("pnCCD" | "LPD" | "AGIPD | "AGIPDSPB").
        :type detector_type: str

        :param plasma_search_flag: Flag for the plasma search method ("BLANK").
        :type plasma_search_flag: str

        :param plasma_simulation_flag: Flag for the plasma simulation method ("BLANKPLASMA").
        :type plasma_simulation_flag: str

        :param point_simulation_method: Method for the charge point simulation ("FULL" | "FANO" | "LUT" | "BINNING").
        :type point_simulation_method: str

        :param patterns: Which patterns to feed into the detector simulation. Default: Use all patterns.
        :type patterns: (str || int) or iterable over these types.
        :example patterns: patterns=0 # use the first pattern.
        :example patterns: patterns=range(10) # use the first 10 patterns
        :example patterns: patterns=['0000001','0001001'] # user patterns with Ids  '0000001' and '0001001'.
        """

        # Prohibit calling the detector with nothing
        if all([detector_type is None,
            plasma_search_flag is None,
            plasma_simulation_flag is None,
            point_simulation_method is None]):
                raise AttributeError("Please specify at least the detector type")

        # Set defaults
        if plasma_search_flag is None:
            plasma_search_flag="BLANK"
        if plasma_simulation_flag is None:
            plasma_simulation_flag="BLANKPLASMA"
        if point_simulation_method is None:
            point_simulation_method="FULL"
        if patterns is None:
            patterns = [0]

        # Use the setters: They check the type of the input and set the private
        # attributes or raise an exception if the the type does not match the
        # required type
        self.detector_type = detector_type
        self.plasma_search_flag = plasma_search_flag
        self.plasma_simulation_flag = plasma_simulation_flag
        self.patterns = patterns
        self.point_simulation_method = point_simulation_method


    def _setDefaults(self):
        self._AbstractCalculatorParameters__cups_per_task_default = 1


    # Getter and Setter
    # getter raise an AttributeError if the attribute accessed by the called
    # getter is still of type None
    # setter check the input type with SimEx.Utilities.EntityChecks
    # checkAndSetInstance function -> raise an error if input type is not
    # matching
    @property
    def detector_type(self):
        """
        :return string containing the detector name
        """
        if self.__detector_type is None:
            raise TypeError("Attribute detector_type has not been set yet.")
        else:
            return self.__detector_type
    @detector_type.setter
    def detector_type(self,value):
        """
        :param value, a string with the detector name
        """
        # Check the type
        self.__detector_type = checkAndSetInstance(str,value,None)

        # Check the value
        con = lpdi.Constants()
        not_valid_option = True
        try:
            for i in list(range(con.size("DetectorType"))):
                if value == con.varValue("DetectorType",i):
                    not_valid_option = not_valid_option and False
        except:
            err = sys.exc_info()
            print(("Error type: " + str(err[0])))
            print(("Error value: " + str(err[1])))
            print(("Error traceback: " + str(err[2])))
            not_valid_option = True
        if not_valid_option:
            raise ValueError("Unknown detector type: " + str(value))

    @property
    def patterns(self):
        """
        :return: The patterns to use in the detector simulation.
        """
        return self.__patterns
    @patterns.setter
    def patterns(self, val):
        if hasattr(val, '__iter__'):
            self.__patterns = val
        else:
            self.__patterns = [val]
        ### TODO: more sanity checks (all items of same type, only int or str allowed).

    @property
    def plasma_search_flag(self):
        """
        :return string, the plasma search method
        """
        if self.__plasma_search_flag is None:
            raise TypeError("Attribute plasma_search_flag has not been set yet.")
        else:
            return self.__plasma_search_flag
    @plasma_search_flag.setter
    def plasma_search_flag(self,value):
        """
        :param value, a string, the plasma search method
        """
        # Check the type
        self.__plasma_search_flag = checkAndSetInstance(str,value,None)

        # Check the value
        con = lpdi.Constants()
        not_valid_option = True
        try:
            for i in list(range(con.size("PlasmaSearch"))):
                if value == con.varValue("PlasmaSearch",i):
                    not_valid_option = not_valid_option and False
        except:
            err = sys.exc_info()
            print(("Error type: " + str(err[0])))
            print(("Error value: " + str(err[1])))
            print(("Error traceback: " + str(err[2])))
            not_valid_option = True
        if not_valid_option:
           raise ValueError("Unknown plasma_search_flag: " + str(value))

    @property
    def plasma_simulation_flag(self):
        """
        :return string, the plasma simulation method
        """
        if self.__plasma_simulation_flag is None:
            raise TypeError("Attribute plasma_simulation_flag has not been set yet.")
        else:
            return self.__plasma_simulation_flag
    @plasma_simulation_flag.setter
    def plasma_simulation_flag(self,value):
        """
        :param value, a string, the plasma simulation method
        """
        # Check the type
        self.__plasma_simulation_flag = checkAndSetInstance(str,value,None)

        # Check the value
        con = lpdi.Constants()
        not_valid_option = True
        try:
            for i in list(range(con.size("PlasmaSim"))):
                if value == con.varValue("PlasmaSim",i):
                    not_valid_option = not_valid_option and False
        except:
            err = sys.exc_info()
            print(("Error type: " + str(err[0])))
            print(("Error value: " + str(err[1])))
            print(("Error traceback: " + str(err[2])))
            not_valid_option = True
        if not_valid_option:
            raise ValueError("Unknown plasma_simulation_flag: " + str(value))




    @property
    def point_simulation_method(self):
        """
        :return string, the charge simulation method
        """
        if self.__point_simulation_method is None:
            raise TypeError("Attribute point_simulation_method has not been set yet.")
        else:
            return self.__point_simulation_method
    @point_simulation_method.setter
    def point_simulation_method(self,value):
        """
        :param value, a string, the charge simulation method
        """
        # Check the type
        self.__point_simulation_method = checkAndSetInstance(str,value,None)

        # Check the value
        con = lpdi.Constants()
        not_valid_option = True
        try:
            for i in list(range(con.size("ChargeProp"))):
                if value == con.varValue("ChargeProp",i):
                    not_valid_option = not_valid_option and False
        except:
            err = sys.exc_info()
            print(("Error type: " + str(err[0])))
            print(("Error value: " + str(err[1])))
            print(("Error traceback: " + str(err[2])))
            not_valid_option = True
        if not_valid_option:
            raise ValueError("Unknown point_simulation_method: " + str(value))

