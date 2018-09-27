""":module WPGBeamlines: Module holding functions that return predefined WPG beamlines. """
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


# Import the prop beamline.
from prop import exfel_spb_kb_beamline
from prop import exfel_spb_day1_beamline

def setupSPBDay1Beamline():
    """ Setup and return a WPG beamline corresponding to the SPB day 1 configuration. """

    return exfel_spb_day1_beamline

def setup_S2E_SPI_beamline():
    """ Utility function that returns the S2E SPI beamline (Yoon et al. Scientific Reports (2016). """
    return exfel_spb_kb_beamline

