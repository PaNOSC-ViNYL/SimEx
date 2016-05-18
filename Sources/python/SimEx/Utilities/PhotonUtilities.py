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
#                                                                        #
##########################################################################

""" Module for photon utilities
    @author CFG
    @institution XFEL
    @creation 20160518
"""
from argparse import ArgumentParser
from scipy import constants
import h5py
import numpy

# Get some constants.
c = constants.speed_of_light
eps0 = constants.epsilon_0
e = constants.e

def convertWavefrontToPhotons(input_file):
    """ Utility to convert openPMD conform hdf5 with electric fields to photons. """

    # Check input file.
    if not h5py.is_hdf5(input_file):
        raise IOError("Not a valid hdf5 file: %s. " % (input_file))

    # Open input.
    h5 = h5py.File( input_file, 'r')

    data = h5['data']

    time_keys = data.keys()

    photon_energy = h5['history/parent/params/photonEnergy'].value # eV
    photon_energy = photon_energy * e # Convert to J

    sum_x = 0.0
    sum_y = 0.0
    for key in time_keys:

        # Get time of this slice.
        t  = data[key].attrs['time']

        # Get duration of this slice.
        dt = data[key].attrs['dt']

        # Get fields.
        E = data[key+'/meshes/E']

        # Get grid spacing.
        dx,dy = E.attrs['gridSpacing']

        # Get area element.
        dA = dx*dy

        # Get fields in x and y.
        Ex = data[key+'/meshes/E/x'].value # V/m
        Ey = data[key+'/meshes/E/y'].value # V/m


        # Calculate number of photons via intensity and photon energy. Since fields are stored as sqrt(W/mm^2), have to convert to W/m^2 (factor 1e6 below).
        number_of_photons_x = numpy.round(abs(Ex)**2 * dA * dt *1.0e6 / photon_energy)
        number_of_photons_y = numpy.round(abs(Ey)**2 * dA * dt *1.0e6 / photon_energy)

        sum_x += number_of_photons_x.sum(axis=-1).sum(axis=-1)
        sum_y += number_of_photons_y.sum(axis=-1).sum(axis=-1)

        phases_x = numpy.angle(Ex)
        phases_y = numpy.angle(Ey)

        #import pylab
        #pylab.imshow(phases_x, cmap="RdBu")
        #pylab.show()

        print "t=%e: found %d horizontally polarized photons in central pixel." % (t, number_of_photons_x[39,39])
        print "t=%e: found %d vertically polarized photons in central pixel." % (t, number_of_photons_y[39,39])

    print "Found total %e, %e photons (hor, ver)" % (sum_x, sum_y)

if __name__ == "__main__":

    # Parse arguments.
    parser = ArgumentParser(description="Convert Maxwell fields to photons.")
    parser.add_argument("input_file", metavar="input_file",
                      help="name of the file to extract photon numbers from.")
    args = parser.parse_args()

    # Call the converter routine.
    convertWavefrontToPhotons(args.input_file)








