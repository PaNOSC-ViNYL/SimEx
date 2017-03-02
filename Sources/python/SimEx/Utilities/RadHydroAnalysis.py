#!/usr/bin/env python2.7
##########################################################################
#                                                                        #
# Copyright (C) 2017 Carsten Fortmann-Grote, Richard Briggs              #
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

import os
import numpy
from matplotlib import pyplot
from xraydb import XrayDB
import h5py

from SimEx.Parameters.EstherPhotonMatterInteractorParameters import EstherPhotonMatterInteractorParameters

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
    edge_fyield = edge_data[1]
    edge_jump = edge_data[2]

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

def radHydroAnalysis(filename):
    """ Generates four plots to analyse shock compression data.

    :param filename: Filename of hdf5 file containing rad-hydro data in openPMD format.
    :type filename: str

    """
    # Get parameters for the corresponding esther run.
    esther_parameters = EstherPhotonMatterInteractorParameters(read_from_file=os.path.dirname(filename))

    # Get zone dimensions.
    number_of_sample_zones = esther_parameters._EstherPhotonMatterInteractorParameters__number_of_sample_zones
    try:
        number_of_window_zones = esther_parameters._EstherPhotonMatterInteractorParameters__number_of_window_zones
    except:
        number_of_window_zones = 0

    # Get data from h5 output.
    with h5py.File(filename, 'r') as h5:
        # Time snapshots.
        snapshots = [int(k) for k in h5["/data"].keys()]
        snapshots.sort()
        times = numpy.array([h5["/data/%s" % (s)].attrs["time"] for s in snapshots])*1e9 # ns

        # Get simulation data.
        positions  = numpy.array([h5["/data/%s/meshes/pos" % (s)].value for s in snapshots])*1e6 # mu
        pressures  = numpy.array([h5["/data/%s/meshes/pres" % (s)].value for s in snapshots])/1e9 # GPa
        velocities = -numpy.array([h5["/data/%s/meshes/vel" % (s)].value for s in snapshots])/1e3 # km/s
        temperatures = numpy.array([h5["/data/%s/meshes/temp" % (s)].value for s in snapshots]) # K

        h5.close()

    # Find limits of sample zone.
    total_number_of_zones = positions.shape[1]
    number_of_ablator_zones = total_number_of_zones-number_of_sample_zones-number_of_window_zones

    sample_indices = range(number_of_window_zones, number_of_window_zones+number_of_sample_zones)
    sample_start_index = sample_indices[0]
    sample_end_index = sample_indices[-1]

    ### PLOTS ###
    ###################
    # Top left panel: Pressure vs. time averaged over sample.
    ###################
    pyplot.subplot(2,2,1)
    x = times
    y = numpy.mean(pressures[:,sample_start_index:sample_end_index], axis=1)
    dy = numpy.std(pressures[:,sample_start_index:sample_end_index], axis=1)
    pyplot.errorbar(x,y,yerr=dy)

    pyplot.xlabel("time (ns)")
    pyplot.ylabel("pressure (GPa)")

    pyplot.gca().get_yaxis().get_major_formatter().set_powerlimits((0, 0))
    pyplot.gca().get_xaxis().get_major_formatter().set_powerlimits((0, 0))


    ###################
    # Top right panel: Velocity vs. time in last sample zone.
    ###################
    pyplot.subplot(2,2,2)
    x = times
    y = velocities[:,sample_end_index-1]
    pyplot.plot(x,y)

    pyplot.xlabel("time (ns)")
    pyplot.ylabel("velocity (km/s)")

    pyplot.gca().get_yaxis().get_major_formatter().set_powerlimits((0, 0))
    pyplot.gca().get_xaxis().get_major_formatter().set_powerlimits((0, 0))

    ###################
    # Bottom left panel: Pressure contour as function of x and t.
    ###################
    pyplot.subplot(2,2,3)
    X = numpy.array([times for i in range(total_number_of_zones)])
    Y = positions.transpose()
    pyplot.contourf(X,Y,pressures.transpose(),32, cmap="YlGnBu_r")

    y = positions[:,sample_start_index]
    pyplot.plot(x,y,'k',lw=2)
    y = positions[:,sample_end_index-1]
    pyplot.plot(x,y,'k',lw=2)

    pyplot.xlabel("time (ns)")
    pyplot.ylabel("position (um)")

    pyplot.ylim([positions.min(), 0])

    pyplot.gca().get_yaxis().get_major_formatter().set_powerlimits((0, 0))
    pyplot.gca().get_xaxis().get_major_formatter().set_powerlimits((0, 0))

    ###################
    # Bottom right panel: Temperature vs. pressure.
    ###################
    sample_middle_index = int(0.5*(sample_start_index + sample_end_index))
    pyplot.subplot(2,2,4)
    x = pressures[:,sample_middle_index]
    y = temperatures[:,sample_middle_index]

    pyplot.plot(x,y)
    pyplot.xlabel("pressure (GPa)")
    pyplot.ylabel("temperature (K)")

    pyplot.gca().get_yaxis().get_major_formatter().set_powerlimits((0, 0))
    pyplot.gca().get_xaxis().get_major_formatter().set_powerlimits((0, 0))

    pyplot.show()
