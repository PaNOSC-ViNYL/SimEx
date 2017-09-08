""" :module shadow_to_opmd: Script to save a Shadow beams object to OpenPMD compliant hdf5.
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
from scipy import constants

import h5py
import math
import numpy
import os
import sys

### ADOPT ME
utilities_path = "/home/grotec/Codes/eucall-software/simex_platform/develop/Sources/python/SimEx/Utilities"
if utilities_path not in sys.path:
    sys.path.insert(0, utilities_path)

# Get some constants.
c = constants.speed_of_light
eps0 = constants.epsilon_0
e = constants.e
hbar = constants.hbar

LENGTH_UNIT = 'm'

import OpenPMDTools as opmd

def convertToOPMD(beam, number_of_x_bins=None, number_of_y_bins=None, number_of_t_bins=None):
    """ Format beam entries to particles and fields in openpmd file (hdf5).
    :param beam: The beam to convert.
    :type beam: dict
    """

    # Set default number of bins.
    if number_of_x_bins is None:
        number_of_x_bins = 128
    if number_of_y_bins is None:
        number_of_y_bins = 128
    if number_of_t_bins is None:
        number_of_t_bins = 128

    print("Starting conversion...")
    with h5py.File(os.path.join(os.getcwd(),'shadow3_out.opmd.h5'), 'w') as opmd_h5:

        opmd.setup_root_attr( opmd_h5 )

        number_of_rays = beam['X'].shape[0]
        print ("Found %d good rays." % (number_of_rays))

        E_max = max(beam['photon_energy'])
        E_min = min(beam['photon_energy'])

        sum_x = 0.0
        sum_y = 0.0

        # Write opmd
        # Setup the root attributes.
        it = 0

        print(" Setup file structure.")
        opmd.setup_root_attr( opmd_h5 )

        # Get 3D intensity histogram.
        xyz_array = numpy.empty((number_of_rays, 3))
        print(xyz_array.shape)
        xyz_array[:,0] = beam["X"]
        xyz_array[:,1] = -beam["Z"]
        xyz_array[:,2] = -c*beam["Y"]

        # Get E fields in cartesian components.
        E_s = numpy.sqrt(beam["I_s"]) * numpy.exp(1j*beam["phi_s"])
        E_p = numpy.sqrt(beam["I_p"]) * numpy.exp(1j*beam["phi_p"])

        # Get photon number for horizontal polarized light.
        N_s = beam["I_s"] / beam["photon_energy"] / e
        N_p = beam["I_p"] / beam["photon_energy"] / e

        # Get fields, number of photons and phases via histograms.
        E_horz_real, xyt_edges = numpy.histogramdd(sample=xyz_array,
                                        bins=[number_of_x_bins, number_of_y_bins, number_of_t_bins],
                                        normed=False,
                                        weights=numpy.real(E_s),
                                        )
        E_horz_imag, xyt_edges = numpy.histogramdd(sample=xyz_array,
                                        bins=[number_of_x_bins, number_of_y_bins, number_of_t_bins],
                                        normed=False,
                                        weights=numpy.imag(E_s),
                                        )
        E_vert_real, xyt_edges = numpy.histogramdd(sample=xyz_array,
                                        bins=[number_of_x_bins, number_of_y_bins, number_of_t_bins],
                                        normed=False,
                                        weights=numpy.real(E_p),
                                        )
        E_vert_imag, xyt_edges = numpy.histogramdd(sample=xyz_array,
                                        bins=[number_of_x_bins, number_of_y_bins, number_of_t_bins],
                                        normed=False,
                                        weights=numpy.imag(E_p),
                                        )

        Nph_horz, xyt_edges = numpy.histogramdd(sample=xyz_array,
                                        bins=[number_of_x_bins, number_of_y_bins, number_of_t_bins],
                                        normed=False,
                                        weights=N_s,
                                        )

        Nph_vert, xyt_edges = numpy.histogramdd(sample=xyz_array,
                                        bins=[number_of_x_bins, number_of_y_bins, number_of_t_bins],
                                        normed=False,
                                        weights=N_p
                                        )
        phi_horz, xyt_edges = numpy.histogramdd(sample=xyz_array,
                                        bins=[number_of_x_bins, number_of_y_bins, number_of_t_bins],
                                        normed=False,
                                        weights=beam["phi_s"],
                                        )

        phi_vert, xyt_edges = numpy.histogramdd(sample=xyz_array,
                                        bins=[number_of_x_bins, number_of_y_bins, number_of_t_bins],
                                        normed=False,
                                        weights=beam["phi_p"]
                                        )


        index_vs_t = numpy.empty((number_of_rays, 2))
        index_vs_t[:,0] = -c*beam["Y"]
        index_vs_t[:,1] = beam["ray_index"]
        rays_histogram, t_edges, index_edges = numpy.histogram2d(x=-c*beam["Y"],
                                                    y=beam["ray_index"],
                                                    bins=[number_of_t_bins, number_of_rays+1],)

        # Get bin centers and bin lengths
        x_los = xyt_edges[0][:-1]
        x_his = xyt_edges[0][1:]
        x_cnt = 0.5*(x_his + x_los)
        x_len = abs(x_cnt[1] - x_cnt[0])
        y_los = xyt_edges[1][:-1]
        y_his = xyt_edges[1][1:]
        y_cnt = 0.5*(y_his + y_los)
        y_len = abs(y_cnt[1] - y_cnt[0])
        t_los = xyt_edges[2][:-1]
        t_his = xyt_edges[2][1:]
        t_cnt = 0.5*(t_his + t_los)
        t_len = abs(t_cnt[1])

        # Get 3-D voxel (x-y-t) volume.
        xyt_voxel_volume = x_len * y_len * t_len # [m**2 s]

        # Scale photon number by voxel volume.
        Nph_horz *= xyt_voxel_volume
        Nph_vert *= xyt_voxel_volume

        # Get "voxel phase" (this must be wrong ...).
        phi_horz = numpy.mod(phi_horz, 2.*math.pi)
        phi_horz = numpy.mod(phi_vert, 2.*math.pi)

        sum_x = 0.0
        sum_y = 0.0
        for it in range(number_of_t_bins):


            # Setup basepaths.
            full_meshes_path = opmd.get_basePath(opmd_h5, it) + opmd_h5.attrs["meshesPath"]
            full_particles_path = opmd.get_basePath(opmd_h5, it) + opmd_h5.attrs["particlesPath"]

            opmd.setup_base_path( opmd_h5, iteration=it, time=t_cnt[it], time_step=t_len)
            meshes = opmd_h5.create_group(full_meshes_path)
            particles = opmd_h5.create_group(full_particles_path)

            ### PARTICLES (PHOTONS)
            # Get all photons in this time slice.
            it_rays= numpy.where( -c*beam["Y"] >= t_los[it] )
            tmp = beam["Y"][it_rays]
            it_rays = numpy.where( -c*tmp <= t_his[it] )[0].tolist()
            number_of_it_rays = len(it_rays)
            print ("Rays in this slice (it=%d) : %s (length %d)" % (it, str(it_rays), number_of_it_rays))

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
            photons_momentum.create_dataset('x', (number_of_it_rays,), dtype=numpy.float64, compression='gzip')
            photons_momentum['x'][:] = beam['K_x'][it_rays]
            photons_momentum.create_dataset('y', (number_of_it_rays,), dtype=numpy.float64, compression='gzip')
            photons_momentum['y'][:] = -1.0*beam['K_z'][it_rays] # Prefactor because switching between Shadow3 coordinates to WPG/SimEx coordinate system (z = beam direction, x=horizontal left to righ, y=vertical top to bottom).
            photons_momentum.create_dataset('z', (number_of_it_rays,), dtype=numpy.float64, compression='gzip')
            photons_momentum['z'][:] = beam['K_y'][it_rays] # Prefactor because switching between Shadow3 coordinates to WPG/SimEx coordinate system (z = beam direction, x=horizontal left to righ, y=vertical top to bottom).

            # Write photon positions.
            print(" Writing photon positions.")
            photons_position.attrs['unitDimension'] = numpy.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=numpy.float64)
            photons_position.attrs['unitSI'] = numpy.float64(1.0)
            photons_position.create_dataset('x', (number_of_it_rays,), dtype=numpy.float64, compression='gzip')
            photons_position['x'][:] = beam['X'][it_rays]
            photons_position.create_dataset('y', (number_of_it_rays,), dtype=numpy.float64, compression='gzip')
            photons_position['y'][:] = -1.0*beam['Z'][it_rays] # Prefactor because switching between Shadow3 coordinates to WPG/SimEx coordinate system (z = beam direction, x=horizontal left to righ, y=vertical top to bottom).
            photons_position.create_dataset('z', (number_of_it_rays,), dtype=numpy.float64, compression='gzip')
            photons_position['z'][:] = beam['Y'][it_rays] # Prefactor because switching between Shadow3 coordinates to WPG/SimEx coordinate system (z = beam direction, x=horizontal left to righ, y=vertical top to bottom).

            # Write photon weights
            print(" Writing photon weights.")
            photons_weighting = photons.create_dataset(b"weighting", (number_of_it_rays,), dtype=numpy.float64)
            photons_weighting.attrs['unitDimension'] = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=numpy.float64)
            photons_weighting.attrs['unitSI'] = numpy.float64(1.0)
            photons_weighting.attrs['normalized'] = numpy.string_('False')
            weights = beam['I_tot'][it_rays]
            photons_weighting[:] = weights


            ### FIELDS (NUMBER OF PHOTONS)
            # Path to the E field, within the h5 file.
            full_e_path_name = b"E"
            E = meshes.create_group(full_e_path_name)

            # Create the dataset (2d cartesian grid)
            E.create_dataset(b"x", (number_of_x_bins, number_of_y_bins), dtype=numpy.complex64, compression='gzip')
            E.create_dataset(b"y", (number_of_x_bins, number_of_y_bins), dtype=numpy.complex64, compression='gzip')

            # Write the common metadata for the group
            E.attrs["geometry"] = numpy.string_("cartesian")
            # Get grid geometry.
            nx = number_of_x_bins
            xMax = max(x_cnt)
            xMin = min(x_cnt)
            dx = x_len
            ny = number_of_y_bins
            yMax = max(y_cnt)
            yMin = min(y_cnt)
            dy = y_len
            E.attrs["gridSpacing"] = numpy.array( [dx,dy], dtype=numpy.float64)
            E.attrs["gridGlobalOffset"] = numpy.array([0., 0.], dtype=numpy.float64)
            E.attrs["gridUnitSI"] = numpy.float64(1.0)
            E.attrs["dataOrder"] = numpy.string_("C")
            E.attrs["axisLabels"] = numpy.array([b"x",b"y"])
            E.attrs["unitDimension"] = \
               numpy.array([1.0, 1.0, -3.0, -1.0, 0.0, 0.0, 0.0 ], dtype=numpy.float64)
               #            L    M     T     I  theta  N    J
               # E is in volts per meters: V / m = kg * m / (A * s^3)
               # -> L * M * T^-3 * I^-1

            # Add time information
            E.attrs["timeOffset"] = 0.  # Time offset with respect to basePath's time

            # Write attribute that is specific to each dataset:
            # - Staggered position within a cell
            E["x"].attrs["position"] = numpy.array([0.0, 0.5], dtype=numpy.float32)
            E["y"].attrs["position"] = numpy.array([0.5, 0.0], dtype=numpy.float32)

            # - Conversion factor to SI units
            # WPG writes E fields in units of sqrt(W/mm^2), i.e. it writes E*sqrt(c * eps0 / 2).
            # Unit analysis:
            # [E] = V/m
            # [eps0] = As/Vm
            # [c] = m/s
            # ==> [E^2 * eps0 * c] = V**2/m**2 * As/Vm * m/s = V*A/m**2 = W/m**2 = [Intensity]
            # Converting to SI units by dividing by sqrt(c*eps0/2)*1e3, 1e3 for conversion from mm to m.
            E["x"].attrs["unitSI"] = numpy.float64(1.0  / math.sqrt(0.5 * c * eps0) / 1.0e3 )
            E["y"].attrs["unitSI"] = numpy.float64(1.0  / math.sqrt(0.5 * c * eps0) / 1.0e3 )

            # Copy the fields.
            Ex = E_horz_real[:,:,it] + 1j * E_horz_imag[:,:,it]
            Ey = E_vert_real[:,:,it] + 1j * E_vert_imag[:,:,it]
            E["x"][:,:] = Ex
            E["y"][:,:] = Ey

            # Path to the photons
            print(" Setup number_of_photons mesh.")
            full_photons_path_name = b"Nph"
            Nph = meshes.create_group(full_photons_path_name)
            # Create the dataset (2d cartesian grid)
            Nph.create_dataset(b"x", (number_of_x_bins, number_of_y_bins), dtype=numpy.float32, compression='gzip')
            Nph.create_dataset(b"y", (number_of_x_bins, number_of_y_bins), dtype=numpy.float32, compression='gzip')

            # Write the common metadata for the group
            Nph.attrs["geometry"] = numpy.string_("cartesian")
            Nph.attrs["gridSpacing"] = numpy.array( [x_len,y_len], dtype=numpy.float64)
            Nph.attrs["gridGlobalOffset"] = numpy.array([0.0, 0.0], dtype=numpy.float64)
            Nph.attrs["gridUnitSI"] = numpy.float64(1.0)
            Nph.attrs["dataOrder"] = numpy.string_("C")
            Nph.attrs["axisLabels"] = numpy.array([b"x",b"y"])
            Nph.attrs["unitDimension"] = \
               numpy.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=numpy.float64)

            # Add time information
            Nph.attrs["timeOffset"] = 0.  # Time offset with respect to basePath's time
            # Nph - Staggered position within a cell
            Nph["x"].attrs["position"] = numpy.array([0.0, 0.5], dtype=numpy.float32)
            Nph["y"].attrs["position"] = numpy.array([0.5, 0.0], dtype=numpy.float32)
            Nph["x"].attrs["unitSI"] = numpy.float64(1.0 )
            Nph["y"].attrs["unitSI"] = numpy.float64(1.0 )

            # Calculate number of photons via intensity and photon energy.
            # Since fields are stored as sqrt(W/mm^2), have to convert to W/m^2 (factor 1e6 below).
            number_of_photons_x = Nph_horz[:,:,it]
            number_of_photons_y = Nph_vert[:,:,it]
            sum_x += number_of_photons_x.sum()
            sum_y += number_of_photons_y.sum()
            Nph["x"][:,:] = number_of_photons_x
            Nph["y"][:,:] = number_of_photons_y

            ### Phases.
            # Path to phases
            full_phases_path_name = b"phases"
            meshes.create_group(full_phases_path_name)
            phases = meshes[full_phases_path_name]

            # Create the dataset (2d cartesian grid)
            phases.create_dataset(b"x", (number_of_x_bins, number_of_y_bins), dtype=numpy.float32, compression='gzip')
            phases.create_dataset(b"y", (number_of_x_bins, number_of_y_bins), dtype=numpy.float32, compression='gzip')

            # Write the common metadata for the group
            phases.attrs["geometry"] = numpy.string_("cartesian")
            phases.attrs["gridSpacing"] = numpy.array( [x_len,y_len], dtype=numpy.float64)
            phases.attrs["gridGlobalOffset"] = numpy.array([0.0, 0.0], dtype=numpy.float64)
            phases.attrs["gridUnitSI"] = numpy.float64(1.0)
            phases.attrs["dataOrder"] = numpy.string_("C")
            phases.attrs["axisLabels"] = numpy.array([b"x",b"y"])
            phases.attrs["unitDimension"] = \
               numpy.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=numpy.float64)

            # Add time information
            phases.attrs["timeOffset"] = 0.  # Time offset with respect to basePath's time
            # phases - Staggered position within a cell
            phases["x"].attrs["position"] = numpy.array([0.0, 0.5], dtype=numpy.float32)
            phases["y"].attrs["position"] = numpy.array([0.5, 0.0], dtype=numpy.float32)
            phases["x"].attrs["unitSI"] = numpy.float64(1.0 )
            phases["y"].attrs["unitSI"] = numpy.float64(1.0 )

            # Add time information
            phases.attrs["timeOffset"] = 0.  # Time offset with respect to basePath's time
            # phases positions. - Staggered position within a cell
            phases["x"].attrs["position"] = numpy.array([0.0, 0.5], dtype=numpy.float32)
            phases["y"].attrs["position"] = numpy.array([0.5, 0.0], dtype=numpy.float32)

            phases["x"][:,:] = phi_horz[:,:,it]
            phases["y"][:,:] = phi_vert[:,:,it]

        print(" Closing hdf5 file.")
    print("... Conversion done.")


###################333
print("Getting data from beam object.")

# Get required data from beam object.
beam_data_columns = in_object_1._beam.getshcol(col = range(1,34),
                                               nolost=1, # Don't use lost rays.
                                              )
# Count number of unlost rays.
number_of_rays = len(beam_data_columns[0])

beam_data_dict = {
                "X"                      : beam_data_columns[ 0],   # X spatial coordinate [user's unit]
                "Y"                      : beam_data_columns[ 1],   # Y spatial coordinate [user's unit]
                "Z"                      : beam_data_columns[ 2],   # Z spatial coordinate [user's unit]
                "Xp"                     : beam_data_columns[ 3],   # Xp direction or divergence [rads]
                "Yp"                     : beam_data_columns[ 4],   # Yp direction or divergence [rads]
                "Zp"                     : beam_data_columns[ 5],   # Zp direction or divergence [rads]
                "E_sx"                   : beam_data_columns[ 6],   # X component of the electromagnetic vector (s-polariz)
                "E_sy"                   : beam_data_columns[ 7],   # Y component of the electromagnetic vector (s-polariz)
                "E_sz"                   : beam_data_columns[ 8],   # Z component of the electromagnetic vector (s-polariz)
                "lost"                   : beam_data_columns[ 9],   # Lost ray flag
                "photon_energy"          : beam_data_columns[10],   # Energy [eV]
                "ray_index"              : beam_data_columns[11],   # Ray index
                "lopt"                   : beam_data_columns[12],   # Optical path length
                "phi_s"                  : beam_data_columns[13],   # Phase (s-polarization) in rad
                "phi_p"                  : beam_data_columns[14],   # Phase (p-polarization) in rad
                "E_px"                   : beam_data_columns[15],   # X component of the electromagnetic vector (p-polariz)
                "E_py"                   : beam_data_columns[16],   # Y component of the electromagnetic vector (p-polariz)
                "E_pz"                   : beam_data_columns[17],   # Z component of the electromagnetic vector (p-polariz)
                "lambda"                 : beam_data_columns[18],   # Wavelength [A]
                "radius"                 : beam_data_columns[19],   # R= SQRT(X^2+Y^2+Z^2)
                "propagation_axis_angle" : beam_data_columns[20],   # angle from Y axis
                "E_length"               : beam_data_columns[21],   # the magnituse of the Electromagnetic vector
                "I_tot"                  : beam_data_columns[22],   # |E|^2 (total intensity)
                "I_s"                    : beam_data_columns[23],   # total intensity for s-polarization
                "I_p"                    : beam_data_columns[24],   # total intensity for p-polarization
                "K"                      : beam_data_columns[25],   # K = 2 pi / lambda [A^-1]
                "K_x"                    : beam_data_columns[26],   # K = 2 pi / lambda * col4 [A^-1]
                "K_y"                    : beam_data_columns[27],   # K = 2 pi / lambda * col5 [A^-1]
                "K_z"                    : beam_data_columns[28],   # K = 2 pi / lambda * col6 [A^-1]
                "S0"                     : beam_data_columns[29],   # S0-stokes = |Es|^2 + |Ep|^2
                "S1"                     : beam_data_columns[30],   # S1-stokes = |Es|^2 - |Ep|^2
                "S2"                     : beam_data_columns[31],   # S2-stokes = 2 |Es| |Ep| cos(phase_s-phase_p)
                "S3"                     : beam_data_columns[32],   # S3-stokes = 2 |Es| |Ep| sin(phase_s-phase_p)
                   }

convertToOPMD(beam_data_dict)


