from SimEx import PhysicalQuantity, ureg

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

