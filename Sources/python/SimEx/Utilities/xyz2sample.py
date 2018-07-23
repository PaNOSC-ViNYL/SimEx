#! /usr/bin/env python
""" Read xyz structure file and convert to sample dir. """

from argparse import ArgumentParser
import numpy
import h5py
import csv
import os
import shutil
from periodictable import elements

csv.QUOTE_NONNUMERIC=True

def main(xyz):
    if not os.path.isfile(xyz):
        raise IOError("%s is not a file." % (xyz))

    sample_dir = 'sample'
    if not os.path.isdir(sample_dir):
        shutil.mkdir(sample_dir)
    coordinates_fname = os.path.join(sample_dir, "r.txt")
    atom_numbers_fname = os.path.join(sample_dir, "Z.txt")


    Z = []
    r = []
    with open(xyz, 'r', newline='' ) as xyz_handle:
        reader = csv.reader(xyz_handle, delimiter=' ')

        for line in reader:
            if len(line) < 4:
                print("INFO: "+"".join(line))
                continue
            symbol = line[0]
            element = getattr(elements, symbol)
            Z.append(str(element.number))

            coords = [float(x) for x in line[1:] if x != '']
            r.append(coords)

    # Convert to m.
    r = numpy.array(r)*1.0e-10

    with open(coordinates_fname, 'w') as r_handle:
        for coords in r:
            r_handle.write("%.8e\t%.8e\t%.8e\n" % (coords[0], coords[1], coords[2]))

    with open(atom_numbers_fname, 'w') as Z_handle:
        Z_handle.write(' '.join(Z))

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("xyz",
                        metavar="xyz",
                        help="Input structure file in xyz format.",
                        default=None)

    args = parser.parse_args()

    main(args.xyz)

