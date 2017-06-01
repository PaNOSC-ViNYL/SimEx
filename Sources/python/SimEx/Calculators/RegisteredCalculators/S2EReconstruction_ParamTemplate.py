##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 Carsten Fortmann-Grote                         #
#               2016-2017 Sergey Yakubov                                 #
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


EMC_Parameters = {'initial_number_of_quaternions' : 1,
                  'max_number_of_quaternions'     : 9,
                  'max_number_of_iterations'      : 3,
                  'min_error'                     : 1.0e-8,
                  'beamstop'                      : 1.0e-5,
                  'detailed_output'               : False
                 }

DM_Parameters = {'number_of_trials'        : 5,
                 'number_of_iterations'    : 2,
                 'averaging_start'         : 15,
                 'leash'                   : 0.2,
                 'number_of_shrink_cycles' : 2,
                }

parameters = {'EMC_Parameters' : EMC_Parameters, 'DM_Parameters' : DM_Parameters}


