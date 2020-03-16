##########################################################################
#                                                                        #
# Copyright (C) 2015-2019 Carsten Fortmann-Grote                         #
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

import math
from argparse import ArgumentParser

import h5py
import numpy
import openpmd_api as opmd
from SimEx.Utilities import OpenPMDTools as opmd_legacy
from scipy import constants

# Get some constants.
c = constants.speed_of_light
eps0 = constants.epsilon_0
e = constants.e

OPMD_DATATYPES={
                0 :opmd.Datatype.CHAR,
                1 :opmd.Datatype.UCHAR,
                2 :opmd.Datatype.SHORT,
                3 :opmd.Datatype.INT,
                4 :opmd.Datatype.LONG,
                5 :opmd.Datatype.LONG,
                6 :opmd.Datatype.USHORT,
                7 :opmd.Datatype.UINT,
                8 :opmd.Datatype.ULONG,
                9 :opmd.Datatype.ULONG,
                10:opmd.Datatype.FLOAT,
                11:opmd.Datatype.DOUBLE,
                12:opmd.Datatype.LONG_DOUBLE,
                13:opmd.Datatype.STRING,
                14:opmd.Datatype.VEC_CHAR,
                15:opmd.Datatype.VEC_SHORT,
                16:opmd.Datatype.VEC_INT,
                17:opmd.Datatype.VEC_LONG,
                18:opmd.Datatype.VEC_LONG,
                19:opmd.Datatype.VEC_UCHAR,
                20:opmd.Datatype.VEC_USHORT,
                21:opmd.Datatype.VEC_UINT,
                22:opmd.Datatype.VEC_ULONG,
                23:opmd.Datatype.VEC_ULONG,
                24:opmd.Datatype.VEC_FLOAT,
                25:opmd.Datatype.VEC_DOUBLE,
                26:opmd.Datatype.VEC_LONG_DOUBLE,
                27:opmd.Datatype.VEC_STRING,
                28:opmd.Datatype.ARR_DBL_7,
                29:opmd.Datatype.BOOL,
                }


def convertToOPMD(input_file):
    """ Take native wpg output and rewrite in openPMD conformant way.
    :param input_file: The hdf5 file to be converted.
    :type  input_file: string

    :example: convertToOPMD(input_file="prop_out.h5")
    """
    # Check input file.
    if not h5py.is_hdf5(input_file):
        raise IOError("Not a valid hdf5 file: %s. " % (input_file))

    # Read the data into memory.
    with h5py.File( input_file, 'r') as h5:

        ## Branch off if this is a non-time dependent calculation in frequency domain.
        #if data_shape[2] == 1 and h5['params/wDomain'][()] == "frequency":
            ## Time independent calculation in frequency domain.
            #_convert_from_frequency_representation(h5, opmd_h5, data_shape)
            #return

        number_of_x_meshpoints = h5['params/Mesh/nx'][()]
        number_of_y_meshpoints = h5['params/Mesh/ny'][()]
        number_of_time_steps =   h5['params/Mesh/nSlices'][()]

        time_max = h5['params/Mesh/sliceMax'][()]
        time_min = h5['params/Mesh/sliceMin'][()]
        time_step = abs(time_max - time_min) / number_of_time_steps #s

        photon_energy = h5['params/photonEnergy'][()]
        photon_energy = photon_energy * e # Convert to J

        # matrix dataset to write with values 0...size*size-1
        print("Read geometry: ({0}x{1}x{2}).".format(
            number_of_x_meshpoints, number_of_y_meshpoints, number_of_time_steps))

        # open file for writing
        opmd_fname = input_file.replace(".h5", ".opmd.h5")

        series = opmd.Series(opmd_fname, opmd.Access_Type.create)

        # Add metadata
        series.set_author("SIMEX")

        ### FIXME: For some obscure reason, have to local import time module here, othewise
        ### FIXME: get runtime error about "time" not being assigned.
        import time
        localtime = time.localtime()
        date_string = "{}-{}-{} {}:{}:{} {}".format(localtime.tm_year,
                                                    localtime.tm_mon,
                                                    localtime.tm_mday,
                                                    localtime.tm_hour,
                                                    localtime.tm_min,
                                                    localtime.tm_sec,
                                                    localtime.tm_zone,
                                                    )
        # Base standard attributes.
        series.set_date(date_string)
        series.set_software("WavePropaGator (WPG)")
        series.set_software_version(h5["info/package_version"][()])

        # WAVEFRONT extension attributes.
        series.set_attribute("beamline", str(h5['params/beamline/printout'][()]))
        series.set_attribute("temporal domain", str(h5["params/wDomain"][()]))
        series.set_attribute("spatial domain", str(h5["params/wSpace"][()]))

        # Further comments.
        series.set_comment("This series is based on output from a WPG run converted to \
                           openPMD format using the utility %s, part of the SimEx library. " % (__file__))

        # Loop over time slices.
        print("Converting {0:s} to openpmd compliant {1:s}.".format(input_file, opmd_fname))

        # Add constant data here.
        series.set_attribute("radius of curvature in x", h5["params/Rx"][()])
        series.set_attribute("z coordinate", h5["params/Mesh/zCoord"][()])
        series.set_attribute("Rx_Unit_Dimension", [1,0,0,0,0,0,0])
        series.set_attribute("Rx_UnitSI", 1.0)
        series.set_attribute("radius of curvature in y", h5["params/Ry"][()])
        series.set_attribute("Ry_Unit_Dimension", [1,0,0,0,0,0,0])
        series.set_attribute("Ry_UnitSI", 1.0)
        series.set_attribute("Delta radius of curvature in x", h5["params/dRx"][()])
        series.set_attribute("DRx_Unit_Dimension", [1,0,0,0,0,0,0])
        series.set_attribute("DRx_UnitSI", 1.0)
        series.set_attribute("Delta radius of curvature in y", h5["params/dRy"][()])
        series.set_attribute("DRy_Unit_Dimension", [1,0,0,0,0,0,0])
        series.set_attribute("DRy_UnitSI", 1.0)
        series.set_attribute("photon energy", h5['params/photonEnergy'][()])
        series.set_attribute("photon energy unit dimension", [2,1,-2,0,0,0,0])
        series.set_attribute("photon energy UnitSI", e)

        for time_step in range(number_of_time_steps):

            E_hor_real = series.iterations[time_step+1].meshes["E_real"]["x"]
            E_hor_imag = series.iterations[time_step+1].meshes["E_imag"]["x"]
            E_ver_real = series.iterations[time_step+1].meshes["E_real"]["y"]
            E_ver_imag = series.iterations[time_step+1].meshes["E_imag"]["y"]

            ehor_re = h5['data/arrEhor'][:, :, time_step, 0].astype(numpy.float64)
            ehor_im = h5['data/arrEhor'][:, :, time_step, 1].astype(numpy.float64)
            ever_re = h5['data/arrEver'][:, :, time_step, 0].astype(numpy.float64)
            ever_im = h5['data/arrEver'][:, :, time_step, 1].astype(numpy.float64)

            ehor_re_dataset = opmd.Dataset(ehor_re.dtype, [number_of_x_meshpoints, number_of_y_meshpoints])
            ehor_im_dataset = opmd.Dataset(ehor_im.dtype, [number_of_x_meshpoints, number_of_y_meshpoints])
            ever_re_dataset = opmd.Dataset(ever_re.dtype, [number_of_x_meshpoints, number_of_y_meshpoints])
            ever_im_dataset = opmd.Dataset(ever_im.dtype, [number_of_x_meshpoints, number_of_y_meshpoints])

            E_hor_real.reset_dataset(ehor_re_dataset)
            E_hor_imag.reset_dataset(ehor_im_dataset)
            E_ver_real.reset_dataset(ever_re_dataset)
            E_ver_imag.reset_dataset(ever_im_dataset)

            E_hor_real[()] = ehor_re
            E_hor_imag[()] = ehor_im
            E_ver_real[()] = ehor_re
            E_ver_imag[()] = ehor_im

            # Write the common metadata for the group
            E_real = series.iterations[time_step+1].meshes["E_real"]
            E_imag = series.iterations[time_step+1].meshes["E_imag"]

            # Get grid geometry.
            E_real.set_geometry(opmd.Geometry.cartesian)
            E_imag.set_geometry(opmd.Geometry.cartesian)

            # Get grid properties.
            nx = h5['params/Mesh/nx'][()]
            xMax = h5['params/Mesh/xMax'][()]
            xMin = h5['params/Mesh/xMin'][()]
            dx = (xMax - xMin) / nx

            ny = h5['params/Mesh/ny'][()]
            yMax = h5['params/Mesh/yMax'][()]
            yMin = h5['params/Mesh/yMin'][()]
            dy = (yMax - yMin) / ny

            tMax = h5['params/Mesh/sliceMax'][()]
            tMin = h5['params/Mesh/sliceMin'][()]
            dt = (tMax - tMin) / number_of_time_steps

            E_real.set_grid_spacing(numpy.array([dx, dy], dtype=numpy.float64))
            E_imag.set_grid_spacing(numpy.array([dx, dy], dtype=numpy.float64))

            E_real.set_grid_global_offset(numpy.array([h5['params/xCentre'][()],
                                                       h5['params/yCentre'][()]],
                                                      dtype=numpy.float64
                                                      )
                                          )
            E_imag.set_grid_global_offset(numpy.array([h5['params/xCentre'][()],
                                                       h5['params/yCentre'][()]],
                                                      dtype=numpy.float64
                                                      )
                                          )

            E_real.set_grid_unit_SI(numpy.float64(1.0))
            E_imag.set_grid_unit_SI(numpy.float64(1.0))

            E_real.set_data_order(opmd.Data_Order.C)
            E_imag.set_data_order(opmd.Data_Order.C)

            E_real.set_axis_labels([b"x", b"y"])
            E_imag.set_axis_labels([b"x", b"y"])

            unit_dimension = {opmd.Unit_Dimension.L:  1.0,
                              opmd.Unit_Dimension.M:  1.0,
                              opmd.Unit_Dimension.T: -3.0,
                              opmd.Unit_Dimension.I: -1.0,
                              opmd.Unit_Dimension.theta: 0.0,
                              opmd.Unit_Dimension.N: 0.0,
                              opmd.Unit_Dimension.J: 0.0
                              }
            E_real.set_unit_dimension(unit_dimension)
            E_imag.set_unit_dimension(unit_dimension)

            # Write attribute that is specific to each dataset:
            # - Staggered position within a cell

            # - Conversion factor to SI units
            # WPG writes E fields in units of sqrt(W/mm^2), i.e. it writes E*sqrt(c * eps0 / 2).
            # Unit analysis:
            # [E] = V/m
            # [eps0] = As/Vm
            # [c] = m/s
            # ==> [E^2 * eps0 * c] = V**2/m**2 * As/Vm * m/s = V*A/m**2 = W/m**2 = [Intensity]
            # Converting to SI units by dividing by sqrt(c*eps0/2)*1e3, 1e3 for conversion from mm to m.
            c    = 2.998e8   # m/s
            eps0 = 8.854e-12 # As/Vm
            E_real.set_grid_unit_SI(numpy.float64(1.0/math.sqrt(0.5*c*eps0)/1.0e3))
            E_imag.set_grid_unit_SI(numpy.float64(1.0/math.sqrt(0.5*c*eps0)/1.0e3))

            # Add particles.

            series.flush()


    # The files in 'series' are still open until the object is destroyed, on
    # which it cleanly flushes and closes all open file handles.
    # One can delete the object explicitly (or let it run out of scope) to
    # trigger this.
    del series

    return

        # Open in and out files.
    if(False):
            # Get number of time slices in wpg output, assuming horizontal and vertical polarizations have same dimensions, which is always true for wpg output.
            data_shape = h5['data/arrEhor'][()].shape

            # Branch off if this is a non-time dependent calculation in frequency domain.
            if data_shape[2] == 1 and h5['params/wDomain'][()] == "frequency":
                # Time independent calculation in frequency domain.
                _convert_from_frequency_representation(h5, opmd_h5, data_shape)
                return

            number_of_x_meshpoints = data_shape[0]
            number_of_y_meshpoints = data_shape[1]
            number_of_time_steps = data_shape[2]

            time_max = h5['params/Mesh/sliceMax'][()] #s
            time_min = h5['params/Mesh/sliceMin'][()] #s
            time_step = abs(time_max - time_min) / number_of_time_steps #s

            photon_energy = h5['params/photonEnergy'][()] # eV
            photon_energy = photon_energy * e # Convert to J

            # Copy misc and params from original wpg output.
            opmd_h5.create_group('history/parent')
            try:
                h5.copy('/params',  opmd_h5['history/parent'])
                h5.copy('/misc',    opmd_h5['history/parent'])
                h5.copy('/history', opmd_h5['history/parent'])

            # Some keys may not exist, e.g. if the input file comes from a non-simex wpg run.
            except KeyError:
                pass
            except:
                raise

            sum_x = 0.0
            sum_y = 0.0
            for it in range(number_of_time_steps):
                # Write opmd
                # Setup the root attributes for iteration 0
                opmd_legacy.setup_root_attr( opmd_h5 )

                full_meshes_path = opmd_legacy.get_basePath(opmd_h5, it) + opmd_h5.attrs["meshesPath"]
                # Setup basepath.
                time=time_min+it*time_step
                opmd_legacy.setup_base_path( opmd_h5, iteration=it, time=time, time_step=time_step)
                opmd_h5.create_group(full_meshes_path)
                meshes = opmd_h5[full_meshes_path]

                # Path to the E field, within the h5 file.
                full_e_path_name = b"E"
                meshes.create_group(full_e_path_name)
                E = meshes[full_e_path_name]

                # Create the dataset (2d cartesian grid)
                E.create_dataset(b"x", (number_of_x_meshpoints, number_of_y_meshpoints), dtype=numpy.complex64, compression='gzip')
                E.create_dataset(b"y", (number_of_x_meshpoints, number_of_y_meshpoints), dtype=numpy.complex64, compression='gzip')

                # Write the common metadata for the group
                E.attrs["geometry"] = numpy.string_("cartesian")
                # Get grid geometry.
                nx = h5['params/Mesh/nx'][()]
                xMax = h5['params/Mesh/xMax'][()]
                xMin = h5['params/Mesh/xMin'][()]
                dx = (xMax - xMin) / nx
                ny = h5['params/Mesh/ny'][()]
                yMax = h5['params/Mesh/yMax'][()]
                yMin = h5['params/Mesh/yMin'][()]
                dy = (yMax - yMin) / ny
                E.attrs["gridSpacing"] = numpy.array( [dx,dy], dtype=numpy.float64)
                E.attrs["gridGlobalOffset"] = numpy.array([h5['params/xCentre'][()], h5['params/yCentre'][()]], dtype=numpy.float64)
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
                c    = 2.998e8   # m/s
                eps0 = 8.854e-12 # As/Vm
                E["x"].attrs["unitSI"] = numpy.float64(1.0  / math.sqrt(0.5 * c * eps0) / 1.0e3 )
                E["y"].attrs["unitSI"] = numpy.float64(1.0  / math.sqrt(0.5 * c * eps0) / 1.0e3 )

                # Copy the fields.
                Ex = h5['data/arrEhor'][:,:,it,0] + 1j * h5['data/arrEhor'][:,:,it,1]
                Ey = h5['data/arrEver'][:,:,it,0] + 1j * h5['data/arrEver'][:,:,it,1]
                E["x"][:,:] = Ex
                E["y"][:,:] = Ey

                # Get area element.
                dA = dx*dy

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
                Nph.attrs["gridGlobalOffset"] = numpy.array([h5['params/xCentre'][()], h5['params/yCentre'][()]], dtype=numpy.float64)
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
                number_of_photons_x = numpy.round(abs(Ex)**2 * dA * time_step *1.0e6 / photon_energy)
                number_of_photons_y = numpy.round(abs(Ey)**2 * dA * time_step *1.0e6 / photon_energy)
                sum_x += number_of_photons_x.sum(axis=-1).sum(axis=-1)
                sum_y += number_of_photons_y.sum(axis=-1).sum(axis=-1)
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
                phases.attrs["gridGlobalOffset"] = numpy.array([h5['params/xCentre'][()], h5['params/yCentre'][()]], dtype=numpy.float64)
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

def convertToOPMDLegacy(input_file):
    """ Take native wpg output and rewrite in openPMD conformant way.
    @param input_file: The hdf5 file to be converted.
    @type: string
    @example: input_file = "prop_out.h5"
    """

    # Check input file.
    if not h5py.is_hdf5(input_file):
        raise IOError("Not a valid hdf5 file: %s. " % (input_file))

    # Open in and out files.
    with h5py.File( input_file, 'r') as h5:
        with h5py.File(input_file.replace(".h5", ".opmd.h5"), 'w') as opmd_h5:

            # Get number of time slices in wpg output, assuming horizontal and vertical polarizations have same dimensions, which is always true for wpg output.
            data_shape = h5['data/arrEhor'][()].shape

            # Branch off if this is a non-time dependent calculation in frequency domain.
            if data_shape[2] == 1 and h5['params/wDomain'][()] == "frequency":
                # Time independent calculation in frequency domain.
                _convert_from_frequency_representation(h5, opmd_h5, data_shape)
                return

            number_of_x_meshpoints = data_shape[0]
            number_of_y_meshpoints = data_shape[1]
            number_of_time_steps = data_shape[2]


            time_max = h5['params/Mesh/sliceMax'][()] #s
            time_min = h5['params/Mesh/sliceMin'][()] #s
            time_step = abs(time_max - time_min) / number_of_time_steps #s

            photon_energy = h5['params/photonEnergy'][()] # eV
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
            for it in range(number_of_time_steps):
                # Write opmd
                # Setup the root attributes for iteration 0
                opmd_legacy.setup_root_attr( opmd_h5 )

                full_meshes_path = opmd_legacy.get_basePath(opmd_h5, it) + opmd_h5.attrs["meshesPath"]
                # Setup basepath.
                time=time_min+it*time_step
                opmd_legacy.setup_base_path( opmd_h5, iteration=it, time=time, time_step=time_step)
                opmd_h5.create_group(full_meshes_path)
                meshes = opmd_h5[full_meshes_path]

                # Path to the E field, within the h5 file.
                full_e_path_name = b"E"
                meshes.create_group(full_e_path_name)
                E = meshes[full_e_path_name]

                # Create the dataset (2d cartesian grid)
                E.create_dataset(b"x", (number_of_x_meshpoints, number_of_y_meshpoints), dtype=numpy.complex64, compression='gzip')
                E.create_dataset(b"y", (number_of_x_meshpoints, number_of_y_meshpoints), dtype=numpy.complex64, compression='gzip')

                # Write the common metadata for the group
                E.attrs["geometry"] = numpy.string_("cartesian")
                # Get grid geometry.
                nx = h5['params/Mesh/nx'][()]
                xMax = h5['params/Mesh/xMax'][()]
                xMin = h5['params/Mesh/xMin'][()]
                dx = (xMax - xMin) / nx
                ny = h5['params/Mesh/ny'][()]
                yMax = h5['params/Mesh/yMax'][()]
                yMin = h5['params/Mesh/yMin'][()]
                dy = (yMax - yMin) / ny
                E.attrs["gridSpacing"] = numpy.array( [dx,dy], dtype=numpy.float64)
                E.attrs["gridGlobalOffset"] = numpy.array([h5['params/xCentre'][()], h5['params/yCentre'][()]], dtype=numpy.float64)
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
                c    = 2.998e8   # m/s
                eps0 = 8.854e-12 # As/Vm
                E["x"].attrs["unitSI"] = numpy.float64(1.0  / math.sqrt(0.5 * c * eps0) / 1.0e3 )
                E["y"].attrs["unitSI"] = numpy.float64(1.0  / math.sqrt(0.5 * c * eps0) / 1.0e3 )

                # Copy the fields.
                Ex = h5['data/arrEhor'][:,:,it,0] + 1j * h5['data/arrEhor'][:,:,it,1]
                Ey = h5['data/arrEver'][:,:,it,0] + 1j * h5['data/arrEver'][:,:,it,1]
                E["x"][:,:] = Ex
                E["y"][:,:] = Ey

                # Get area element.
                dA = dx*dy

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
                Nph.attrs["gridGlobalOffset"] = numpy.array([h5['params/xCentre'][()], h5['params/yCentre'][()]], dtype=numpy.float64)
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
                number_of_photons_x = numpy.round(abs(Ex)**2 * dA * time_step *1.0e6 / photon_energy)
                number_of_photons_y = numpy.round(abs(Ey)**2 * dA * time_step *1.0e6 / photon_energy)
                sum_x += number_of_photons_x.sum(axis=-1).sum(axis=-1)
                sum_y += number_of_photons_y.sum(axis=-1).sum(axis=-1)
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
                phases.attrs["gridGlobalOffset"] = numpy.array([h5['params/xCentre'][()], h5['params/yCentre'][()]], dtype=numpy.float64)
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

def _convert_from_frequency_representation(h5, opmd_h5, data_shape, pulse_energy=1.0e-3, pulse_duration=23.0e-15):
    """ Converter for non-time dependent wavefronts in frequency representation.
    Requires knowledge of pulse energy and pulse duration to allow photon number calculation.
    """

    number_of_x_meshpoints = data_shape[0]
    number_of_y_meshpoints = data_shape[1]

    photon_energy = h5['params/photonEnergy'][()] # eV
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
    opmd_legacy.setup_root_attr( opmd_h5 )

    full_meshes_path = opmd_legacy.get_basePath(opmd_h5, it) + opmd_h5.attrs["meshesPath"]
    # Setup basepath.
    time = 0.0
    time_step = pulse_duration
    opmd_legacy.setup_base_path( opmd_h5, iteration=it, time=time, time_step=time_step)
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
    nx = h5['params/Mesh/nx'][()]
    xMax = h5['params/Mesh/xMax'][()]
    xMin = h5['params/Mesh/xMin'][()]
    dx = (xMax - xMin) / nx
    ny = h5['params/Mesh/ny'][()]
    yMax = h5['params/Mesh/yMax'][()]
    yMin = h5['params/Mesh/yMin'][()]
    dy = (yMax - yMin) / ny
    #E.attrs["gridSpacing"] = numpy.array( [dx,dy], dtype=numpy.float64)
    #E.attrs["gridGlobalOffset"] = numpy.array([h5['params/xCentre'][()], h5['params/yCentre'][()]], dtype=numpy.float64)
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
    Nph.attrs["gridGlobalOffset"] = numpy.array([h5['params/xCentre'][()], h5['params/yCentre'][()]], dtype=numpy.float64)
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
    phases.attrs["gridGlobalOffset"] = numpy.array([h5['params/xCentre'][()], h5['params/yCentre'][()]], dtype=numpy.float64)
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

if __name__ == "__main__":

    # Parse arguments.
    parser = ArgumentParser(description="Convert wpg output to openPMD conform hdf5.")
    parser.add_argument("input_file", metavar="input_file",
                      help="name of the file to convert.")
    args = parser.parse_args()

    # Call the converter routine.
    convertToOPMD(args.input_file)
