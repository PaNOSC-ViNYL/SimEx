##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 jan-Philipp Burcher, Carsten Fortmann-Grote    #
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

import so

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance

class XCSITPhotonDetectorParameters(AbstractCalculatorParameters):
	"""
	Datastructure to store the necessary parameters for a XCSITPhotonDetector
	simulation
	"""

	# set the only allowed attributes of instances of this class
    ### COMMENT why use a dict?
	__slots__ = "__param_dict"


	# Create the instance attributes
	def __init__(self,
				detector_type=None
				plasma_search_flag=None
				plasmaSim=None
				point_simulation_method=None):
		"""
		fields required to run the simulation

        :param detector_type: The detector type to simulate ("pnCCD" | "LPD" | "AGIPD | "AGIPDSPB").
        :type detector_type: str

        :param plasma_search_flag: Flag for the plasma search method ("BLANK").
        :type plasma_search_flag: str

        :param plasma_simulation_flag: Flag for the plasma simulation method ("BLANKPLASMA").
        :type plasma_simulation_flag: str

        :param point_simulation_method: Method for the charge point simulation ("FULL" | "FANO" | "LUT" | "BINNING").
        :type point_simulation_method: str
		"""

		self.__param_dict["detector_type"] = None
		self.__param_dict["plasma_search_flag"] = None
		self.__param_dict["plasma_simulation_flag"]	= None
		self.__param_dict["point_simulation_method"]	= None

        ### COMMENT: Consider default handling in setters:
        ### COMMENT: self.detector_type = detector_type


	# Getter and Setter
	@property
	def detector_type(self):
		"""
		:return string containing the detector name
		"""
		return self.__param_dict["detector_type"]
	@detector_type.setter
	def detector_type(self,value)
		"""
		:param value, a string with the detector name
		"""
		self.__param_dict["detector_type"] = checkAndSetInstance(str,value,None)


	@property
	def plasma_search_flag(self):
		"""
		:return string, the plasma search method
		"""
		return self.__param_dict["plasma_search_flag"]
	@plasma_search_flag.setter
	def plasma_search_flag(self,value)
		"""
		:param value, a string, the plasma search method
		"""
		self.__param_dict["plasma_search_flag"] = checkAndSetInstance(str,value,None)

	@property
	def plasma_simulation_flag(self):
		"""
		:return string, the plasma simulation method
		"""
		return self.__param_dict["plasma_simulation_flag"]
	@plasma_simulation_flag.setter
	def plasma_simulation_flag(self,value)
		"""
		:param value, a string, the plasma simulation method
		"""
		self.__param_dict["plasma_simulation_flag"] = checkAndSetInstance(str,value,None)

	@property
	def point_simulation_method(self):
		"""
		:return string, the charge simulation method
		"""
		return self.__param_dict["point_simulation_method"]
	@point_simulation_method.setter
	def point_simulation_method(self,value)
		"""
		:param value, a string, the charge simulation method
		"""
		self.__param_dict["point_simulation_method"] = checkAndSetInstance(str,value,None)
