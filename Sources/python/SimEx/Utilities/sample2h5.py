#! /usr/bin/env python
""" Write sample coordinates and atom numbers to an hdf5 file. """

from argparse import ArgumentParser
import numpy
import h5py
import csv
import os

csv.QUOTE_NONNUMERIC=True
sample_h5_fname = 'sample.h5'

def main(sample_dir):
    if not os.path.isdir(sample_dir):
        raise IOError("%s is not a directory." % (sample_dir))

    coordinates_fname = os.path.join(sample_dir, "r.txt")
    atom_numbers_fname = os.path.join(sample_dir, "Z.txt")

    if not os.path.exists(coordinates_fname):
        raise IOError("%s does not exist." % (coordinates_fname))
    if not os.path.exists(atom_numbers_fname):
        raise IOError("%s does not exist." % (atom_numbers_fname))

    # Read coordinates in Angstrom.
    coordinates = numpy.loadtxt(coordinates_fname)

    with open(atom_numbers_fname, 'r', newline='' ) as Z_handle:
        reader = csv.reader(Z_handle, delimiter=' ')
        z = reader.__next__()
        Z = [int(zz) for zz in z if zz != '']


    with h5py.File(sample_h5_fname,'w') as h5:
        h5.create_dataset("Z", data=Z)
        h5.create_dataset("r", data=coordinates)

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("input_dir",
                        metavar="input_dir",
                        help="Path of the sample directory containing Z.txt (atomic numbers on one line) and r.txt (Atoms' Cartesian coordinates in units of metre. One triple (x y z) per line.",
                        default=None)

    args = parser.parse_args()

    main(args.input_dir)

