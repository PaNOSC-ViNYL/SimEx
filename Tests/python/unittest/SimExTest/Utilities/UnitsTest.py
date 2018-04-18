""" module: Hosting Test of the Units module."""
##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 Carsten Fortmann-Grote                         #
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

import unittest

from SimEx.Utilities.Units import meter
from SimEx.Utilities.Units import second
from SimEx.Utilities.Units import kilogram
from SimEx.Utilities.Units import ampere
from SimEx.Utilities.Units import volt
from SimEx.Utilities.Units import joule
from SimEx.Utilities.Units import newton
from SimEx.Utilities.Units import kelvin



class UnitsTest(unittest.TestCase):
    """ Test class for the EntityChecks class. """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        pass

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        pass

    def setUp(self):
        """ Setting up a test. """
        pass

    def tearDown(self):
        """ Tearing down a test. """
        pass

    def testMeter(self):
        """ Test the length unit. """

        # Check setting up a length.
        l = 2.6*meter
        self.assertEqual(l.units, "meter")

        # Check area
        a = l**2
        self.assertEqual(a.units, "meter**2")
        self.assertEqual(a.units, "square meter")

        # Check equality of units
        l2 = 2.3e-5*meter
        self.assertEqual(l.units, l2.units)

    def testSecond(self):
        """ Test the time unit. """

        # Check setting up a time.
        l = 2.6*second
        self.assertEqual(l.units, "second")

        # Check power.
        a = l**2
        self.assertEqual(a.units, "second**2")
        self.assertEqual(a.units, "square second")

        # Check equality of units
        l2 = 2.3e-5*second
        self.assertEqual(l.units, l2.units)

    def testKilogram(self):
        """ Test the mass unit."""

        # Check setting up a current.
        l = 2.6*kilogram
        self.assertEqual(l.units, "kilogram")

        # Check power
        a = l**2
        self.assertEqual(a.units, "kilogram**2")
        self.assertEqual(a.units, "square kilogram")

        # Check equality of units
        l2 = 2.3e-5*kilogram
        self.assertEqual(l.units, l2.units)

    def testAmpere(self):
        """ Test the current unit."""

        # Check setting up a current.
        l = 2.6*ampere
        self.assertEqual(l.units, "ampere")

        # Check power
        a = l**2
        self.assertEqual(a.units, "ampere**2")
        self.assertEqual(a.units, "square ampere")

        # Check equality of units
        l2 = 2.3e-5*ampere
        self.assertEqual(l.units, l2.units)

    def testVolt(self):
        """ Test the voltage unit."""

        # Check setting up a voltage.
        l = 2.6*volt
        self.assertEqual(l.units, "volt")

        # Check power
        a = l**2
        self.assertEqual(a.units, "volt**2")
        self.assertEqual(a.units, "square volt")

        # Check equality of units
        l2 = 2.3e-5*volt
        self.assertEqual(l.units, l2.units)

    def testJoule(self):
        """ Test the energy unit."""

        # Check setting up a energy.
        l = 2.6*joule
        self.assertEqual(l.units, "joule")

        # Check power
        a = l**2
        self.assertEqual(a.units, "joule**2")
        self.assertEqual(a.units, "square joule")

        # Check equality of units
        l2 = 2.3e-5*joule
        self.assertEqual(l.units, l2.units)

    def testNewton(self):
        """ Test the force unit."""

        # Check setting up a force.
        l = 2.6*newton
        self.assertEqual(l.units, "newton")

        # Check power
        a = l**2
        self.assertEqual(a.units, "newton**2")
        self.assertEqual(a.units, "square newton")

        # Check equality of units
        l2 = 2.3e-5*newton
        self.assertEqual(l.units, l2.units)

    def testKelvin(self):
        """ Test the temperature unit."""

        # Check setting up a temperature.
        l = 2.6*kelvin
        self.assertEqual(l.units, "kelvin")

        # Check power
        a = l**2
        self.assertEqual(a.units, "kelvin**2")
        self.assertEqual(a.units, "square kelvin")

        # Check equality of units
        l2 = 2.3e-5*kelvin
        self.assertEqual(l.units, l2.units)


if __name__ == '__main__':
    unittest.main()
