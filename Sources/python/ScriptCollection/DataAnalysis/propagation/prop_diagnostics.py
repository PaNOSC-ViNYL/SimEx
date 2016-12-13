#!/usr/bin/env python2.7
##########################################################################
#                                                                        #
# Copyright (C) 2016 Carsten Fortmann-Grote                              #
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

""" :module: Holding functions for quick diagnostics of wavefront propagation results. """
from argparse import ArgumentParser

import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib import pyplot

import wpg
from wpg.wpg_uti_wf import plot_t_wf,look_at_q_space


### TODO
# Plot phase distribution
# Plot average and rms intensity distribution over given patterns.


def main(args):

    # Get wavefront file name.
    wavefront_file = args.input_file

    wavefront = wpg.Wavefront()
    wavefront.load_hdf5(wavefront_file)

    if args._do_intensity_distribution:
        plot_t_wf(wavefront)

    if args._do_qspace_intensity:
        look_at_q_space(wavefront)


    pyplot.show()


if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("input_file",
                        metavar="input_file",
                        help="Name (path) of input file.",
                        default=None)

    parser.add_argument("-I",
                        "--intensity",
                        action="store_true",
                        dest="_do_intensity_distribution",
                        default=True,
                        help="Plot the intensity distribution in x-y.")

    parser.add_argument("-R",
                        "--reciprocal",
                        action="store_true",
                        dest="_do_qspace_intensity",
                        default=True,
                        help="Plot the intensity distribution in qx-qy.")


    args = parser.parse_args()

    main(args)

