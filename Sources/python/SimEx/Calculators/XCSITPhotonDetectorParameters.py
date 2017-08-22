#
# File:		XCSITPhotonDetectorParameters.py
# Author:	jburchert
# Date:		17 August 2017
#

import so

from SimEx.Parameters.AbstractCalculatorParameters import
AbstractCalculatorParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance

class XCSITPhotonDetectorParameters(AbstractCalculatorParameters):
	"""
	Datastructure to store the necessary parameters for a XCSITPhotonDetector
	simulation
	"""

	# set the only allowed attributes of instances of this class
	__slots__ = "__param_dict"


	# Create the instance attributes
	def __init__(self,
				detectortype=None
				plasmasearch=None
				plasmaSim=None
				pointsim=None):
		"""
		fields required to run the simulation

		:param 	detectortype = "pnCCD" | "LPD" | "AGIPD | "AGIPDSPB"
		:type 	str

		:param  plasmasearch = "BLANK"
		:type	str

		:param	plasmasim = "BLANKPLASMA"
		:type	str

		:param 	pointsim = "FULL" | "FANO" | "LUT" | "BINNING"
		:type 	str
		"""

		self.__param_dict["detectortype"] = None
		self.__param_dict["plasmasearch"] = None
		self.__param_dict["plasmasim"]	= None
		self.__param_dict["pointsim"]	= None



	# Getter and Setter
	@property
	def detectortype(self):
		"""
		:return string containing the detector name
		"""
		return self.__param_dict["detectortype"]
	@detectortype.setter
	def detectortype(self,value)
		"""
		:param value, a string with the detector name
		"""
		self.__param_dict["detectortype"] = checkAndSetInstance(str,value,None)


	@property
	def plasmasearch(self):
		"""
		:return string, the plasma search method
		"""
		return self.__param_dict["plasmasearch"]
	@plasmasearch.setter
	def plasmasearch(self,value)
		"""
		:param value, a string, the plasma search method
		"""
		self.__param_dict["plasmasearch"] = checkAndSetInstance(str,value,None)

	@property
	def plasmasim(self):
		"""
		:return string, the plasma simulation method
		"""
		return self.__param_dict["plasmasim"]
	@plasmasim.setter
	def plasmasim(self,value)
		"""
		:param value, a string, the plasma simulation method
		"""
		self.__param_dict["plasmasim"] = checkAndSetInstance(str,value,None)

	@property
	def pointsim(self):
		"""
		:return string, the charge simulation method
		"""
		return self.__param_dict["pointsim"]
	@pointsim.setter
	def pointsim(self,value)
		"""
		:param value, a string, the charge simulation method
		"""
		self.__param_dict["pointsim"] = checkAndSetInstance(str,value,None)


