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
#                                                                        #
##########################################################################


input_path = 'default'
output_path = 'default'

parameters={ 'uniform_rotation': True,
             'calculate_Compton' : False,
             'slice_interval' : 100,
             'number_of_slices' : 2,
             'pmi_start_ID' : 1,
             'pmi_stop_ID'  : 1,
             'number_of_diffraction_patterns' : 2,
             'extra_MPI_parameters' : '',
             'beam_parameter_file' : 'input/s2e.beam',
             'beam_geometry_file' : 'input/s2e.geom',
           }

