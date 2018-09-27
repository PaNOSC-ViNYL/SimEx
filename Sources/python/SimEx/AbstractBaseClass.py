""":module AbstractBaseClass: Hosting the origin of everythin. """
##########################################################################
#                                                                        #
# Copyright (C) 2015-2018 Carsten Fortmann-Grote                         #
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

from abc import ABCMeta, abstractmethod
import copy

class AbstractBaseClass(object, metaclass=ABCMeta):
    """
    :class AbstractBaseClass: The SimEx abstract base class from which all SimEx classes derive.
    """

    @abstractmethod
    def __init__(self, **kwargs):
        """
        :param **kwargs:  key=value pairs for calculator specific parameters.
        """

    def __call__(self, **kwargs):
        """
        Copy constructor of the class. Returns an identical or mutated copy of self.

        :param kwargs: List of key-value arguments supported by the class constructor.

        """
        clone = copy.deepcopy(self)

        if kwargs is not None:
            for key,value in kwargs.items():
                setattr(clone, key, value)

        return clone

    def __eq__(self, comp):
        """ Test equality of this and another ABC instance. """
        eq = True
        for key, val in self.__dict__.items():
            if not ( val == comp.__dict__[key] ):
                #print key, val, comp.__dict__[key]
                return not eq

        return eq



