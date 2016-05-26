#!/usr/bin/env python
#
# Copyright (c) 2015, Axel Huebl, Remi Lehe, Carsten Fortmann-Grote
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

from dateutil.tz import tzlocal
import collections
import datetime
import h5py
import numpy
import re
import string
import sys, getopt, os.path


def get_basePath(f, iteration):
    """
    Get the basePath for a certain iteration

    Parameter
    ---------
    f : an h5py.File object
        The file in which to write the data
    iteration : an iteration number

    Returns
    -------
    A string with a in-file path.
    """
    iteration_str = numpy.string_(str(iteration))
    return numpy.string_(f.attrs["basePath"]).replace(b"%T", iteration_str)

def setup_base_path(f, iteration, time, time_step):
    """
    Write the basePath group for `iteration`

    Parameters
    ----------
    f : an h5py.File object
        The file in which to write the data

    iteration : int
        The iteration number for this output
    """
    # Create the corresponding group
    base_path = get_basePath(f, iteration)
    f.create_group( base_path )
    bp = f[ base_path ]

    # Required attributes
    bp.attrs["time"] = time  # Value expressed in seconds
    bp.attrs["dt"] = time_step   # Value expressed in seconds
    bp.attrs["timeUnitSI"] = numpy.float64(1.0) # Conversion factor.

def setup_root_attr(f):
    """
    Write the root metadata for this file

    Parameter
    ---------
    f : an h5py.File object
        The file in which to write the data
    """

    # extensions list
    ext_list = [["ED-PIC", numpy.uint32(1)]]

    # Required attributes
    f.attrs["openPMD"] = numpy.string_("1.0.0")
    f.attrs["openPMDextension"] = ext_list[0][1] # ED-PIC extension is used
    f.attrs["basePath"] = numpy.string_("/data/%T/")
    f.attrs["meshesPath"] = numpy.string_("meshes/")
    f.attrs["particlesPath"] = numpy.string_("particles/")
    f.attrs["iterationEncoding"] = numpy.string_("groupBased")
    f.attrs["iterationFormat"] = numpy.string_("/data/%T/")

    # Recommended attributes
    f.attrs["author"] = numpy.string_("Carsten Fortmann-Grote <carsten.grote@xfel.eu>")
    f.attrs["software"] = numpy.string_("openPMD conform wpg output.")
    f.attrs["softwareVersion"] = numpy.string_("1.0.0")
    f.attrs["date"] = numpy.string_( datetime.datetime.now(tzlocal()).strftime('%Y-%m-%d %H:%M:%S %z'))


def write_b_2d_cartesian(meshes, data_ez):
    """
    Write the metadata and the data associated with the vector field B,
    using a 2d Cartesian representation.
    In this special case, the components of the vector field B.x and B.y
    shall be constant.

    Parameters
    ----------
    meshes : an h5py.Group object
             Group of the meshes in basePath + meshesPath
    data_ez : 2darray of reals
        The values of the component B.z on the 2d x-y grid
        (The first axis corresponds to x, and the second axis corresponds to y)
    """
    # Path to the E field, within the h5py file
    full_b_path_name = b"B"
    meshes.create_group(full_b_path_name)
    B = meshes[full_b_path_name]

    # Create the dataset (2d cartesian grid)
    B.create_group(b"x")
    B.create_group(b"y")
    B.create_dataset(b"z", data_ez.shape, dtype=numpy.float32)

    # Write the common metadata for the group
    B.attrs["geometry"] = numpy.string_("cartesian")
    B.attrs["gridSpacing"] = numpy.array([1.0, 1.0], dtype=numpy.float32)   # dx, dy
    B.attrs["gridGlobalOffset"] = numpy.array([0.0, 0.0], dtype=numpy.float32)
    B.attrs["gridUnitSI"] = numpy.float64(1.0)
    B.attrs["dataOrder"] = numpy.string_("C")
    B.attrs["axisLabels"] = numpy.array([b"x",b"y"])
    B.attrs["unitDimension"] = \
       numpy.array([0.0, 1.0, -2.0, -1.0, 0.0, 0.0, 0.0 ], dtype=numpy.float64)
       #          L    M     T     I  theta  N    J
       # B is in Tesla : kg / (A * s^2) -> M * T^-2 * I^-1

    # Add specific information for PIC simulations at the group level
    add_EDPIC_attr_meshes(B)

    # Add time information
    B.attrs["timeOffset"] = 0.25 # Time offset with basePath's time

    # Write attribute that is specific to each dataset:
    # - Staggered position within a cell
    B["x"].attrs["position"] = numpy.array([0.0, 0.0], dtype=numpy.float32)
    B["y"].attrs["position"] = numpy.array([0.0, 0.0], dtype=numpy.float32)
    B["z"].attrs["position"] = numpy.array([0.5, 0.5], dtype=numpy.float32)
    # - Conversion factor to SI units
    B["x"].attrs["unitSI"] = numpy.float64(3.3)
    B["y"].attrs["unitSI"] = numpy.float64(3.3)
    B["z"].attrs["unitSI"] = numpy.float64(3.3)

    # Fill the array with the field data
    #   the constant record components B.x and B.y have the same shape
    #   (== same mesh discretization) as the non-constant record
    #   component B.z
    B["x"].attrs["value"] = numpy.float(0.0)
    B["x"].attrs["shape"] = numpy.array(data_ez.shape, dtype=numpy.uint64)
    B["y"].attrs["value"] = numpy.float(0.0)
    B["y"].attrs["shape"] = numpy.array(data_ez.shape, dtype=numpy.uint64)
    B["z"][:,:] =  data_ez[:,:]

def write_e_2d_cartesian(meshes, data_ex, data_ey, data_ez ):
    """
    Write the metadata and the data associated with the vector field E,
    using a 2d Cartesian representation

    Parameters
    ----------
    meshes : an h5py.Group object
             Group of the meshes in basePath + meshesPath

    data_ex, data_ey, data_ez : 2darray of reals
        The values of the components E.x, E.y, E.z on the 2d x-y grid
        (The first axis corresponds to x, and the second axis corresponds to y)
    """
    # Path to the E field, within the h5py file
    full_e_path_name = b"E"
    meshes.create_group(full_e_path_name)
    E = meshes[full_e_path_name]

    # Create the dataset (2d cartesian grid)
    E.create_dataset(b"x", data_ex.shape, dtype=numpy.float32)
    E.create_dataset(b"y", data_ey.shape, dtype=numpy.float32)
    E.create_dataset(b"z", data_ez.shape, dtype=numpy.float32)

    # Write the common metadata for the group
    E.attrs["geometry"] = numpy.string_("cartesian")
    E.attrs["gridSpacing"] = numpy.array([1.0, 1.0], dtype=numpy.float32)  # dx, dy
    E.attrs["gridGlobalOffset"] = numpy.array([0.0, 0.0], dtype=numpy.float32)
    E.attrs["gridUnitSI"] = numpy.float64(1.0)
    E.attrs["dataOrder"] = numpy.string_("C")
    E.attrs["axisLabels"] = numpy.array([b"x",b"y"])
    E.attrs["unitDimension"] = \
       numpy.array([1.0, 1.0, -3.0, -1.0, 0.0, 0.0, 0.0 ], dtype=numpy.float64)
       #            L    M     T     I  theta  N    J
       # E is in volts per meters: V / m = kg * m / (A * s^3)
       # -> L * M * T^-3 * I^-1

    # Add specific information for PIC simulations at the group level
    add_EDPIC_attr_meshes(E)

    # Add time information
    E.attrs["timeOffset"] = 0.  # Time offset with respect to basePath's time

    # Write attribute that is specific to each dataset:
    # - Staggered position within a cell
    E["x"].attrs["position"] = numpy.array([0.0, 0.5], dtype=numpy.float32)
    E["y"].attrs["position"] = numpy.array([0.5, 0.0], dtype=numpy.float32)
    E["z"].attrs["position"] = numpy.array([0.0, 0.0], dtype=numpy.float32)
    # - Conversion factor to SI units
    E["x"].attrs["unitSI"] = numpy.float64(1.0e9)
    E["y"].attrs["unitSI"] = numpy.float64(1.0e9)
    E["z"].attrs["unitSI"] = numpy.float64(1.0e9)

    # Fill the array with the field data
    E["x"][:,:] =  data_ex[:,:]
    E["y"][:,:] =  data_ey[:,:]
    E["z"][:,:] =  data_ez[:,:]


def add_EDPIC_attr_meshes(field):
    """
    Write the metadata which is specific to PIC algorithm
    for a given field

    Parameters
    ----------
    field : an h5py.Group or h5py.Dataset object
            The record of the field (Group for vector mesh
            and Dataset for scalar meshes)

    """
    field.attrs["fieldSmoothing"] = numpy.string_("none")
    # field.attrs["fieldSmoothingParameters"] = \
    #     numpy.string_("period=10;numPasses=4;compensator=true")


def add_EDPIC_attr_particles(particle):
    """
    Write the metadata which is specific to the PIC algorithm
    for a given species.

    Parameters
    ----------
    particle : an h5py.Group object
               The group of the particle that gets additional attributes.

    """
    particle.attrs["particleShape"] = 3.0
    particle.attrs["currentDeposition"] = numpy.string_("Esirkepov")
    # particle.attrs["currentDepositionParameters"] = numpy.string_("")
    particle.attrs["particlePush"] = numpy.string_("Boris")
    particle.attrs["particleInterpolation"] = numpy.string_("uniform")
    particle.attrs["particleSmoothing"] = numpy.string_("none")
    # particle.attrs["particleSmoothingParameters"] = \
    #     numpy.string_("period=1;numPasses=2;compensator=false")


def write_meshes(f, iteration):
    full_meshes_path = get_basePath(f, iteration) + f.attrs["meshesPath"]
    f.create_group(full_meshes_path)
    meshes = f[full_meshes_path]

    # Extension: Additional attributes for ED-PIC
    meshes.attrs["fieldSolver"] = numpy.string_("Yee")
    meshes.attrs["fieldBoundary"] = numpy.array(
        [b"periodic", b"periodic", b"open", b"open"])
    meshes.attrs["particleBoundary"] = numpy.array(
        [b"periodic", b"periodic", b"absorbing", b"absorbing"])
    meshes.attrs["currentSmoothing"] = numpy.string_("Binomial")
    meshes.attrs["currentSmoothingParameters"] = \
         numpy.string_("period=1;numPasses=2;compensator=false")
    meshes.attrs["chargeCorrection"] = numpy.string_("none")

    # (Here the data is randomly generated, but in an actual simulation,
    # this would be replaced by the simulation data.)

    # - Write rho
    # Mode 0 : real values, mode 1 : complex values
    data_rho0 = numpy.random.rand(32,64)
    data_rho1 = numpy.random.rand(32,64) + 1.j*numpy.random.rand(32,64)
    write_rho_cylindrical(meshes, data_rho0, data_rho1)

    # - Write E
    data_ex = numpy.random.rand(32,64)
    data_ey = numpy.random.rand(32,64)
    data_ez = numpy.random.rand(32,64)
    write_e_2d_cartesian( meshes, data_ex, data_ey, data_ez )

    # - Write B
    data_bz = numpy.random.rand(32,64)
    write_b_2d_cartesian( meshes, data_bz )

def write_particles(f, iteration):
    fullParticlesPath = get_basePath(f, iteration) + f.attrs["particlesPath"]
    f.create_group(fullParticlesPath + b"electrons")
    electrons = f[fullParticlesPath + b"electrons"]

    globalNumParticles = 128 # example number of all particles

    electrons.attrs["comment"] = numpy.string_("My first electron species")

    # Extension: ED-PIC Attributes
    #   required
    add_EDPIC_attr_particles(electrons)
    #   recommended
    # currently none

    # constant scalar particle records (that could also be variable records)
    electrons.create_group(b"charge")
    charge = electrons["charge"]
    charge.attrs["value"] = -1.0
    charge.attrs["shape"] = numpy.array([globalNumParticles], dtype=numpy.uint64)
    # macroWeighted: False(0) the charge value is given for an underlying,
    #                real particle
    # weightingPower == 1: the charge of the macro particle scales linearly
    #                      with the number of underlying real particles
    #                      it represents
    charge.attrs["macroWeighted"] = numpy.uint32(0)
    charge.attrs["weightingPower"] = numpy.float64(1.0)
    # attributes from the base standard
    charge.attrs["timeOffset"] = 0.
    charge.attrs["unitSI"] = numpy.float64(1.60217657e-19)
    charge.attrs["unitDimension"] = \
       numpy.array([0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0 ], dtype=numpy.float64)
       #          L    M    T    I  theta  N    J
       # C = A * s

    electrons.create_group(b"mass")
    mass = electrons["mass"]
    mass.attrs["value"] = 1.0
    mass.attrs["shape"] = numpy.array([globalNumParticles], dtype=numpy.uint64)
    # macroWeighted: False(0) the mass value is given for an underlying,
    #                real particle
    # weightingPower == 1: the mass of the macro particle scales linearly
    #                      with the number of underlying real particles
    #                      it represents
    mass.attrs["macroWeighted"] = numpy.uint32(0)
    mass.attrs["weightingPower"] = numpy.float64(1.0)
    # attributes from the base standard
    mass.attrs["timeOffset"] = 0.
    mass.attrs["unitSI"] = numpy.float64(9.10938291e-31)
    mass.attrs["unitDimension"] = \
       numpy.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], dtype=numpy.float64)
       #          L    M    T    I  theta  N    J

    # scalar particle records (non-const/individual per particle)
    electrons.create_dataset(b"weighting", (globalNumParticles,),
                             dtype=numpy.float32)
    weighting = electrons["weighting"]
    # macroWeighted: True(1) by definition
    # weightingPower == 1: since this is the identity of weighting,
    #                      it scales linearly with itself
    weighting.attrs["macroWeighted"] = numpy.uint32(1)
    weighting.attrs["weightingPower"] = numpy.float64(1.0)
    # attributes from the base standard
    weighting.attrs["timeOffset"] = 0.
    weighting.attrs["unitSI"] = numpy.float64(1.0)
    weighting.attrs["unitDimension"] = \
       numpy.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], dtype=numpy.float64)
    # plain floating point number

    # Position of each particle
    electrons.create_group(b"position")
    position = electrons["position"]
    position.create_dataset("x", (globalNumParticles,), dtype=numpy.float32)
    position.create_dataset("y", (globalNumParticles,), dtype=numpy.float32)
    position.create_dataset("z", (globalNumParticles,), dtype=numpy.float32)
    # Conversion factor to SI units
    position["x"].attrs["unitSI"] = numpy.float64(1.e-9)
    position["y"].attrs["unitSI"] = numpy.float64(1.e-9)
    position["z"].attrs["unitSI"] = numpy.float64(1.e-9)
    # macroWeighted: can be 1 or 0 in this case, since it's the same for macro
    #                particles and representing underlying particles
    # weightingPower == 0: the position does not scale with the weighting
    position.attrs["macroWeighted"] = numpy.uint32(1)
    position.attrs["weightingPower"] = numpy.float64(0.0)
    # attributes from the base standard
    position.attrs["timeOffset"] = 0.
    position.attrs["unitDimension"] = \
       numpy.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], dtype=numpy.float64)
       #          L    M     T    I  theta  N    J
       # Dimension of Length per component

    # Position offset of each particle
    electrons.create_group(b"positionOffset")
    offset = electrons["positionOffset"]
    # Constant components here (typical of a moving window along z)
    offset.create_group(b"x")
    offset["x"].attrs["value"] = numpy.float32(0.)
    offset["x"].attrs["shape"] = numpy.array([globalNumParticles], dtype=numpy.uint64)
    offset.create_group(b"y")
    offset["y"].attrs["value"] = numpy.float32(0.)
    offset["y"].attrs["shape"] = numpy.array([globalNumParticles], dtype=numpy.uint64)
    offset.create_group(b"z")
    offset["z"].attrs["value"] = numpy.float32(100.)
    offset["z"].attrs["shape"] = numpy.array([globalNumParticles], dtype=numpy.uint64)
    # Conversion factor to SI units
    offset["x"].attrs["unitSI"] = numpy.float64(1.e-9)
    offset["y"].attrs["unitSI"] = numpy.float64(1.e-9)
    offset["z"].attrs["unitSI"] = numpy.float64(1.e-9)
    # macroWeighted: can be 1 or 0 in this case, since it's the same for macro
    #                particles and representing underlying particles
    # weightingPower == 0: the positionOffset does not scale with the weighting
    offset.attrs["macroWeighted"] = numpy.uint32(1)
    offset.attrs["weightingPower"] = numpy.float64(0.0)
    # attributes from the base standard
    offset.attrs["timeOffset"] = 0.
    offset.attrs["unitDimension"] = \
       numpy.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], dtype=numpy.float64)
       #          L    M     T    I  theta  N    J
       # Dimension of Length per component

    # Momentum of each particle
    electrons.create_group(b"momentum")
    momentum = electrons["momentum"]
    momentum.create_dataset("x", (globalNumParticles,), dtype=numpy.float32)
    momentum.create_dataset("y", (globalNumParticles,), dtype=numpy.float32)
    momentum.create_dataset("z", (globalNumParticles,), dtype=numpy.float32)
    # Conversion factor to SI units
    momentum["x"].attrs["unitSI"] = numpy.float64(1.60217657e-19)
    momentum["y"].attrs["unitSI"] = numpy.float64(1.60217657e-19)
    momentum["z"].attrs["unitSI"] = numpy.float64(1.60217657e-19)

    # macroWeighted: True(1) in this example we store the momentum
    #                of the macro particle
    # weightingPower == 1: each underlying particle contributes linearly
    #                      to the total momentum
    momentum.attrs["macroWeighted"] = numpy.uint32(1)
    momentum.attrs["weightingPower"] = numpy.float64(1.0)
    # attributes from the base standard
    momentum.attrs["timeOffset"] = 0.25
    momentum.attrs["unitDimension"] = \
       numpy.array([1.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0 ], dtype=numpy.float64)
       #          L    M     T    I  theta  N    J
       # Dimension of Length * Mass / Time

    # Sub-Group `particlePatches`
    #   recommended
    mpi_size = 4  # "emulate" example MPI run with 4 ranks
    # 2 + 2 * Dimensionality of position record
    grid_layout = numpy.array( [512, 128, 1] ) # global grid in cells
    electrons.create_group(b"particlePatches")
    particlePatches = electrons["particlePatches"]

    particlePatches.create_dataset("numParticles", (mpi_size,), dtype=numpy.uint64)
    particlePatches.create_dataset("numParticlesOffset", (mpi_size,), dtype=numpy.uint64)
    particlePatches.create_dataset("offset/x", (mpi_size,), dtype=numpy.float32)
    particlePatches.create_group(b"offset/y")
    particlePatches.create_group(b"offset/z")
    particlePatches["offset/x"].attrs["unitSI"] = offset["x"].attrs["unitSI"]
    particlePatches["offset/y"].attrs["unitSI"] = offset["y"].attrs["unitSI"]
    particlePatches["offset/z"].attrs["unitSI"] = offset["z"].attrs["unitSI"]
    particlePatches.create_dataset("extent/x", (mpi_size,), dtype=numpy.float32)
    particlePatches.create_group(b"extent/y")
    particlePatches.create_group(b"extent/z")
    particlePatches["extent/x"].attrs["unitSI"] = offset["x"].attrs["unitSI"]
    particlePatches["extent/y"].attrs["unitSI"] = offset["y"].attrs["unitSI"]
    particlePatches["extent/z"].attrs["unitSI"] = offset["z"].attrs["unitSI"]

    # domain decomposition shall be 1D along x (but positions are still 3D)
    # we can therefor make the other components constant
    particlePatches["offset/y"].attrs["value"] = numpy.float32(0.0)   # full size
    particlePatches["offset/z"].attrs["value"] = numpy.float32(0.0)   # full size
    particlePatches["offset/y"].attrs["shape"] = numpy.array([mpi_size], dtype=numpy.uint64)
    particlePatches["offset/z"].attrs["shape"] = numpy.array([mpi_size], dtype=numpy.uint64)

    particlePatches["extent/y"].attrs["value"] = numpy.float32(128.0) # full size
    particlePatches["extent/z"].attrs["value"] = numpy.float32(1.0)   # full size
    particlePatches["extent/y"].attrs["shape"] = numpy.array([mpi_size], dtype=numpy.uint64)
    particlePatches["extent/z"].attrs["shape"] = numpy.array([mpi_size], dtype=numpy.uint64)

    for rank in numpy.arange(mpi_size):
        # each MPI rank would write its part independently
        # numParticles: number of particles in this patch
        particlePatches['numParticles'][rank] = globalNumParticles / mpi_size
        # numParticlesOffset: offset within the one-dimensional records where
        #                     the first particle in this patch is stored
        particlePatches['numParticlesOffset'][rank] = rank*globalNumParticles / mpi_size
        # offset and extent in the grid
        # example: 1D domain decompositon of 3D simulation along the first axis
        # 1st dimension spatial offset
        particlePatches['offset/x'][rank] = rank * grid_layout[0] / mpi_size
        particlePatches['extent/x'][rank] = grid_layout[0] / mpi_size



openPMD = "1.0.0"

ext_list = [["ED-PIC", numpy.uint32(1)]]

def help():
    """ Print usage information for this file """
    print('This is the openPMD file check for HDF5 files.\n')
    print('Check for format version: %s\n' % openPMD)
    print('Usage:\n  checkOpenPMD_h5py.py -i <fileName> [-v] [--EDPIC]')
    sys.exit()


def parse_cmd(argv):
    """ Parse the command line arguments """
    file_name = ''
    verbose = False
    extension_pic = False
    try:
        opts, args = getopt.getopt(argv,"hvi:e",["file=","EDPIC"])
    except getopt.GetoptError:
        print('checkOpenPMD_h5py.py -i <fileName>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help()
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("--EDPIC"):
            extension_pic = True
        elif opt in ("-i", "--file"):
            file_name = arg
    if not os.path.isfile(file_name):
        help()
    return(file_name, verbose, extension_pic)


def open_file(file_name):
    if h5py.is_hdf5(file_name):
        f = h5py.File(file_name, "r")
        return(f)
    else:
        help()

def get_attr(f, name):
    """
    Try to access the path `name` in the file `f`
    Return the corresponding attribute if it is present
    """
    if name in list(f.attrs.keys()):
        return(True, f.attrs[name])
    else:
        return(False, None)

def test_record(g, r):
    """
    Checks if a record is valid

    Parameters
    ----------
    g : h5py.Group
        The group the record resides in

    r : string
        The name of the record.

    Returns
    -------
    An array with 2 elements :
    - The first element is 1 if an error occured, and 0 otherwise
    - The second element is 0 if a warning arised, and 0 otherwise
    """
    regEx = re.compile("^\w+$") # Python3 only: re.ASCII
    if regEx.match(r):
        # test component names
        result_array = numpy.array([0,0])
        if not is_scalar_record(g[r]) :
            for component_name in g[r]:
                if not regEx.match(component_name):
                    print("Error: Component %s of record %s is NOT" \
                    " named properly (a-Z0-9_)!" %(component_name, g[r].name) )
                    result_array += numpy.array([1,0])
    else:
        print("Error: Record %s is NOT named properly (a-Z0-9_)!" \
              %(r.name) )
        result_array = numpy.array([1,0])

    return(result_array)

def test_key(f, v, request, name):
    """
    Checks whether a key is present. A key can either be
    a h5py.Group or a h5py.Dataset.
    Returns an error if the key if absent and requested
    Returns a warning if the key if absent and recommended

    Parameters
    ----------
    f : an h5py.File or h5py.Group object
        The object in which to find the key

    v : bool
        Verbose option

    request : string
        Either "required", "recommended" or "optional"

    name : string
        The name of the key within this File, Group or DataSet

    Returns
    -------
    An array with 2 elements :
    - The first element is 1 if an error occured, and 0 otherwise
    - The second element is 0 if a warning arised, and 0 otherwise
    """
    valid = (name in list(f.keys()))
    if valid:
        if v:
            print("Key %s (%s) exists in `%s`!" %(name, request, str(f.name) ) )
        result_array = numpy.array([0,0])
    else:
        if request == "required":
            print("Error: Key %s (%s) does NOT exist in `%s`!" \
            %(name, request, str(f.name)) )
            result_array = numpy.array([1, 0])
        elif request == "recommended":
            print("Warning: Key %s (%s) does NOT exist in `%s`!" \
            %(name, request, str(f.name)) )
            result_array = numpy.array([0, 1])
        elif request == "optional":
            if v:
                print("Info: Key %s (%s) does NOT exist in `%s`!"  \
            %(name, request, str(f.name)) )
            result_array = numpy.array([0, 0])
        else :
            raise ValueError("Unrecognized string for `request` : %s" %request)

    return(result_array)

def test_attr(f, v, request, name, is_type=None, type_format=None):
    """
    Checks whether an attribute is present.
    Returns an error if the attribute if absent and requested
    Returns a warning if the attribute if absent and recommanded

    Parameters
    ----------
    f : an h5py.File, h5py.Group or h5py.DataSet object
        The object in which to find the key

    v : bool
        Verbose option

    request : string
        Either "required", "recommended" or "optional

    name : string
        The name of the attribute within this File, Group or DataSet

    is_type : (numpy or python) data type
        The type of the attribute. Default is "arbitrary" for None.
        Can be a list of data types where at least one data type must match
        but this list can not be combined with type_format.

    type_format: (numpy or python) data type
        Used with is_type to specify numpy ndarray dtypes or a
        base numpy.string_ format regex. Can be a list of data types
        for ndarrays where at least one data type must match.

    Returns
    -------
    An array with 2 elements :
    - The first element is 1 if an error occured, and 0 otherwise
    - The second element is 0 if a warning arised, and 0 otherwise
    """
    valid, value = get_attr(f, name)
    if valid:
        if v:
            print("Attribute %s (%s) exists in `%s`! Type = %s, Value = %s" \
            %(name, request, str(f.name), type(value), str(value)) )

        # test type
        if is_type is not None:
            if not type_format is None and not is_type is numpy.string_ and \
               not isinstance(type_format, collections.Iterable):
                type_format = [type_format]
                type_format_names = map(lambda x: x.__name__, type_format)
            if not is_type is None and not isinstance(is_type, collections.Iterable):
                is_type = [is_type]
            is_type_names = map(lambda x: x.__name__, is_type)
            # add for each type in is_type -> wrong, need to add this at the comparison level!
            if type(value) in is_type:
                # numpy.string_ format or general ndarray dtype text
                if type(value) is numpy.string_ and type_format is not None:
                    regEx = re.compile(type_format) # Python3 only: re.ASCII
                    if regEx.match(value.decode()) :
                        result_array = numpy.array([0,0])
                    else:
                        print("Error: Attribute %s in `%s` does not satisfy " \
                              "format ('%s' should be in format '%s')!" \
                              %(name, str(f.name), value.decode(), type_format ) )
                        result_array = numpy.array([1,0])
                # ndarray dtypes
                elif type(value) is numpy.ndarray:
                    if value.dtype.type in type_format:
                        result_array = numpy.array([0,0])
                    elif type_format is None:
                        result_array = numpy.array([0,0])
                    else:
                        print("Error: Attribute %s in `%s` is not of type " \
                              "ndarray of '%s' (is ndarray of '%s')!" \
                              %(name, str(f.name), type_format_names, \
                              value.dtype.type.__name__) )
                        result_array = numpy.array([1,0])
                else:
                    result_array = numpy.array([0,0])
            else:
                print(
                 "Error: Attribute %s in `%s` is not of type '%s' (is '%s')!" \
                 %(name, str(f.name), str(is_type_names), \
                  type(value).__name__) )
                result_array = numpy.array([1,0])
        else: # is_type is None (== arbitrary)
            result_array = numpy.array([0,0])
    else:
        if request == "required":
            print("Error: Attribute %s (%s) does NOT exist in `%s`!" \
            %(name, request, str(f.name)) )
            result_array = numpy.array([1, 0])
        elif request == "recommended":
            print("Warning: Attribute %s (%s) does NOT exist in `%s`!" \
            %(name, request, str(f.name)) )
            result_array = numpy.array([0, 1])
        elif request == "optional":
            if v:
                print("Info: Attribute %s (%s) does NOT exist in `%s`!"  \
            %(name, request, str(f.name)) )
            result_array = numpy.array([0, 0])
        else :
            raise ValueError("Unrecognized string for `request` : %s" %request)

    return(result_array)

def is_scalar_record(r):
    """
    Checks if a record is a scalar record or not.

    Parameters
    ----------
    r : an h5py.Group or h5py.Dataset object
        the record that shall be tested

    Returns
    -------
    bool : true if the record is a scalar record, false if the record
           is either a vector or an other type of tensor record
    """
    if type(r) is h5py.Group :
        # now it could be either a vector/tensor record
        # or a scalar record with a constant component

        valid, value = get_attr(r, "value")
        # constant components require a "value" and a "shape" attribute
        if valid :
            return True
        else:
            return False
    else :
        return True

def test_component(c, v) :
    """
    Checks if a record component defines all required attributes.

    Parameters
    ----------
    c : an h5py.Group or h5py.Dataset object
        the record component that shall be tested

    v : bool
        Verbose option

    Returns
    -------
    An array with 2 elements :
    - The first element is the number of errors encountered
    - The second element is the number of warnings encountered
    """
    # Initialize the result array
    # First element : number of errors
    # Second element : number of warnings
    result_array = numpy.array([0,0])

    if type(c) is h5py.Group :
        # since this check tests components, this must be a constant
        # component: requires "value" and "shape" attributes
        result_array += test_attr(c, v, "required", "value") # type can be arbitrary
        result_array += test_attr(c, v, "required", "shape", numpy.ndarray, numpy.uint64)

    # default attributes for all components
    result_array += test_attr(c, v, "required", "unitSI", numpy.float64)

    return(result_array)


def check_root_attr(f, v, pic):
    """
    Scan the root of the file and make sure that all the attributes are present

    Parameters
    ----------
    f : an h5py.File object
        The HDF5 file in which to find the attribute

    v : bool
        Verbose option

    pic : bool
        Whether to check for the ED-PIC extension attributes

    Returns
    -------
    An array with 2 elements :
    - The first element is the number of errors encountered
    - The second element is the number of warnings encountered
    """
    # Initialize the result array
    # First element : number of errors
    # Second element : number of warnings
    result_array = numpy.array([0,0])

    # STANDARD.md
    #   required
    result_array += test_attr(f, v, "required", "openPMD", numpy.string_, "^[0-9]+\.[0-9]+\.[0-9]+$")
    result_array += test_attr(f, v, "required", "openPMDextension", numpy.uint32)
    result_array += test_attr(f, v, "required", "basePath", numpy.string_, "^\/data\/\%T\/$")
    result_array += test_attr(f, v, "required", "meshesPath", numpy.string_)
    result_array += test_attr(f, v, "required", "particlesPath", numpy.string_)
    result_array += test_attr(f, v, "required", "iterationEncoding", numpy.string_, "^groupBased|fileBased$")
    result_array += test_attr(f, v, "required", "iterationFormat", numpy.string_)

    # groupBased iteration encoding needs to match basePath
    if result_array[0] == 0 :
        if f.attrs["iterationEncoding"].decode() == "groupBased" :
            if f.attrs["iterationFormat"].decode() != f.attrs["basePath"].decode() :
                print("Error: for groupBased iterationEncoding the basePath "
                      "and iterationFormat must match!")
                result_array += numpy.array([1,0])

    #   recommended
    result_array += test_attr(f, v, "recommended", "author", numpy.string_)
    result_array += test_attr(f, v, "recommended", "software", numpy.string_)
    result_array += test_attr(f, v, "recommended",
                              "softwareVersion", numpy.string_)
    result_array += test_attr(f, v, "recommended", "date", numpy.string_,
      "^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [\+|-][0-9]{4}$")

    #   optional
    result_array += test_attr(f, v, "optional", "comment", numpy.string_)

    # Extension: ED-PIC
    if pic:
        valid, extensionIDs = get_attr(f, "openPMDextension")
        if valid:
            if (ext_list[0][1] & extensionIDs) != extensionIDs:
                print("Error: ID=%s for extension `%s` not found in " \
                      "`openPMDextension` (is %s)!" \
                     %(ext_list[0][1], ext_list[0][0], extensionIDs) )
                result_array += numpy.array([1,0])

    return(result_array)


def check_iterations(f, v, pic) :
    """
    Scan all the iterations present in the file, checking both
    the meshes and the particles

    Parameters
    ----------
    f : an h5py.File object
        The HDF5 file in which to find the attribute

    v : bool
        Verbose option

    pic : bool
        Whether to check for the ED-PIC extension attributes

    Returns
    -------
    An array with 2 elements :
    - The first element is the number of errors encountered
    - The second element is the number of warnings encountered
    """

    # Find all the iterations
    format_error = False
    try :
        list_iterations = list(f['/data/'].keys())
    except KeyError :
        format_error = True
    else :
        # Check that these iterations are indeed encoded as integers
        for iteration in list_iterations :
            for character in iteration : # go through the string
                if not (character in string.digits) :
                    format_error = True
    # Detect any error and interrupt execution if one is found
    if format_error == True :
        print("Error: it seems that the path of the data within the HDF5 file "
              "is not of the form '/data/%T/', where %T corresponds to an "
              "actual integer.")
        return(numpy.array([1, 0]))
    else :
        print("Found %d iteration(s)" % len(list_iterations) )

    # Initialize the result array
    # First element : number of errors
    # Second element : number of warnings
    result_array = numpy.array([ 0, 0])

    # Loop over the iterations and check the meshes and the particles
    for iteration in list_iterations :
        result_array += check_base_path(f, iteration, v, pic)
        # Go deeper only if there is no error at this point
        if result_array[0] == 0 :
            result_array += check_meshes(f, iteration, v, pic)
            result_array += check_particles(f, iteration, v, pic)

    return(result_array)

def check_base_path(f, iteration, v, pic):
    """
    Scan the base_path that corresponds to this iteration

    Parameters
    ----------
    f : an h5py.File object
        The HDF5 file in which to find the attribute

    iteration : string representing an integer
        The iteration at which to scan the meshes

    v : bool
        Verbose option

    pic : bool
        Whether to check for the ED-PIC extension attributes

    Returns
    -------
    An array with 2 elements :
    - The first element is the number of errors encountered
    - The second element is the number of warnings encountered
    """
    # Initialize the result array
    # First element : number of errors
    # Second element : number of warnings
    result_array = numpy.array([ 0, 0])

    # Find the path to the data
    base_path = ("/data/%s/" % iteration).encode('ascii')
    bp = f[base_path]

    # Check for the attributes of the STANDARD.md
    result_array += test_attr(bp, v, "required", "time", [numpy.float32, numpy.float64])
    result_array += test_attr(bp, v, "required", "dt", [numpy.float32, numpy.float64])
    result_array += test_attr(bp, v, "required", "timeUnitSI", numpy.float64)

    return(result_array)

def check_meshes(f, iteration, v, pic):
    """
    Scan all the meshes corresponding to one iteration

    Parameters
    ----------
    f : an h5py.File object
        The HDF5 file in which to find the attribute

    iteration : string representing an integer
        The iteration at which to scan the meshes

    v : bool
        Verbose option

    pic : bool
        Whether to check for the ED-PIC extension attributes

    Returns
    -------
    An array with 2 elements :
    - The first element is the number of errors encountered
    - The second element is the number of warnings encountered
    """
    # Initialize the result array
    # First element : number of errors
    # Second element : number of warnings
    result_array = numpy.array([ 0, 0])

    # Find the path to the data
    base_path = "/data/%s/" % iteration
    valid, meshes_path = get_attr(f, "meshesPath")
    if not valid :
        print("Error: `meshesPath` is missing or malformed in '/'")
        return( numpy.array([1, 0]) )
    meshes_path = meshes_path.decode()

    if os.path.join( base_path, meshes_path) != ( base_path + meshes_path ):
        print("Error: `basePath`+`meshesPath` seems to be malformed "
            "(is `basePath` absolute and ends on a `/` ?)")
        return( numpy.array([1, 0]) )
    else:
        full_meshes_path = (base_path + meshes_path).encode('ascii')
        # Find all the meshes
        try:
            list_meshes = list(f[full_meshes_path].keys())
        except KeyError:
            list_meshes = []
    #print( "Iteration %s : found %d meshes" %( iteration, len(list_meshes) ) )

    # Check for the attributes of the STANDARD.md
    for field_name in list_meshes :
        field = f[full_meshes_path + field_name.encode('ascii')]

        result_array += test_record(f[full_meshes_path], field_name)

        # General attributes of the record
        result_array += test_attr(field, v, "required",
                                  "unitDimension", numpy.ndarray, numpy.float64)
        result_array += test_attr(field, v, "required",
                                  "timeOffset", [numpy.float32, numpy.float64])
        result_array += test_attr(field, v, "required",
                                  "gridSpacing", numpy.ndarray, [numpy.float32, numpy.float64])
        result_array += test_attr(field, v, "required",
                                  "gridGlobalOffset", numpy.ndarray, [numpy.float32, numpy.float64])
        result_array += test_attr(field, v, "required",
                                  "gridUnitSI", numpy.float64)
        result_array += test_attr(field, v, "required",
                                  "dataOrder", numpy.string_)
        result_array += test_attr(field, v, "required",
                                  "axisLabels", numpy.ndarray, numpy.string_)
        # Specific check for geometry
        geometry_test = test_attr(field, v, "required", "geometry", numpy.string_)
        result_array += geometry_test
        # geometryParameters is required when using thetaMode
        if geometry_test[0] == 0 and field.attrs["geometry"] == b"thetaMode" :
            result_array += test_attr(field, v, "required",
                                            "geometryParameters", numpy.string_)
        # otherwise it is optional
        else :
            result_array += test_attr(field, v, "optional",
                                            "geometryParameters", numpy.string_)

        # Attributes of the record's components
        if is_scalar_record(field) :   # If the record is a scalar field
            result_array += test_component(field, v)
            result_array += test_attr(field, v,
                                "required", "position", numpy.ndarray, [numpy.float32, numpy.float64])
        else:                          # If the record is a vector field
            # Loop over the components
            for component_name in list(field.keys()) :
                component = field[component_name]
                result_array += test_component(component, v)
                result_array += test_attr(component, v,
                                "required", "position", numpy.ndarray, [numpy.float32, numpy.float64])

    # Check for the attributes of the PIC extension,
    # if asked to do so by the user
    if pic:

        # Check the attributes associated with the field solver
        result_array += test_attr(f[full_meshes_path], v, "required",
                                  "fieldSolver", numpy.string_)
        valid, field_solver = get_attr(f[full_meshes_path], "fieldSolver")
        if (valid == True) and (field_solver in ["other", "GPSTD"]) :
            result_array += test_attr(f[full_meshes_path], v, "required",
                                      "fieldSolverParameters", numpy.string_)

        # Check for the attributes associated with the field boundaries
        result_array += test_attr(f[full_meshes_path], v, "required",
                                "fieldBoundary", numpy.ndarray, numpy.string_)
        valid, field_boundary = get_attr(f[full_meshes_path], "fieldBoundary")
        if (valid == True) and (numpy.any(field_boundary == b"other")) :
            result_array += test_attr(f[full_meshes_path], v, "required",
                        "fieldBoundaryParameters", numpy.ndarray, numpy.string_)

        # Check for the attributes associated with the field boundaries
        result_array += test_attr(f[full_meshes_path], v, "required",
                                "particleBoundary", numpy.ndarray, numpy.string_)
        valid, particle_boundary = get_attr(f[full_meshes_path], "particleBoundary")
        if (valid == True) and (numpy.any(particle_boundary == b"other")) :
            result_array += test_attr(f[full_meshes_path], v, "required",
                    "particleBoundaryParameters", numpy.ndarray, numpy.string_)

        # Check the attributes associated with the current smoothing
        result_array += test_attr(f[full_meshes_path], v, "required",
                                  "currentSmoothing", numpy.string_)
        valid, current_smoothing = get_attr(f[full_meshes_path], "currentSmoothing")
        if (valid == True) and (current_smoothing != b"none") :
            result_array += test_attr(f[full_meshes_path], v, "required",
                        "currentSmoothingParameters", numpy.string_)

        # Check the attributes associated with the charge conservation
        result_array += test_attr(f[full_meshes_path], v, "required",
                                  "chargeCorrection", numpy.string_)
        valid, charge_correction = get_attr(f[full_meshes_path], "chargeCorrection")
        if valid == True and charge_correction != b"none":
            result_array += test_attr(f[full_meshes_path], v, "required",
                        "chargeCorrectionParameters", numpy.string_)

        # Check for the attributes of each record
        for field_name in list_meshes :
            field = f[full_meshes_path + field_name.encode('ascii')]
            result_array + test_attr(field, v, "required",
                                     "fieldSmoothing", numpy.string_)
            valid, field_smoothing = get_attr(field, "fieldSmoothing")
            if (valid == True) and (field_smoothing != b"none") :
                result_array += test_attr(field,v, "required",
                                    "fieldSmoothingParameters", numpy.string_)
    return(result_array)


def check_particles(f, iteration, v, pic) :
    """
    Scan all the particle data corresponding to one iteration

    Parameters
    ----------
    f : an h5py.File object
        The HDF5 file in which to find the attribute

    iteration : string representing an integer
        The iteration at which to scan the particle data

    v : bool
        Verbose option

    pic : bool
        Whether to check for the ED-PIC extension attributes

    Returns
    -------
    An array with 2 elements :
    - The first element is the number of errors encountered
    - The second element is the number of warnings encountered
    """
    # Initialize the result array
    # First element : number of errors
    # Second element : number of warnings
    result_array = numpy.array([ 0, 0])

    # Find the path to the data
    base_path = ("/data/%s/" % iteration).encode('ascii')
    valid, particles_path = get_attr(f, "particlesPath")
    if os.path.join( base_path, particles_path) !=  \
        ( base_path + particles_path ) :
        print("Error: `basePath`+`meshesPath` seems to be malformed "
            "(is `basePath` absolute and ends on a `/` ?)")
        return( numpy.array([1, 0]) )
    else:
        full_particle_path = base_path + particles_path
        # Find all the particle species
        try:
            list_species = list(f[full_particle_path].keys())
        except KeyError:
            list_species = []
    #print( "Iteration %s : found %d particle species" %( iteration, len(list_species) ) )

    # Go through all the particle species
    for species_name in list_species :
        species = f[full_particle_path + species_name.encode('ascii')]

        # Check all records for this species
        for species_record_name in species :
            result_array += test_record(species, species_record_name)

        # Check the position record of the particles
        result_array += test_key(species, v, "required", "position")

        # Check the position offset record of the particles
        result_array += test_key(species, v, "required", "positionOffset")
        if result_array[0] == 0 :
            position_dimensions = len(species["position"].keys())
            positionOffset_dimensions = len(species["positionOffset"].keys())
            if position_dimensions != positionOffset_dimensions :
                print("Error: `position` (ndim=%s) and `positionOffset` " \
                      "(ndim=%s) do not have the same dimensions in " \
                      "species `%s`!" \
                      %(str(position_dimensions), \
                        str(positionOffset_dimensions),
                        species.name) )
                result_array += numpy.array([ 1, 0])

        # Check the particlePatches record of the particles
        patch_test = test_key(species, v, "recommended", "particlePatches")
        result_array += patch_test
        if result_array[0] == 0 and patch_test[1] == 0 :
            result_array += test_key(species["particlePatches"], v, "required",
                                     "numParticles")
            result_array += test_key(species["particlePatches"], v, "required",
                                     "numParticlesOffset")
            result_array += test_key(species["particlePatches"], v, "required",
                                     "offset")
            result_array += test_key(species["particlePatches"], v, "required",
                                     "extent")
            if result_array[0] == 0 :
                offset = species["particlePatches"]["offset"]
                extent = species["particlePatches"]["extent"]
                # Attributes of the components
                for component_name in list(species["position"].keys()) :
                    result_array += test_key( offset, v, "required",
                                              component_name)
                    result_array += test_key( extent, v, "required",
                                              component_name)
                    if result_array[0] == 0 :
                        dset_offset = offset[component_name]
                        result_array += test_component(dset_offset, v)
                        dset_extent = extent[component_name]
                        result_array += test_component(dset_extent, v)

        # Check the records required by the PIC extension
        if pic :
            result_array += test_key(species, v, "required", "momentum")
            result_array += test_key(species, v, "required", "charge")
            result_array += test_key(species, v, "required", "mass")
            result_array += test_key(species, v, "required", "weighting")
            result_array += test_key(species, v, "optional", "boundElectrons")
            result_array += test_key(species, v, "optional", "protonNumber")
            result_array += test_key(species, v, "optional", "neutronNumber")

        # Check the attributes associated with the PIC extension
        if pic :
            result_array += test_attr(species, v, "required",
                                      "particleShape", [numpy.float32, numpy.float64])
            result_array += test_attr(species, v, "required",
                                      "currentDeposition", numpy.string_)
            result_array += test_attr(species, v, "required",
                                      "particlePush", numpy.string_)
            result_array += test_attr(species, v, "required",
                                      "particleInterpolation", numpy.string_)

            # Check for the attributes associated with the particle smoothing
            result_array += test_attr(species, v, "required",
                                      "particleSmoothing", numpy.string_)
            valid, particle_smoothing = get_attr(species, "particleSmoothing")
            if valid == True and particle_smoothing != b"none":
                result_array += test_attr(species, v, "required",
                                "particleSmoothingParameters", numpy.string_)

        # Check attributes of each record of the particle
        for record in list(species.keys()) :
            # all records (but particlePatches) require units
            if record != "particlePatches":
                result_array += test_attr(species[record], v,
                        "required", "unitDimension", numpy.ndarray, numpy.float64)
                time_type = f[base_path].attrs["time"].dtype.type
                result_array += test_attr(species[record], v, "required",
                                          "timeOffset", time_type)
                if pic :
                    result_array += test_attr(species[record], v, "required",
                                              "weightingPower", numpy.float64)
                    result_array += test_attr(species[record], v, "required",
                                              "macroWeighted", numpy.uint32)
                # Attributes of the components
                if is_scalar_record( species[record] ) : # Scalar record
                    dset = species[record]
                    result_array += test_component(dset, v)
                else : # Vector record
                    # Loop over the components
                    for component_name in list(species[record].keys()):
                        dset = species[ os.path.join(record, component_name) ]
                        result_array += test_component(dset, v)

    return(result_array)

