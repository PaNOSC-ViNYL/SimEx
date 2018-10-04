#!/usr/bin/env python
""":module RadHydroInputPlots: Hosts utilities to plot target absorption profiles."""
##########################################################################
#                                                                        #
# Copyright (C) 2017-2018 Carsten Fortmann-Grote, Richard Briggs         #
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

""" Collection of utilities to analyse output from (esther) rad-hydro simulations. """

import numpy
from matplotlib import pyplot
from xraydb import XrayDB

def plotTransmission(symbol, edge="K", thickness=0.001, energies=None):
    """ Plots absorption in a given material as function of wavelength.

    :param symbol: The chemical symbol of the material.
    :type symbol: str

    :param edge: The requested absorption edge (K, L1, L2, M1, M2, ...)
    :type edge: str

    :param thickness: The material thickness in centimeters."
    :type thickness: float

    :param energies: For which energies to plot the transmission.
    :type energies: ndarray

    """
    # Instantiate the database.
    xdb = XrayDB()

    # Get info on requested edge.
    edge_data = xdb.xray_edge(symbol, edge)
    edge_position = edge_data[0]

    # Mass density (ambient).
    rho = xdb.density(symbol)

    # Fix energy range.
    min_energy = 0.7*edge_position
    max_energy = 1.3*edge_position

    # Setup arrays
    if energies is None:
        energies = numpy.linspace(min_energy, max_energy, 1024)
    mu = xdb.mu_chantler(symbol, energy=energies)


    # Convert to iterable if needed.
    if not hasattr(thickness, "__iter__"):
        thickness = [thickness]

    absorption = [numpy.exp(-mu*rho*th) for th in thickness]
    for i,abso in enumerate(absorption):
        pyplot.plot(energies, abso, lw=2, label=r"%3.1f $\mu$m" % (thickness[i] * 1e4))
    pyplot.xlabel('Energy (eV)')
    pyplot.ylabel('Transmission')
    pyplot.legend()
    pyplot.title("%s %s-edge" % (symbol, edge))

    pyplot.show()

def plotTargetAndTransmission(symbol, edge="K", thickness=0.001, energies=None, ablator_thickness=0.0025):
    """ Plots absorption in a given material as function of wavelength.

    :param symbol: The chemical symbol of the material.
    :type symbol: str

    :param edge: The requested absorption edge (K, L1, L2, M1, M2, ...)
    :type edge: str

    :param thickness: The material thickness in centimeters."
    :type thickness: float

    :param energies: For which energies to plot the transmission.
    :type energies: ndarray

    :param ablator_thickness: Thickness of ablator
    :type ablator_thickness: float

    """
    # Instantiate the database.
    xdb = XrayDB()

    # Get info on requested edge.
    edge_data = xdb.xray_edge(symbol, edge)
    edge_position = edge_data[0]

    # Mass density (ambient).
    rho = xdb.density(symbol)

    # Fix energy range.
    min_energy = 0.7*edge_position
    max_energy = 1.3*edge_position

    # Setup arrays
    if energies is None:
        energies = numpy.linspace(min_energy, max_energy, 1024)
    mu = xdb.mu_chantler(symbol, energy=energies)


    # Convert to iterable if needed.
    if not hasattr(thickness, "__iter__"):
        thickness = [thickness]

    pyplot.figure(num=None, figsize=(10, 8), dpi=100, facecolor='w', edgecolor='k')
    pyplot.subplot(221)

    pyplot.xlabel('Energy (eV)')
    pyplot.ylabel('Transmission')
    pyplot.legend()
    pyplot.title("%s %s-edge" % (symbol, edge))

    pyplot.subplot(223)
    absorption = [numpy.exp(-mu*rho*th) for th in thickness]
    for i,abso in enumerate(absorption):
        pyplot.plot(energies, abso, lw=2, label=r"%3.1f $\mu$m" % (thickness[i] * 1e4))
    pyplot.xlabel('Energy (eV)')
    pyplot.ylabel('Transmission')
    pyplot.legend()
    pyplot.title("%s %s-edge" % (symbol, edge))

    pyplot.tight_layout()
    pyplot.show()

if __name__ == "__main__":

    plotTransmission("Fe", thickness=0.001)
