""" :script shadow_to_opmd: Script to save a Shadow beams object to OpenPMD compliant hdf5.
    :usage: In Oasys, load this script in the Python script widget and connect the widget to the element at which to save the rays. Click "Execute". A shadow.out.h5 file should now exist in your $PWD. For OpenPMD format, please consult www.openpmd.org
    :Neccessary adjustments: Path to the simex utility collection OpenPMD must be specified. If SimEx ist not installed, get just the class OpenPMDTools.py from https://github.com/eucall-software/simex_platform/blob/develop/Sources/python/SimEx/Utilities/OpenPMDTools.py and copy it to your working directory.
    :note: Assumes that all lengths in the beam object are expressed in units of metres.
"""
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

from argparse import ArgumentParser
import os
import h5py
import numpy
from scipy import constants
import sys

### ADOPT ME
#sys.path.insert(0,<path_to_directory_containing_OpenPMD.py>)

# Get some constants.
c = constants.speed_of_light
eps0 = constants.epsilon_0
e = constants.e
hbar = constants.hbar

LENGTH_UNIT = 'm'

import OpenPMDTools as opmd

def convertToOPMD(beam):
    """ Format beam entries to particles and fields in openpmd file (hdf5).
    :param beam: The beam to convert.
    :type beam: dict
    """
    print("Starting conversion...")
    with h5py.File(os.path.join(os.getcwd(),'shadow3_out.opmd.h5'), 'w') as opmd_h5:

        number_of_time_steps = 1


        E_max = max(beam['photon_energy']['value'])
        E_min = min(beam['photon_energy']['value'])

        sum_x = 0.0
        sum_y = 0.0

        # Write opmd
        # Setup the root attributes.
        it = 0

        print(" Setup file structure.")
        opmd.setup_root_attr( opmd_h5 )

        full_meshes_path = opmd.get_basePath(opmd_h5, it) + opmd_h5.attrs["meshesPath"]
        full_particles_path = opmd.get_basePath(opmd_h5, it) + opmd_h5.attrs["particlesPath"]
        # Setup basepath.
        time = 0.0
        opmd.setup_base_path( opmd_h5, iteration=it, time=time, time_step=0.0)
        opmd_h5.create_group(full_meshes_path)
        opmd_h5.create_group(full_particles_path)
        meshes = opmd_h5[full_meshes_path]
        particles = opmd_h5[full_particles_path]


        ### PARTICLES (PHOTONS)
        opmd.setup_root_attr( opmd_h5 )
        # Get number of time slices in wpg output, assuming horizontal and vertical polarizations have same dimensions, which is always true for wpg output.

        # Path to the photons
        print(" Setup photons.")
        full_photons_path_name = b"photons"
        particles.create_group(full_photons_path_name)
        photons = particles[full_photons_path_name]

        # Create the photon groups
        photons_charge = photons.create_group(b"charge")
        photons_mass = photons.create_group(b"mass")
        photons_momentum = photons.create_group(b"momentum")
        photons_position = photons.create_group(b"position")

        # Write charge attributes
        photons_charge.attrs['unitDimension'] = numpy.array([0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0], dtype=numpy.float64)
        photons_charge.attrs['unitSI'] = numpy.float64(1.0)
        photons_charge.attrs['value'] = numpy.float64(0.0)

        # Write mass attributes
        photons_mass.attrs['unitDimension'] = numpy.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=numpy.float64)
        photons_mass.attrs['unitSI'] = numpy.float64(1.0)
        photons_mass.attrs['value'] = numpy.float64(0.0)

        # Write photon momenta
        print( " Writing photon momenta.")
        photons_momentum.attrs['unitDimension'] = numpy.array([1.0,1.0,-1.0, 0.0, 0.0, 0.0, 0.0], dtype=numpy.float64)
        photons_momentum.attrs['unitSI'] = hbar*1e10 # Shadow delivers k in units of 1/A
        photons_momentum.create_dataset('x', (number_of_rays,), dtype=numpy.float64, compression='gzip')
        photons_momentum['x'][:] = beam['Kx']['value']
        photons_momentum.create_dataset('y', (number_of_rays,), dtype=numpy.float64, compression='gzip')
        photons_momentum['y'][:] = -1.0*beam['Kz']['value'] # Prefactor because switching between Shadow3 coordinates to WPG/SimEx coordinate system (z = beam direction, x=horizontal left to righ, y=vertical top to bottom).
        photons_momentum.create_dataset('z', (number_of_rays,), dtype=numpy.float64, compression='gzip')
        photons_momentum['z'][:] = beam['Ky']['value'] # Prefactor because switching between Shadow3 coordinates to WPG/SimEx coordinate system (z = beam direction, x=horizontal left to righ, y=vertical top to bottom).

        # Write photon positions.
        print(" Writing photon positions.")
        photons_position.attrs['unitDimension'] = numpy.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=numpy.float64)
        photons_position.attrs['unitSI'] = numpy.float64(1.0)
        photons_position.create_dataset('x', (number_of_rays,), dtype=numpy.float64, compression='gzip')
        photons_position['x'][:] = beam['X']['value']
        photons_position.create_dataset('y', (number_of_rays,), dtype=numpy.float64, compression='gzip')
        photons_position['y'][:] = -1.0*beam['Z']['value'] # Prefactor because switching between Shadow3 coordinates to WPG/SimEx coordinate system (z = beam direction, x=horizontal left to righ, y=vertical top to bottom).
        photons_position.create_dataset('z', (number_of_rays,), dtype=numpy.float64, compression='gzip')
        photons_position['z'][:] = beam['Y']['value'] # Prefactor because switching between Shadow3 coordinates to WPG/SimEx coordinate system (z = beam direction, x=horizontal left to righ, y=vertical top to bottom).

        # Write photon weights
        print(" Writing photon weights.")
        photons_weighting = photons.create_dataset(b"weighting", (number_of_rays,), dtype=numpy.float64)
        photons_weighting.attrs['unitDimension'] = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=numpy.float64)
        photons_weighting.attrs['unitSI'] = numpy.float64(1.0)
        photons_weighting.attrs['normalized'] = numpy.string_('True')
        weights = beam['intensity']['value']/sum(beam['intensity']['value'])
        photons_weighting[:] = weights

        print(" Closing hdf5 file.")
        opmd_h5.close()
        print("... Conversion done.")


###################333
print("Getting data from beam object.")

# Get required data from beam object.
beam_data_columns = in_object_1._beam.getshcol(col = [ 1,  # x [user's units]
                                                       2,  # y [user's units]
                                                       3,  # z [user's units]
                                                       7,  # Ex s-pol
                                                       8,  # Ey s-pol
                                                       9,  # Ez s-pol
                                                      11,  # Energy [eV]
                                                      14,  # s-pol phase
                                                      15,  # p-pol phase
                                                      16,  # Ex p-pol
                                                      17,  # Ey p-pol
                                                      18,  # Ez p-pol
                                                      23,  # total intensity
                                                      27,  # Kx
                                                      28,  # Ky
                                                      29   # Kz
                                               ],
                                               nolost=1, # Don't use lost rays.
                                              )
# Count number of unlost rays.
number_of_rays = len(beam_data_columns[0])

beam_data_dict = {
                   'X' :             {'value' : beam_data_columns[ 0], 'unit' : LENGTH_UNIT},
                   'Y' :             {'value' : beam_data_columns[ 1], 'unit' : LENGTH_UNIT},
                   'Z' :             {'value' : beam_data_columns[ 2], 'unit' : LENGTH_UNIT},
                   'Ex_s' :          {'value' : beam_data_columns[ 3], 'unit' : 'V/m'},
                   'Ey_s' :          {'value' : beam_data_columns[ 4], 'unit' : 'V/m'},
                   'Ez_s' :          {'value' : beam_data_columns[ 5], 'unit' : 'V/m'},
                   'photon_energy' : {'value' : beam_data_columns[ 6], 'unit' : 'eV'},
                   'phase_s':        {'value' : beam_data_columns[ 7], 'unit' : 'rad'},
                   'phase_p':        {'value' : beam_data_columns[ 8], 'unit' : 'rad'},
                   'Ex_p' :          {'value' : beam_data_columns[ 9], 'unit' : LENGTH_UNIT},
                   'Ey_p' :          {'value' : beam_data_columns[10], 'unit' : LENGTH_UNIT},
                   'Ez_p' :          {'value' : beam_data_columns[11], 'unit' : LENGTH_UNIT},
                   'intensity':      {'value' : beam_data_columns[12], 'unit' : 'W/LENGTH_UNIT/LENGTH_UNIT'},
                   'Kx' :            {'value' : beam_data_columns[13], 'unit' : '1/Angstrom'},
                   'Ky' :            {'value' : beam_data_columns[14], 'unit' : '1/Angstrom'},
                   'Kz' :            {'value' : beam_data_columns[15], 'unit' : '1/Angstrom'},
                   }

convertToOPMD(beam_data_dict)


