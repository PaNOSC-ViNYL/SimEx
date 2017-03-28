#!/usr/bin/env python2.7
##########################################################################
#                                                                        #
# Copyright (C) 2016-2017 Carsten Fortmann-Grote                         #
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
from SimEx.Analysis.XFELPhotonAnalysis import XFELPhotonAnalysis, plt

def main(args):

    # Setup the object.
    analyzer = XFELPhotonAnalysis(input_path=args.input_file)

    if args._do_intensity_distribution:
        analyzer.plotIntensityMap(logscale=args.logscale)
    if args._do_qspace_intensity:
        analyzer.plotIntensityMap(logscale=args.logscale, qspace=True)
    if args._do_total_power:
        analyzer.plotTotalPower()
    if args._do_on_axis_power:
        analyzer.plotOnAxisPowerDensity()
    if args._do_spectrum:
        analyzer.plotTotalPower(spectrum=True)

    plt.show()


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
                        default=False,
                        help="Plot the intensity distribution in x-y.")

    parser.add_argument("-R",
                        "--reciprocal",
                        action="store_true",
                        dest="_do_qspace_intensity",
                        default=False,
                        help="Plot the intensity distribution in qx-qy.")

    #parser.add_argument("-P",
                        #"--phase",
                        #action="store_true",
                        #dest="_do_phase_distribution",
                        #default=False,
                        #help="Plot the phase distribution in x-y.")

    parser.add_argument("-S",
                        "--spectrum",
                        action="store_true",
                        dest="_do_spectrum",
                        default=False,
                        help="Plot the power spectra.")

    parser.add_argument("-l",
                        "--logscale",
                        action="store_true",
                        dest="logscale",
                        default=False,
                        help="Plot color profiles on logscale.")

    parser.add_argument("-T",
                        "--total-power",
                        action="store_true",
                        dest="_do_total_power",
                        default=False,
                        help="Plot total power as function of time.")

    parser.add_argument("-X",
                        "--on-axis-power",
                        action="store_true",
                        dest="_do_on_axis_power",
                        default=False,
                        help="Plot total power as function of time.")




    args = parser.parse_args()

    main(args)

