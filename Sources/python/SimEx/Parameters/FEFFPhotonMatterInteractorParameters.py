""" :module: Holds the FEFFPhotonMatterInteractorParameters class.
##########################################################################
#                                                                        #
# Copyright (C) 2015 - 2018 Carsten Fortmann-Grote                        #
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
"""

import sys


from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.Utilities import ALL_ELEMENTS

class FEFFPhotonMatterInteractorParameters(AbstractCalculatorParameters):
    """
    Interface class for photon-matter interaction calculations using the FEFF code.
    """

    def __init__(self,
            atoms=None,
            potentials=None,
            edge=None,
            amplitude_reduction_factor=None,
            effective_path_distance=None,
            ):
        """
        Constructor for the FEFF photon interactor.

        :param atoms: The atomic structure (Atom coordinates ([x,y,z] in Angstrom), element symbol, and potential index). If no potential index is given, all atoms of the same species will be assigned the default potential. The scattering atom must have the potential index 0.
        :type atoms: list || tuple
        :example atoms: ([[0.0, 0.0, 0.0], 'Cu', 0], [[0.0, 1.0, 1.2], 'O', 1], ...)

        :param potentials: The potentials to use.
        :type potentials: list

        :param edge: The edge to calculate (K, L1, L2, M1, M2, M3, ...). Default 'K'.
        :type edge: str

        :param amplitude_reduction_factor: The amplitude reduction factor. Default 1.0
        :type amplitude_reduction_factor: float

        :param effective_path_distance: The maximum effective (half-path) distance in Angstrom.  Translates to rpath parameter in feff.inp. Default 2.2 times nearest neighbor distance.
        :type effective_path_distance: float
        """

        # Initialize base class.
        super(FEFFPhotonMatterInteractorParameters, self).__init__()

        # Set the parameters. Type checking performed here.
        self.atoms = atoms
        self.potentials = potentials
        self.edge = edge
        self.amplitude_reduction_factor = amplitude_reduction_factor
        self.effective_path_distance = effective_path_distance

        # Finalize. This will check parameter consistency.
        self.finalize()

    # Queries and setters.
    @property
    def atoms(self):
        """ Query method for atoms """
        return self.__atoms
    @atoms.setter
    def atoms(self, value):
        """ Set self.__atoms to value. """
        # If all passed, set the member attribute.
        self.__atoms = _checkAndSetAtoms(value)
        self.__finalized = False

    @property
    def potentials(self):
        """ Query method for potentials """
        return self.__potentials
    @potentials.setter
    def potentials(self, value):
        """ Set self.__potentials to value. """
        self.__potentials = value
        self.__finalized = False

    @property
    def edge(self):
        """ Query method for edge """
        return self.__edge
    @edge.setter
    def edge(self, value):
        """ Set self.__edge to value. """
        if not isinstance(value, str):
            raise TypeError("Parameter 'edge' must be a string")
        if value in ['K', 'L1', 'L2', 'M1', 'M2', 'M3']:
            self.__edge = value
        else:
            raise ValueError("Parameter 'edge' must be one of 'K', 'L1', 'L2', 'M1', 'M2', or 'M3'.")
        self.__finalized = False

    @property
    def amplitude_reduction_factor(self):
        """ Query method for amplitude_reduction_factor """
        return self.__amplitude_reduction_factor
    @amplitude_reduction_factor.setter
    def amplitude_reduction_factor(self, value):
        """ Set self.__amplitude_reduction_factor to value. """

        try: # Cast int to float.
            value = float(value)
        except:
            raise TypeError("Parameter 'amplitude_reduction_factor' must be a float.")

        if ( value >=0.0 or value <= 1.0 ):
            self.__amplitude_reduction_factor = value
        else:
            raise TypeError("Parameter 'amplitude_reduction_factor' must obey 0.0 <= x <= 1.0.")

        self.__finalized = False

    @property
    def effective_path_distance(self):
        """ Query method for effective_path_distance """
        return self.__effective_path_distance
    @effective_path_distance.setter
    def effective_path_distance(self, value):
        """ Set self.__effective_path_distance to value. """
        try: # Cast int to float.
            value = float(value)
        except:
            raise TypeError("Parameter 'effective_path_distance' must be a float.")

        if ( value >=0.0):
            self.__effective_path_distance = value
        else:
            raise TypeError("Parameter 'effective_path_distance' must obey 0.0 <= x.")

        self.__finalized = False

    @property
    def finalized(self):
        """ Query the finalization status. """
        return self.__finalized

    def finalize(self):
        """ Finalize the parameters. Check if all parameters are internally consistent."""

        # Only if not finalized.
        if self.__finalized:
            return

        else:
            # Finalize potentials.
            self.__potential_list = []

            # Get atoms.
            atoms = self.atoms
            # Get potential indices.
            potential_indices = [atom[2] for atom in atoms]
            symbols = [atom[1] for atom in atoms]

            # Sort and set.
            unique_indices = set(potential_indices)

            # Loop over all unique potential indices and aggregate the potential information.
            for ui in unique_indices:
                index = potential_indices.index(ui)
                symbol = atoms[index][1] # Returns first found.
                atomic_number = ALL_ELEMENTS.index(symbol)+1
                self.__potential_list.append([ui, atomic_number, symbol])

            self.__finalized = True

    def _serialize(self, stream=sys.stdout ):
        """ """
        """ Private method to serialize the parameters, i.e. write the feff.inp file. """

        # Only possible if finalized.
        if not self.__finalized:
            raise RuntimeError("Only finalized parameters can be serialized. Call the finalize() method before serialize().")

        else:
            stream.write("EDGE    %s\n" % (self.edge) )
            stream.write("S02     %f\n" % (self.amplitude_reduction_factor) )
            stream.write("CONTROL 1 1 1 1 1 1\n")
            stream.write("PRINT   0 0 0 0 0 0\n")
            stream.write("RPATH   %f\n" % (self.effective_path_distance) )
            stream.write("EXAFS\n")
            stream.write("\n")
            stream.write("POTENTIALS\n")
            for potential in self.__potential_list:
                stream.write("%d      %d      %s\n" % (potential[0], potential[1], potential[2]) )
            stream.write("\n")
            stream.write("ATOMS\n")
            for atom in self.atoms:
                stream.write("%6.5f      %6.5f      %6.5f      %d\n" % (atom[0][0], atom[0][1], atom[0][2], atom[2]) )

            stream.write("END")
#
##########################################
# Utility functions

    def _setDefaults(self):
        """ """
        """ Set the inherited parameters defaults that depend on the special calculator. """
        self._AbstractCalculatorParameters__cpus_per_task_default = 1

def _checkAndSetAtoms(value):
    """ """
    """ Private function to check if input is a valid atoms list.

    :parameter value: The value to check.
    :return: The atom list if checks pass.
    :raises: Exception if input not a correct atom list.
    """
    # Check if None
    if value is None:
        raise TypeError( "Parameter 'atoms' must be an iterable (list or tuple) of length > 0")

    # Check if iterable.
    if not hasattr( value, '__iter__') or len(value) < 1:
        raise TypeError( "Parameter 'atoms' must be an iterable (list or tuple) of length > 0")

    # Check all elements.
    for atom in value:
        # Check that each atom is a list of tuple.
        if not ( isinstance(atom, list) or isinstance(atom, tuple)):
            raise TypeError( "Each element in 'atoms' must be a list or tuple.")

        # Check that first element is the coordinate vector.
        if not hasattr( atom[0], '__iter__' ) or not len(atom[0]) == 3:
            raise TypeError( "The first element in each element in 'atoms' must be an iterable of length 3 (atomic coordinates in Angstrom).")

        # Check that second element is the element symbol.
        if not isinstance( atom[1], str ):
            raise TypeError( "The second element in each element in 'atoms' must be a string (element symbol).")
        if not atom[1] in ALL_ELEMENTS:
            raise ValueError( "The second element in each element in 'atoms' must be a valid element symbol.")
        # Check that third element is the potential index.
        if not isinstance( atom[2], int ):
            raise TypeError( "The third element in each element in 'atoms' must be an integer (potential index).")

    ### Check potential indices.
    # Extract potential indices.
    potential_indices = [atom[2] for atom in value]
    # Sort.
    potential_indices.sort()

    # Check that there's only one index 0.
    if potential_indices[0] != 0 or 0 in potential_indices[1:]:
        raise ValueError( "There must be one and only one potential index 0.")

    # Get unique indices.
    unique_indices = set(potential_indices)

    # Check no indices missing.
    for i,ui in enumerate(unique_indices):
        if i != ui:
            raise ValueError( "Potential index %d is missing." % (i) )

    # All sane, return.
    return value

def _checkAndSetPotentials(value):
    """ """
    """ Check if value is a valid potential. Currently, only None is accepted, i.e. default FEFF potentials are used.

    :param value: The input to check.
    :raises TypeError: if input is not None.
    """

    if value is None:
        return value
    else:
        raise ValueError( "Parameter 'potentials' must be None.")

def _checkAndSetEdge( value):
    """ """
    """ Check input value if a valid edge.

    :param value: The value to check.
    :raises TypeError: if not a str.
    :raises ValueError: if not a valid edge designator ('K', 'L1', 'L2', 'M1', 'M2', 'M3', ...).
    :return: The checked edge designator.
    """

    # Check default.
    if value is None:
        return 'K'

    # Check if str.
    if not isinstance(value, str):
        raise TypeError( "Parameter 'edge' must be a string.")

    # Lower case is ok, convert to upper.
    value = value.upper()

    # Accepted edges.
    valid_edges = ['K', 'L1', 'L2', 'M1', 'M2', 'M3']

    # Check if valid edge.
    if not value in valid_edges:
        raise ValueError( "Parameter 'edge' must be one of %s. " % (str(valid_edges)) )

    # All sane, return.
    return value

def _checkAndSetAmplitudeReductionFactor(value):
    """ """
    """ Check input value for amplitude_reduction_factor.

    :param value: The value to check.
    :raises TypeError: if not a float (0, 1 ok.)
    :raises ValueError: if not in range [0, 1].
    :return: The checked amplitude reduction factor.
    """

    # Handle default.
    if value is None:
        return 1.0

    # Convert to float.
    if isinstance( value, int):
        value = float( value )

    # Check type.
    if not isinstance( value, float ):
        raise TypeError( "Parameter 'amplitude_reduction_factor' must be a float. ")

    # Check range.
    if ( value < 0.0 ) or ( value > 1.0 ):
        raise ValueError( "Parameter 'amplitude_reduction_factor' must obey 0 <= x <= 1.")

    # All sane, return
    return value

def _checkAndSetEffectivePathDistance(value):
    """ """
    """ Check input value for effective_path_distance.

    :param value: The value to check.
    :raises TypeError: if not a number.
    :raises ValueError: if not >= 0.
    :return: The checked effective path distance.
    """

    # Handle default.
    if value is None:
        return None

    # Convert to float.
    if isinstance( value, int):
        value = float( value )

    # Check type.
    if not isinstance( value, float ):
        raise TypeError( "Parameter 'effective_path_distance' must be a float. ")

    # Check range.
    if ( value < 0.0 ):
        raise ValueError( "Parameter 'effective_path_distance' must obey x >= 0.")

    # All sane, return
    return value

