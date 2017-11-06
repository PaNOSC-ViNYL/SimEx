from SimEx import PhysicalQuantity
from scipy.constants import e,c,hbar

Metre           = PhysicalQuantity(1.0, 'meter')
Second          = PhysicalQuantity(1.0, 'second')
Kilogram        = PhysicalQuantity(1.0, 'kilogram')
Ampere          = PhysicalQuantity(1.0, 'ampere')
Volt            = PhysicalQuantity(1.0, 'volt')
Joule           = PhysicalQuantity(1.0, 'joule')
Newton          = PhysicalQuantity(1.0, 'newton')
Kelvin          = PhysicalQuantity(1.0, 'kelvin')

Coulomb         = Ampere * Second
ElectronVolt    = e * Joule
