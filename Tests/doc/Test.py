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

import unittest
import os, sys

# Define the encapsulating test suite.
def suite():
    suites = [
               unittest.makeSuite(DocTest, 'test')
             ]

    return unittest.TestSuite(suites)

class DocTest(unittest.TestCase):
    """
    Test class for the documentation.
    """

    def testDocPresence(self):
        """ Test if the documentation was generated. """
        path_to_check =  os.path.abspath( os.path.join( os.path.dirname(__file__), '..','..', 'share','doc','simex','index.html') )
        print "Checking %s." % (path_to_check)
        self.assertTrue( os.path.isfile( path_to_check) )


# Run the top level suite and return a success status code. This enables running an automated git-bisect.
if __name__=="__main__":

    result = unittest.TextTestRunner(verbosity=2).run(suite())

    if result.wasSuccessful():
        print '---> OK <---'
        sys.exit(0)

    sys.exit(1)
