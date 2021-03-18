#!/usr/bin/env python
# -*- coding: utf-8 -*-


import h5py
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('linkpath', metavar='LINKPATH')
args = parser.parse_args()

# Path where individual h5 files are located.
path_to_files = args.linkpath

# Setup new file.
with h5py.File(args.linkpath + ".h5", "w") as h5_outfile:

    # Files to read from.
    individual_files = [
        os.path.join(path_to_files, f) for f in os.listdir(path_to_files)
    ]
    individual_files.sort()

    # Keep track of global parameters being linked.
    global_parameters = False
    # Loop over all individual files and link in the top level groups.
    for ind_file in individual_files:
        # Open file.
        with h5py.File(ind_file, 'r') as h5_infile:

            # Links must be relative.
            relative_link_target = os.path.relpath(
                path=ind_file,
                start=os.path.dirname(os.path.dirname(ind_file)))

            # Link global parameters.
            if not global_parameters and len(h5_infile["params"]) > 0:
                global_parameters = True

                h5_outfile["params"] = h5py.ExternalLink(
                    relative_link_target, "params")
                h5_outfile["info"] = h5py.ExternalLink(relative_link_target,
                                                       "info")
                h5_outfile["misc"] = h5py.ExternalLink(relative_link_target,
                                                       "misc")
                h5_outfile["version"] = h5py.ExternalLink(
                    relative_link_target, "version")

            for key in h5_infile['data']:

                # Link in the data.
                ds_path = "data/%s" % (key)
                h5_outfile[ds_path] = h5py.ExternalLink(
                    relative_link_target, ds_path)
