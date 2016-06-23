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

""" Module for entity checks.
    @author CFG
    @institution XFEL
    @creation 20160623
"""

import exceptions
import numpy
import os

from Bio import PDB
import periodictable
import matplotlib.mlab # Yes, we actually need it.

def loadPDB( path = None ):
    """
    Utility to load a pdb file and convert it to a dict that will be taken by e.g.
    PMI calculators.

    @param path: Path to the pdb file to be loaded.
    @type : string

    @return : The dictionary expected by downstream simex modules.
    @rtype  : dict

    @throws IOError is path not existing, not a pdb file or corrupt.
    """

    if path is None:
        raise IOError( "The parameter 'path' must be a path to a valid pdb file.")

    if not isinstance (path, str):
        raise IOError( "The parameter 'path' must be a path to a valid pdb file.")

    if not os.path.isfile( path ):
        raise IOError( "The parameter 'path' must be a path to a valid pdb file.")

    # Setup the return dictionary.
    atoms_dict = {'Z' : [],     # Atomic number.
                  'r' : [],     # Cartesian coordinates.
                  'selZ' : {},  # Abundance of each element.
                  'N' : 0,      # Number of atoms.
                  }


    # Attempt loading the pdb.
    try:
        parser = PDB.PDBParser()
        structure = parser.get_structure("sample", path)

        # Get the atoms.
        atoms = structure.get_atoms()

        # Loop over atoms and get charge and coordinates.
        for atom in atoms:

            # Get the element symbol from pdb.
            symbol = atom.element.title()

            # Get the coordinates from pdb.
            coordinates = atom.coord

            # Get the corresponding periodic table element as an instance.
            atom_obj = getattr(periodictable, symbol)

            # Query the atomic number.
            charge = atom_obj.number

            # Write to dict.
            atoms_dict['Z'].append(charge)
            atoms_dict['r'].append(coordinates)

    except:
        raise IOError( "Input file is not a valid pdb file. ")


    if len(atoms_dict['Z']) == 0:
        raise IOError( "Input file is not a valid pdb file. ")

    # Get unique elements.
    for sel_Z in numpy.unique( atoms_dict['Z'] ) :
        atoms_dict['selZ'][sel_Z] = matplotlib.mlab.find( sel_Z == atoms_dict['Z'] )

    # Count number of atoms.
    atoms_dict['N'] = len( atoms_dict['Z'] )

    # Convert to numpy arrays.
    atoms_dict['Z'] = numpy.array( atoms_dict['Z'] )
    atoms_dict['r'] = numpy.array( atoms_dict['r'] )

    # Return.
    return atoms_dict




