""":module EntityChecks: Module for entity checks.  """
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
# Include needed directories in sys.path.                                #
#                                                                        #
##########################################################################

from SimEx import PhysicalQuantity

def checkAndSetInstance(cls, var=None, default=None):
    """
    Utility to check if the passed object is an instance of the given class (or derived class).

    :param cls : The class against which to check.
    :param var : The object to check.
    :param default : The default to use if no var is given.

    :return : The checked object or default.
    :raises TypeError: if var is not an instance of cls or a derived class.
    """

    if var is None:
        if default is None:
            return None
        elif not isinstance(default, cls):
            raise TypeError("The default is not of correct type.")
        else: return default

    elif not isinstance(var, cls):
        raise TypeError("The parameter 'var' is not of correct type: Expected %s, obtained %s." % (cls, type(var)))

    return var

def checkAndSetInteger(var=None, default=None):
    """
    Utility to check if the passed value is a positive integer.

    @param var : The object to check.
    @param default : The default to use if no var is given.
    @return : The checked object or default.
    @throw : TypeError if check fails.
    """

    if var is None:
        if not (isinstance( default, int) ):
            raise TypeError("The default must be an integer.")
        return default

    if not isinstance(var, int):
            raise TypeError("The parameter must be of type integer.")
    return var

def checkAndSetPositiveInteger(var=None, default=None):
    """
    Utility to check if the passed value is a positive integer.

    @param var : The object to check.
    @param default : The default to use if no var is given.
    @return : The checked object or default.
    @throw : TypeError if check fails.
    """

    if var is None:
        if not (isinstance( default, int) and default > 0):
            raise TypeError("The default must be a positive integer.")
        return default

    if not isinstance(var, int):
            raise TypeError("The parameter must be of type integer.")
    if var <= 0:
            raise TypeError("The parameter must be a positive integer.")
    return var

def checkAndSetNonNegativeInteger(var=None, default=None):
    """
    Utility to check if the passed value is a non-negative integer.

    @param var : The object to check.
    @param default : The default to use if no var is given.
    @return : The checked object or default.
    @throw : TypeError if check fails.
    """

    if var is None:
        if not (isinstance( default, int) and default >= 0):
            raise TypeError("The default must be a non-negative integer.")
        return default

    if not isinstance(var, int):
            raise TypeError("The parameter must be of type integer.")
    if var < 0:
            raise TypeError("The parameter must be a non-negative integer.")
    return var

def checkAndSetNumber(var=None, default=None):
    """ Check if input is a numerical type. """
    if var is not None:
        if not isinstance( var, (int, float) ):
            raise TypeError("The given value must be a numerical type, got %s" % (type(var)))
        return var

    if not isinstance( default, (int, float)):
            raise TypeError("The default value must be a numerical type, got %s" % (type(default)))
    return default

def checkAndSetIterable(var=None, default=None):
    """ Check if input is iterable (list, tuple, or array type). """

    if not hasattr( var, "__iter__" ):
        raise AttributeError( "The parameter must be iterable (e.g. a tuple, list, or numpy.array).")

    return var

def checkAndSetPhysicalQuantity(var, default, unit):
    """ Check if input is a PhysicalQuantity and has the correct unit. """

    if var is not None:
        if not isinstance(var, PhysicalQuantity):
            raise TypeError("%s is not a PhysicalQuantity." % (repr(var)) )
        if not var.units == unit.units:
            raise TypeError("Incorrect unit (%s), expected %s." % (var.units, unit.units) )
    else:
        if default is not None:
            if isinstance(default, PhysicalQuantity):
                if default.units == unit.units:
                    return default
                else:
                    return default.to(unit.units)
            else:
                return default*unit
            return default

    return var

