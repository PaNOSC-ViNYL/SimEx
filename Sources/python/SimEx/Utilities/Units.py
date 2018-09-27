""":module Units: Defines physical units and constants."""
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


from SimEx import PhysicalQuantity

from scipy import constants
from scipy.constants import e,c,hbar, m_e, epsilon_0
from scipy.constants import k as kB

# Base units.
meter           = PhysicalQuantity(1.0, 'meter')
second          = PhysicalQuantity(1.0, 'second')
kilogram        = PhysicalQuantity(1.0, 'kilogram')
ampere          = PhysicalQuantity(1.0, 'ampere')
volt            = PhysicalQuantity(1.0, 'volt')
joule           = PhysicalQuantity(1.0, 'joule')
newton          = PhysicalQuantity(1.0, 'newton')
kelvin          = PhysicalQuantity(1.0, 'kelvin')
radian          = PhysicalQuantity(1.0, 'radian')
electronvolt    = PhysicalQuantity(1.0, 'eV')
coulomb         = PhysicalQuantity(1.0, 'C')
farad           = PhysicalQuantity(1.0, 'farad')
rydberg         = constants.value('Rydberg constant times hc in eV') * electronvolt
bohr            = constants.value('Bohr radius') * meter
angstromstar    = constants.value('Angstrom star') * meter
angstrom        = 1.e-10 * meter
radian          = PhysicalQuantity(1.0, 'radian')
one             = PhysicalQuantity(1.0, 'dimensionless')

e = e*coulomb
c = c*meter/second
hbar = hbar * joule * second
m_e = m_e * kilogram
epsilon0 = epsilon_0*farad/meter
kB = kB*joule/kelvin

def compatible(quant1, quant2):
    return quant1.dimensionality == quant2.dimensionality

