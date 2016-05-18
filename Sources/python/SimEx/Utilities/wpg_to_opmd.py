from argparse import ArgumentParser
import h5py
import math
import numpy
import os
import sys

from SimEx.Utilities import OpenPMDTools as opmd

def _convertToOPMD(input_file):
    """ Take native wpg output and rewrite in openPMD conformant way.
    @param input_file: The hdf5 file to be converted.
    @type: string
    @example: input_file = "prop_out.h5"
    """

    # Check input file.
    if not h5py.is_hdf5(input_file):
        raise IOError("Not a valid hdf5 file: %s. " % (input_file))

    # Open in and out files.
    h5 = h5py.File( input_file, 'r')
    opmd_h5 = h5py.File(input_file.replace(".h5", ".opmd.h5"), 'w')

    # Get number of time slices in wpg output, assuming horizontal and vertical polarizations have same dimensions, which is always true for wpg output.
    data_shape = h5['data/arrEhor'].value.shape
    number_of_x_meshpoints = data_shape[0]
    number_of_y_meshpoints = data_shape[1]
    number_of_time_steps = data_shape[2]

    for it in range(number_of_time_steps):
        # Write opmd
        # Setup the root attributes for iteration 0
        opmd.setup_root_attr( opmd_h5 )

        full_meshes_path = opmd.get_basePath(opmd_h5, it) + opmd_h5.attrs["meshesPath"]
        # Setup basepath.
        opmd.setup_base_path( opmd_h5, iteration=it)
        opmd_h5.create_group(full_meshes_path)
        meshes = opmd_h5[full_meshes_path]
        # Path to the E field, within the h5py file
        full_e_path_name = b"E"
        meshes.create_group(full_e_path_name)
        E = meshes[full_e_path_name]


        # Create the dataset (2d cartesian grid)
        E.create_dataset(b"x", (number_of_x_meshpoints, number_of_y_meshpoints), dtype=numpy.complex64)
        E.create_dataset(b"y", (number_of_x_meshpoints, number_of_y_meshpoints), dtype=numpy.complex64)

        # Write the common metadata for the group
        E.attrs["geometry"] = numpy.string_("cartesian")
        E.attrs["gridSpacing"] = numpy.array( [h5['params/dRx'].value, h5['params/dRy'].value], dtype=numpy.float64)
        E.attrs["gridGlobalOffset"] = numpy.array([h5['params/xCentre'].value, h5['params/yCentre'].value], dtype=numpy.float64)
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
        E["x"][:,:] =  h5['data/arrEhor'][:,:,it,0] + 1j * h5['data/arrEhor'][:,:,it,1]
        E["y"][:,:] =  h5['data/arrEver'][:,:,it,0] + 1j * h5['data/arrEver'][:,:,it,1]

    opmd_h5.close()
    h5.close()



if __name__ == "__main__":

    # Parse arguments.
    parser = ArgumentParser(description="Convert wpg output to openPMD conform hdf5.")
    parser.add_argument("input_file", metavar="input_file",
                      help="name of the file to convert.")
    args = parser.parse_args()

    # Call the converter routine.
    _convertToOPMD(args.input_file)

