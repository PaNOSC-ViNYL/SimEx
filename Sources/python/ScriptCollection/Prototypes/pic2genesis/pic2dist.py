""" :module pic2dist: Script to convert openpmd output from picongpu to a genesis beam.dat file. """
##########################################################################
#                                                                        #
# Copyright (C) 2017 Carsten Fortmann-Grote, Ashutosh Sharma             #
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

from scipy.constants import m_e, c, e
import h5py
import numpy
import sys, os

def pic2dist( pic_file_name, target='genesis'):
    """ Utility to extract particle data from openPMD and write into genesis distribution file.

    :param pic_file_name: Filename of openpmd input data file.
    :type pic_file_name: str

    :param target: The targeted file format (genesis || simplex).
    :type target: str

    """

    #  Check path.
    if not os.path.isfile(pic_file_name):
        raise RuntimeError("%s is not a file." % (pic_file_name))

    # Check if input is native or openPMD.
    with h5py.File( pic_file_name, 'r' ) as h5_handle:

        timestep = list(h5_handle['data'].keys())[-1]

        positions = '/data/%s/particles/e/position/' % (timestep)
        momenta = '/data/%s/particles/e/momentum/' % (timestep)

        x_data = h5_handle[positions]['x'].value
        x_data_unit = h5_handle[positions]['x'].attrs['unitSI']
        x = x_data*x_data_unit

        y_data = h5_handle[positions]['y'].value
        y_data_unit = h5_handle[positions]['y'].attrs['unitSI']
        y = y_data*y_data_unit

        z_data = h5_handle[positions]['z'].value
        z_data_unit = h5_handle[positions]['z'].attrs['unitSI']
        z = z_data*z_data_unit

        px_data = h5_handle[momenta]['x'].value
        px_data_unit = h5_handle[momenta]['x'].attrs['unitSI']
        px = px_data*px_data_unit

        py_data = h5_handle[momenta]['y'].value
        py_data_unit = h5_handle[momenta]['y'].attrs['unitSI']
        py = py_data*py_data_unit

        pz_data = h5_handle[momenta]['z'].value
        pz_data_unit = h5_handle[momenta]['z'].attrs['unitSI']
        pz = pz_data*pz_data_unit

        # Convert to xprime, yprime.
        xprime = numpy.arctan(px/py)
        zprime = numpy.arctan(pz/py)

        # Calculate particle charge.
        charge_group = h5_handle['/data/%s/particles/e/charge/' %(timestep)]
        macroparticle_charge = charge_group.attrs['unitSI']

        # Get number of particles and total charge.
        particle_patches = h5_handle['/data/%s/particles/e/particlePatches/numParticles' %(timestep)].value
        number_of_macroparticles = numpy.sum( particle_patches )

        number_of_electrons_per_macroparticle = macroparticle_charge / e
        total_charge = number_of_macroparticles * macroparticle_charge

        # Calculate momentum
        psquare = px**2 + py**2 + pz**2
        gamma = numpy.sqrt( 1. + psquare/((number_of_electrons_per_macroparticle * m_e*c)**2))
        P = numpy.sqrt(psquare/((number_of_electrons_per_macroparticle * m_e*c)**2))

        print("Number of electrons per macroparticle = ", number_of_electrons_per_macroparticle)
        print("Total charge = ", total_charge)
        print("Number of macroparticles = ", number_of_macroparticles)

        h5_handle.close()

    if target == 'genesis':
	    return numpy.vstack([ x, xprime, z, zprime, y/c, P]).transpose(),  total_charge
    elif target == 'simplex':
	    return numpy.vstack([ y/c, x, xprime, z, zprime,  gamma]).transpose(),  total_charge

if __name__ == "__main__":
    data, charge = pic2dist(sys.argv[1], sys.argv[2])
    # Setup header for distribution file.
    comments = "? "
    size = data.shape[0]
    header = "VERSION = 1.0\nSIZE = %d\nCHARGE = %7.6E\nCOLUMNS X XPRIME Y YPRIME T P" % (size, charge)

    if sys.argv[2] == 'genesis':
        numpy.savetxt( fname='beam.dist', X=data, header=header, comments=comments)
    if sys.argv[2] == 'simplex':
        numpy.savetxt( fname='beam.dist', X=data)

