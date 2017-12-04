from SimEx import PhysicalQuantity, ureg
from scipy.constants import e,c,hbar

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
