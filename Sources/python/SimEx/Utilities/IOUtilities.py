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
import os, shutil

from Bio import PDB
import periodictable

def checkAndGetPDB( path ):
    """ Query a given pdb code from the PDB.

    :param pdb_code: The PDB code of the molecule to query.
    :type pdb_code: str

    :return: The queried molecule pdb dataset.
    :rtype: ???

    """

    if path is None:
        raise IOError( "The parameter 'path' must be a path to a valid pdb file.")

    if not isinstance (path, str):
        raise IOError( "The parameter 'path' must be a path to a valid pdb file.")

    # Setup paths and filenames.
    pdb_target_name = os.path.basename(path).split('.pdb')[0]
    pdb_target_dir = os.path.dirname(path)
    source = os.path.join(pdb_target_dir, 'pdb'+pdb_target_name.lower()+'.ent')
    target = os.path.join(pdb_target_dir, pdb_target_name.lower()+'.pdb')

    if not os.path.isfile( path ):
        # Query from pdb.org
        pdb_list = PDB.PDBList()
        if pdb_target_dir == '':
            pdb_target_dir = '.'

        try:
            print "PDB file %s could not be found. Attempting to query from protein database server." % (path)
            pdb_list.retrieve_pdb_file( pdb_target_name, pdir=pdb_target_dir )
        except:
            raise IOError( "Database query failed.")

        # Move and rename the downloaded file.
        shutil.move( source, target  )

    return target


def loadPDB( path = None ):
    """ Wrapper to convert a given pdb file to a sample dictionary used by e.g. the XMDYNCalculator.

    :param path: The path to the pdb file to be converted.
    :type path: str

    :return: The dictionary describing the sample molecule.
    :rtype: dict
    """

    # Check if the sample is present, retrieve it from the pdb if not.
    target = checkAndGetPDB(path)

    # Convert to dict and return.
    return _pdbToS2ESampleDict(target)

def _pdbToS2ESampleDict(path=None):
    """ """
    """
    Workhorse function that converts a pdb file to the sample dictionary.

    :param path: Path to the pdb file to be loaded.
    :type path : string

    :return: The dictionary expected by downstream simex modules.
    :rtype : dict

    :throws IOError: Path not existing, not a pdb file or corrupt.
    """

    try:
        if not os.path.isfile( path ):
            raise IOError()
    except:
        raise IOError( "Parameter 'path' must be a valid pdb file.")

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
        raise IOError( "Input file %s is not a valid pdb file. " % (path) )


    if len(atoms_dict['Z']) == 0:
        raise IOError( "Input file %s is not a valid pdb file. " % (path) )

    # Get unique elements.
    for sel_Z in numpy.unique( atoms_dict['Z'] ) :
        atoms_dict['selZ'][sel_Z] = numpy.nonzero( atoms_dict['Z'] == sel_Z )[0]

    # Count number of atoms.
    atoms_dict['N'] = len( atoms_dict['Z'] )

    # Convert to numpy arrays.
    atoms_dict['Z'] = numpy.array( atoms_dict['Z'] )
    atoms_dict['r'] = numpy.array( atoms_dict['r'] )

    # Return.
    return atoms_dict




