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
# Include needed directories in sys.path.                                #
#                                                                        #
##########################################################################

""" Module for entity checks.
    @author CFG
    @institution XFEL
    @creation 20151006
"""

import exceptions

def checkAndSetInstance(cls, var=None, default=None):
    """
    Utility to check if the passed object is an instance of the given class (or derived class).

    @param cls : The class against which to check.
    @param var : The object to check.
    @param default : The default to use if no var is given.
    @return : The checked object or default.
    @throw : TypeError if var is not an instance of cls or a derived class.
    """

    if var is None:
        if default is None:
            return None
        elif not isinstance(default, cls):
            raise exceptions.TypeError("The default is not of correct type.")
        else: return default

    elif not isinstance(var, cls):
        raise exceptions.TypeError("The parameter 'var' is not of correct type.")

    return var
