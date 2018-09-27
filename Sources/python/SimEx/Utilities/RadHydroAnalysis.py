#!/usr/bin/env python
""":module RadHydroAnalysis: Collection of utilities to analyse output from (esther) rad-hydro simulations. """

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


import os
import numpy
from matplotlib import pyplot
import h5py

from SimEx.Parameters.EstherPhotonMatterInteractorParameters import EstherPhotonMatterInteractorParameters

def radHydroAnalysis(filename):
    """
    Generates four plots to analyse shock compression data.

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
        snapshots = [int(k) for k in list(h5["/data"].keys())]
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

    sample_indices = list(range(number_of_window_zones, number_of_window_zones+number_of_sample_zones))
    #sample_start_index = sample_indices[0]
    #sample_end_index = sample_indices[-1]
    sample_start_index = 1
    sample_end_index =  255

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

    #pyplot.gca().get_yaxis().get_major_formatter().set_powerlimits((0, 0))
    #pyplot.gca().get_xaxis().get_major_formatter().set_powerlimits((0, 0))


    ###################
    # Top right panel: Velocity vs. time in last sample zone.
    ###################
    pyplot.subplot(2,2,2)
    x = times
    y = velocities[:,sample_end_index-1]
    pyplot.plot(x,y)

    pyplot.xlabel("time (ns)")
    pyplot.ylabel("velocity (km/s)")

    #pyplot.gca().get_yaxis().get_major_formatter().set_powerlimits((0, 0))
    #pyplot.gca().get_xaxis().get_major_formatter().set_powerlimits((0, 0))

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

    #pyplot.gca().get_yaxis().get_major_formatter().set_powerlimits((0, 0))
    #pyplot.gca().get_xaxis().get_major_formatter().set_powerlimits((0, 0))

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

    #pyplot.gca().get_yaxis().get_major_formatter().set_powerlimits((0, 0))
    #pyplot.gca().get_xaxis().get_major_formatter().set_powerlimits((0, 0))

    pyplot.tight_layout()
    pyplot.show()
