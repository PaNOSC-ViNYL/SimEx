#!/usr/bin/env python

##########################################################################
#                                                                        #
# Copyright (C) 2015-2018 Carsten Fortmann-Grote                         #
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


from SimEx.Analysis.DiffractionAnalysis import DiffractionAnalysis, plt

from argparse import ArgumentParser
import numpy

def main(args=None):

    # Setup the object.
    analyzer = DiffractionAnalysis(input_path=args.input_path,
                                   pattern_indices=eval(args.pattern_indices),
                                   poissonize=eval(args.poissonize),
                                   )


    # Plot if requested.
    if args.plot:
        analyzer.plotPattern(logscale=args.logscale,
                             operation=eval(args.operation),
                             )
    # Plot if requested.
    if args.radial:
        analyzer.plotRadialProjection(logscale=args.logscale,
                             operation=eval(args.operation),
                             )

    if args.statistics:
        analyzer.statistics()

    plt.show()


    # Animate if requested.
    if args.animation_filename:
        analyzer.animatePatterns(output_path=args.animation_filename)

        print("Animated gif saved to %s." % (analyzer._DiffractionAnalysis__animation_output_path))

if __name__ == '__main__':

    # Setup argument parser.
    parser = ArgumentParser()

    # Add arguments.
    parser.add_argument("input_path",
                        metavar="input_path",
                        help="Name (path) of input file (dir).",
                        default=None)

    parser.add_argument("-p",
                        "--pattern_indices",
                        dest="pattern_indices",
                        default="None",
                        help="")

    parser.add_argument("-P",
                        "--plot",
                        action="store_true",
                        dest="plot",
                        default=False,
                        help="Flag indicating whether to render a plot or not.")

    parser.add_argument("-R",
                        "--radial",
                        action="store_true",
                        dest="radial",
                        default=False,
                        help="Flag indicating whether to render a radial projection plot or not.")


    parser.add_argument("-l",
                        "--logscale",
                        action="store_true",
                        dest="logscale",
                        default=False,
                        help="Apply logscale to z-axis in color profiles.")

    parser.add_argument("-A",
                        "--animation",
                        dest="animation_filename",
                        default="",
                        help="Generate an animated gif out of the given patterns and save to given filename.")

    parser.add_argument("-o",
                        "--operation",
                        dest="operation",
                        default="numpy.sum",
                        help="Which operation to apply to a pattern sequence before plotting.")

    parser.add_argument("-z",
                        "--poissonize",
                        dest="poissonize",
                        default="True",
                        help="Whether to read the poissonized diffraction photon numbers (True) or diffraction intensities (False).")

    parser.add_argument("-S",
                        "--statistics",
                        dest="statistics",
                        default=False,
                        help="Whether to plot a histogram over number of photons per pattern and print some basic statistic information.")


    # Parse arguments.
    args = parser.parse_args()

    # Call main with arguments.
    main(args)
