##########################################################################
#                                                                        #
# Copyright (C) 2015 Carsten Fortmann-Grote                              #
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
# Include needed directories in sys.path.                                #
#                                                                        #
##########################################################################

""" Utility to expose all modules under src/ in the unittest directories."""

import os, sys
import os.path

file_path = os.path.abspath(os.path.dirname(__file__))
separator = os.sep
separated_file_path = file_path.split(separator)
top_level_index = separated_file_path.index('python')
top_level_path = os.path.abspath(separator.join(separated_file_path[:top_level_index+1]))

paths_to_insert = ['src/',
                   'unittest/',
		   'lib/'
                   ]

for p in paths_to_insert:
    path = os.path.join(top_level_path, p)
    if not path in sys.path:
        sys.path.insert(1, path)

del top_level_path, file_path, separated_file_path
