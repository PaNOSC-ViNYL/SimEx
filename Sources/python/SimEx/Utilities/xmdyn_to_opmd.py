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
import h5py
import math
import numpy
import os
from scipy import constants
from SimEx.Utilities.Units import second, meter, electronvolt, joule
from SimEx.Calculate.XMDYNDemoPhotonMatterInteractor import PMIDemo
from periodictable import elements

# Get some constants.
c = constants.speed_of_light
eps0 = constants.epsilon_0
e = constants.e

from SimEx.Utilities import OpenPMDTools as opmd

def convertToOPMD(input_path):
    """ Convert xmdyn output stored on disk into an openPMD compatible hdf5.

    :param input_path: The directory containing xmdyn output.
    :type input_path: str

    """

    # Check input path.
    if not os.path.isdir(input_path):
        raise IOError("Directory %s not found." % (input_path))

    # Check all required data is present.
    snapshot_dir = os.path.join(input_path, 'snp')
    if not os.path.isdir(snapshot_dir):
        raise IOError("%s does not contain a snapshot directory snp/." % (input_path))

    # Get all snapshot directories.
    snapshots = os.listdir(snapshot_dir)

    # Get number of snapshots.
    number_of_snapshots = len(snapshots)
    if len(number_of_snapshots) == 0:
        raise RuntimeError("%s does not contain any snapshots." % (snapshot_dir))

    # Sort dirs.
    snapshots.sort()

    # Check and parse xmdyn input file to extract time steps and photon numbers.
    input_file_path = os.path.join(input_path,'xparams.txt') # We use the file written at xmdyn runtime which reflects the actual state of affairs.
    if not os.path.isfile(input_file_path):
        raise IOError("XMDYN input file %s was not found." % (input_file_path))

    xmdyn_parameters = _parse_xmdyn_xparams(input_file_path)

    # Setup a pmi demo object to facilitate loading of data.
    pmi = PMIDemo()

    # Open in and out files.
    with h5py.File("xmdy_out.opmd.h5", 'w') as opmd_h5:

        time_max = xmdyn_parameters['stop_time'].m_as(second)
        time_min = xmdyn_parameters['start_time'].m_as(second)
        time_step = xmdyn_parameters['time_step'].m_as(second)

        photon_energy = xmdyn_parameters['photon_energy'].m_as(joule)

        sum_x = 0.0
        sum_y = 0.0

        for it, snp in enumerate(snapshots):

            # Load snapshot data as a dict
            snapshot_dict = pmi.f_load_snp_from_dir(snp)

            # Write opmd
            # Setup the root attributes for iteration 0
            opmd.setup_root_attr( opmd_h5 )

            full_meshes_path = opmd.get_basePath(opmd_h5, it) + opmd_h5.attrs["meshesPath"]
            # Setup basepath.
            time=time_min+it*time_step
            opmd.setup_base_path( opmd_h5, iteration=it, time=time, time_step=time_step)
            opmd_h5.create_group(full_meshes_path)
            meshes = opmd_h5[full_meshes_path]

            # Form factors
            ff_path = b"form factor"
            meshes.create_group(ff_path)
            ff = meshes[ff_path]

            # Create the dataset (1d grid)
            f0 = ff.create_dataset(b"f0", snapshot_dict['f0'].shape, dtype=numpy.float64, compression='gzip')
            q  = ff.create_dataset(b"q", snapshot_dict['Q'].shape, dtype=numpy.float64, compression='gzip')

            f0.attrs["gridUnitSI"] = numpy.float64(1.0)
            f0.attrs["dataOrder"] = numpy.string_("C")
            f0.attrs["axisLabels"] = numpy.array([b"f0"])
            f0.attrs["unitDimension"] = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], dtype=numpy.float64)
            #                                           L    M    T    I  th     N    J
            q.attrs["gridUnitSI"] = numpy.float64(1.0)
            q.attrs["dataOrder"] = numpy.string_("C")
            q.attrs["axisLabels"] = numpy.array([b"q"])
            q.attrs["unitDimension"] = numpy.array([-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], dtype=numpy.float64)
            #                                          L    M    T    I   th    N    J

            # Copy the fields.
            ff["q"][:]= snapshot_dict['Q']
            ff["f0"][:] = snapshot_dict['f0']

            # Particles.
            full_particles_path = opmd.get_basePath(opmd_h5, it) + opmd_h5.attrs["particlesPath"]
            opmd.setup_base_path(opmd_h5, iteration=it, time=time, time_step=time_step)
            particles = opmd_h5.create_group(full_particles_path)

            # Atoms and ions.
            ions_path= b"Ions"
            ions = particles.create_group(ions_path)

            # Loop over elements
            #unique_atom_numbers = snapshot_dict['Z'].unique()
            #for uatm_idx, uatm in enumerate(unique_atom_numbers):
                #symbol = elements[uatm].symbol
                #species = ions.create_group(symbol)

            # Loop over atom types and create a group for each.
            for idx, econf in snapshot_dict['econf']:
                econf_group = ions.create_group(econf)

                indices = numpy.where( snapshot_dict['T'] == idx )
                position = econf_group.create_group('position')
                x = snapshot_dict['r'][indices,0]
                y = snapshot_dict['r'][indices,1]
                z = snapshot_dict['r'][indices,2]
                position.create_dataset('x', data=x)
                position.create_dataset('y', data=y)
                position.create_dataset('z', data=z)

                velocity = econf_group.create_group('velocity')
                vx = snapshot_dict['v'][indices,0]
                vy = snapshot_dict['v'][indices,1]
                vz = snapshot_dict['v'][indices,2]
                velocity.create_dataset('x', data=vx)
                velocity.create_dataset('y', data=vy)
                velocity.create_dataset('z', data=vz)

                charge = econf_group.create_dataset('charge', data=snapshot_dict['q'][indices])
                mass = econf_group.create_dataset('mass', data=snapshot_dict['m'][indices])
                uid = econf_group.create_dataset('id', data=snapshot_dict['uid'][indices])
                Z = econf_group.create_dataset('Z', data=snapshot_dict['q'][indices])


            ## Electrons
            #electons_path = b"Electrons"
            #electrons = particles.create_group(electrons_path)

            ### Loop over all particles.
            ##for idx, uid in snapshot_dict['uid']:
                ### Check if ion or electron.
                ##is_electron = snapshot_dict['Z'][idx] == 0

                ##if is_electron:
                    ##particle = electrons.create_group(uid)

                ##else:
                    ##particle = ions.create_group(uid)





def _convert_from_frequency_representation(h5, opmd_h5, data_shape, pulse_energy=1.0e-3, pulse_duration=23.0e-15):
    """ Converter for non-time dependent wavefronts in frequency representation.
    Requires knowledge of pulse energy and pulse duration to allow photon number calculation.
    """

    number_of_x_meshpoints = data_shape[0]
    number_of_y_meshpoints = data_shape[1]

    photon_energy = h5['params/photonEnergy'].value # eV
    photon_energy = photon_energy * e # Convert to J

    # Copy misc and params from original wpg output.
    opmd_h5.create_group('history/parent')
    try:
        h5.copy('/params', opmd_h5['history/parent'])
        h5.copy('/misc', opmd_h5['history/parent'])
        h5.copy('/history', opmd_h5['history/parent'])
    # Some keys may not exist, e.g. if the input file comes from a non-simex wpg run.
    except KeyError:
        pass
    except:
        raise

    sum_x = 0.0
    sum_y = 0.0

    # Write opmd
    # Setup the root attributes.
    it = 0
    opmd.setup_root_attr( opmd_h5 )

    full_meshes_path = opmd.get_basePath(opmd_h5, it) + opmd_h5.attrs["meshesPath"]
    # Setup basepath.
    time = 0.0
    time_step = pulse_duration
    opmd.setup_base_path( opmd_h5, iteration=it, time=time, time_step=time_step)
    opmd_h5.create_group(full_meshes_path)
    meshes = opmd_h5[full_meshes_path]

    ## Path to the E field, within the h5 file.
    #full_e_path_name = b"E"
    #meshes.create_group(full_e_path_name)
    #E = meshes[full_e_path_name]

    ## Create the dataset (2d cartesian grid)
    #E.create_dataset(b"x", (number_of_x_meshpoints, number_of_y_meshpoints), dtype=numpy.complex64, compression='gzip')
    #E.create_dataset(b"y", (number_of_x_meshpoints, number_of_y_meshpoints), dtype=numpy.complex64, compression='gzip')

    ## Write the common metadata for the group
    #E.attrs["geometry"] = numpy.string_("cartesian")
    ## Get grid geometry.
    nx = h5['params/Mesh/nx'].value
    xMax = h5['params/Mesh/xMax'].value
    xMin = h5['params/Mesh/xMin'].value
    dx = (xMax - xMin) / nx
    ny = h5['params/Mesh/ny'].value
    yMax = h5['params/Mesh/yMax'].value
    yMin = h5['params/Mesh/yMin'].value
    dy = (yMax - yMin) / ny
    #E.attrs["gridSpacing"] = numpy.array( [dx,dy], dtype=numpy.float64)
    #E.attrs["gridGlobalOffset"] = numpy.array([h5['params/xCentre'].value, h5['params/yCentre'].value], dtype=numpy.float64)
    #E.attrs["gridUnitSI"] = numpy.float64(1.0)
    #E.attrs["dataOrder"] = numpy.string_("C")
    #E.attrs["axisLabels"] = numpy.array([b"x",b"y"])
    #E.attrs["unitDimension"] = \
       #numpy.array([1.0, 1.0, -3.0, -1.0, 0.0, 0.0, 0.0 ], dtype=numpy.float64)
       ##            L    M     T     I  theta  N    J
       ## E is in volts per meters: V / m = kg * m / (A * s^3)
       ## -> L * M * T^-3 * I^-1

    ## Add time information
    #E.attrs["timeOffset"] = 0.  # Time offset with respect to basePath's time

    ## Write attribute that is specific to each dataset:
    ## - Staggered position within a cell
    #E["x"].attrs["position"] = numpy.array([0.0, 0.5], dtype=numpy.float32)
    #E["y"].attrs["position"] = numpy.array([0.5, 0.0], dtype=numpy.float32)

    ## - Conversion factor to SI units
    ## WPG writes E fields in units of sqrt(W/mm^2), i.e. it writes E*sqrt(c * eps0 / 2).
    ## Unit analysis:
    ## [E] = V/m
    ## [eps0] = As/Vm
    ## [c] = m/s
    ## ==> [E^2 * eps0 * c] = V**2/m**2 * As/Vm * m/s = V*A/m**2 = W/m**2 = [Intensity]
    ## Converting to SI units by dividing by sqrt(c*eps0/2)*1e3, 1e3 for conversion from mm to m.
    #c    = 2.998e8   # m/s
    #eps0 = 8.854e-12 # As/Vm
    #E["x"].attrs["unitSI"] = numpy.float64(1.0  / math.sqrt(0.5 * c * eps0) / 1.0e3 )
    #E["y"].attrs["unitSI"] = numpy.float64(1.0  / math.sqrt(0.5 * c * eps0) / 1.0e3 )

    # Get E fields.
    Ex = h5['data/arrEhor'][:,:,it,0] + 1j * h5['data/arrEhor'][:,:,it,1]
    Ey = h5['data/arrEver'][:,:,it,0] + 1j * h5['data/arrEver'][:,:,it,1]
    #E["x"][:,:] = Ex
    #E["y"][:,:] = Ey

    ### Number of photon fields.
    # Path to the number of photons.
    full_nph_path_name = b"Nph"
    meshes.create_group(full_nph_path_name)
    Nph = meshes[full_nph_path_name]

    # Create the dataset (2d cartesian grid)
    Nph.create_dataset(b"x", (number_of_x_meshpoints, number_of_y_meshpoints), dtype=numpy.float32, compression='gzip')
    Nph.create_dataset(b"y", (number_of_x_meshpoints, number_of_y_meshpoints), dtype=numpy.float32, compression='gzip')

    # Write the common metadata for the group
    Nph.attrs["geometry"] = numpy.string_("cartesian")
    Nph.attrs["gridSpacing"] = numpy.array( [dx,dy], dtype=numpy.float64)
    Nph.attrs["gridGlobalOffset"] = numpy.array([h5['params/xCentre'].value, h5['params/yCentre'].value], dtype=numpy.float64)
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
    number_of_photons_x = numpy.round(abs(Ex)**2)
    number_of_photons_y = numpy.round(abs(Ey)**2)
    sum_x = number_of_photons_x.sum(axis=-1).sum(axis=-1)
    sum_y = number_of_photons_y.sum(axis=-1).sum(axis=-1)

    # Conversion from Nph/s/0.1%bandwidth/mm to Nph. Sum * photon_energy must be equal to pulse energy.
    # Normalization factor.
    c_factor = pulse_energy / photon_energy
    # Normalize
    number_of_photons_x *= c_factor
    number_of_photons_y *= c_factor
    # Normalize to sum over all pixels (if != 0 ).
    if sum_x != 0.0:
        number_of_photons_x /= sum_x
    if sum_y != 0.0:
        number_of_photons_y /= sum_y

    # Write to h5 dataset.
    Nph["x"][:,:] = number_of_photons_x
    Nph["y"][:,:] = number_of_photons_y


    ### Phases.
    # Path to phases
    full_phases_path_name = b"phases"
    meshes.create_group(full_phases_path_name)
    phases = meshes[full_phases_path_name]

    # Create the dataset (2d cartesian grid)
    phases.create_dataset(b"x", (number_of_x_meshpoints, number_of_y_meshpoints), dtype=numpy.float32, compression='gzip')
    phases.create_dataset(b"y", (number_of_x_meshpoints, number_of_y_meshpoints), dtype=numpy.float32, compression='gzip')

    # Write the common metadata for the group
    phases.attrs["geometry"] = numpy.string_("cartesian")
    phases.attrs["gridSpacing"] = numpy.array( [dx,dy], dtype=numpy.float64)
    phases.attrs["gridGlobalOffset"] = numpy.array([h5['params/xCentre'].value, h5['params/yCentre'].value], dtype=numpy.float64)
    phases.attrs["gridUnitSI"] = numpy.float64(1.0)
    phases.attrs["dataOrder"] = numpy.string_("C")
    phases.attrs["axisLabels"] = numpy.array([b"x",b"y"])
    phases.attrs["unitDimension"] = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=numpy.float64)
    phases["x"].attrs["unitSI"] = numpy.float64(1.0 )
    phases["y"].attrs["unitSI"] = numpy.float64(1.0 )

    # Add time information
    phases.attrs["timeOffset"] = 0.  # Time offset with respect to basePath's time
    # phases positions. - Staggered position within a cell
    phases["x"].attrs["position"] = numpy.array([0.0, 0.5], dtype=numpy.float32)
    phases["y"].attrs["position"] = numpy.array([0.5, 0.0], dtype=numpy.float32)

    phases["x"][:,:] = numpy.angle(Ex)
    phases["y"][:,:] = numpy.angle(Ey)

    print("Found %e and %e photons for horizontal and vertical polarization, respectively." % (sum_x, sum_y))

    opmd_h5.close()
    h5.close()

def _parse_xmdyn_xparams(input_file_path):
    """ Parse XMDYN parameters file and extract timeing and photon information.

    :param input_file_path: Path to xmdyn input file.
    :type input_file_path: str

    :return: Parameter dictionary / object.
    :rtype: dict || XMDYNPhotonMatterInteractorParameters

    """
    ret = {
            'start_time' : 0.0*second,
            'stop_time'  : 100.0e-15*second,
            'time_step'  : 1.0e-16*second,
            'number_of_photons' : 3.5e14,
          }

    return ret
if __name__ == "__main__":

    # Parse arguments.
    parser = ArgumentParser(description="Convert wpg output to openPMD conform hdf5.")
    parser.add_argument("input_file", metavar="input_file",
                      help="name of the file to convert.")
    args = parser.parse_args()

    # Call the converter routine.
    convertToOPMD(args.input_file)
