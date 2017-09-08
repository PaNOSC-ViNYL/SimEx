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
# Include needed directories in sys.path.                                #
#                                                                        #
##########################################################################

import time,datetime,os

def prGreen(prt,newline=True):
	print ("\033[92m{}\033[00m" .format(prt))

def prCyan(prt,newline=True):
	print ("\033[96m{}\033[00m" .format(prt))

start_time=time.time()
prCyan("="*80)
prCyan("Simex platform. Copyright (C) 2015-2017.")
prCyan("Running project ${PROJECT_NAME}")
prCyan("-"*80)

# modules will be added here


prCyan("-"*80)

prCyan("Simex finished in "+str(datetime.timedelta(seconds=time.time()-start_time)))

