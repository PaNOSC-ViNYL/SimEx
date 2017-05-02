""" Module for AbstractAnalysis """
##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 Carsten Fortmann-Grote                         #
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

from abc import ABCMeta, abstractmethod
import exceptions
import os

# The one and only pyplot import.
import matplotlib as mpl
mpl.use("Qt4Agg")
from matplotlib import pyplot as plt

from SimEx.Utilities.EntityChecks import checkAndSetInstance

import dill
import sys

class AbstractAnalysis(object):
    """
    Abstract class for all data analysis classes.
    """
    __metaclass__ = ABCMeta

    @classmethod
    def runFromCLI(cls):
        """
        Method to start calculator computations from command line.

        :return: exit with status code

        """
        if len(sys.argv) == 2:
            fname = sys.argv[1]
            calculator=cls.dumpLoader(fname)
            status = calculator._run()
            sys.exit(status)

    @classmethod
    def dumpLoader(cls,fname):
        """
        Creates calculator object from a dump file

        :param fname: path to the dump file.

        :return: Created calculator object.

        :raises RuntimeError: if cannot create object.

        """

        try:
            calculator = dill.load(open(fname))
        except:
            raise exceptions.IOError("Cannot read  from file "+fname)
        if not issubclass(type(calculator),AbstractBaseCalculator):
            raise TypeError( "The argument to the script should be a path to a file "
                             "with object of subclass of AbstractAnalysis")
        return calculator

    @abstractmethod
    def __init__(self, input_path=None):
        """

        :param input_path: Path to hdf5 file holding the data to analyze. Single file or directory.
        :type input_path: str

        """

        if input_path is None:
            raise ValueError("The parameter 'input_path' cannot be None.")

        self.__input_path = checkAndSetInstance(str, input_path, None)

# TODO : think - should we make it abstract and remove default call of backengine?
#    @abstractmethod
    def _run(self):
        """
        Method to do computations. By default starts backengine.
        :return: status code.
        """
        result=self.backengine()

        if result is None:
            result=0

        return result
        # Can be reimplemented by specialized calculator.

    def dumpToFile(self, fname):
        """
        dump class instance to file.

        :param fname: Path to file to dump.

        """

        try:
            dill.dump(self, open(fname, "w"))
        except:
            raise exceptions.IOError("Cannot dump to file "+fname)

    #######################################################################
    # Queries and setters
    #######################################################################
    # control_parameters

    # input
    @property
    def input_path(self):
        """ Query for the input file path(s). """
        return self.__input_path
    @input_path.setter
    def input_path(self, value):
        """ Set the io path(s) to a value. """
        self.__input_path = checkAndSetInstance( (str, list), value, None   )
    @input_path.deleter
    def input_path(self):
        """ Delete the input_path path(s). """
        del self.__input_path

def checkAndSetBaseCalculator(var=None, default=None):
    """
    Check if passed object is an AbstractAnalysis instance. If non is given, set to given default.

    :param var: The object to check.

    :param default: The default to use.

    :return: The checked object.

    :raises RuntimeError: if no valid Analysis object was given.

    """

    return checkAndSetInstance(AbstractAnalysis, var, default)
