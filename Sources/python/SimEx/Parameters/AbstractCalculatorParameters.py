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


class AbstractCalculatorParameters(object):
    """
    Abstract class for all calculator parameters.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, parameters_dict=None):
        """
        Constructor for the Abstract Calculator Parameters.

        @param control_parameters : The parameters to turn into class members.
        <br/><b>type</b> : dict

        """
        pass
