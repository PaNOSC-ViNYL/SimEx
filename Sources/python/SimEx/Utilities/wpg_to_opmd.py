import sys
import numpy
import math
import h5py
import os

from SimEx.Utilities import OpenPMDTools as opmd

def _convertToOPMD(h5_in):
    """ Take native wpg output and rewrite in openpmd conformant way. """

    # Load the generated h5 file.
    #wpg_outputs = [os.path.join( self.output_path, f) for f in os.listdir( self.output_path ) ]
    wpg_outputs = [h5_in]
    wpg_outputs = [f for f in wpg_outputs if f.split('.')[-1] == 'h5']
    print wpg_outputs

    for i,f in enumerate(wpg_outputs):
        h5 = h5py.File( f, 'r')
        opmd_h5 = h5py.File(f+'.opmd', 'w')

        # Get number of time slices in wpg output.
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
            #
            c    = 2.998e8   # m/s
            eps0 = 8.854e-12 # As/Vm
            E["x"].attrs["unitSI"] = numpy.float64(1.0  / math.sqrt(0.5 * c * eps0 * 1.0e3 ))
            E["y"].attrs["unitSI"] = numpy.float64(1.0  / math.sqrt(0.5 * c * eps0 * 1.0e3 ))
            ### CHECKME


            E["x"][:,:] =  h5['data/arrEhor'][:,:,it,0] + 1j * h5['data/arrEhor'][:,:,it,1]
            E["y"][:,:] =  h5['data/arrEver'][:,:,it,0] + 1j * h5['data/arrEver'][:,:,it,1]

        opmd_h5.close()
    h5.close()



if __name__ == "__main__":
    _convertToOPMD(sys.argv[1])


