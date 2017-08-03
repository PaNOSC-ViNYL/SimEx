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

""" Module that holds the ComptonScatteringCalculator class.

    @author : CFG
    @institution : XFEL
    @creation 20160404

"""
import h5py
import math
import numpy
import os
import re
#from scipy.optimize import newton as root
from scipy.optimize import brentq as root
from scipy.constants import physical_constants as PC
from scipy import constants as C
import subprocess
import tempfile

from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Utilities.EntityChecks import checkAndSetInstance, checkAndSetPositiveInteger

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters

# Some constants
BOHR = PC['Bohr radius'][0]
RY = PC['Rydberg constant times hc in eV'][0]
ALPHA = C.alpha

class ComptonScatteringCalculator(AbstractPhotonDiffractor):
    """
    Class representing a Compton scattering calculator.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """
        Constructor for the ComptonScatteringCalculator.

        @param parameters : Parameters for the ComptonScatteringCalculator.
        @type : dict
        @default : None
        """

        # Check parameters.
        parameters = checkAndSetParameters( parameters )

        # Hack to work around input path checking.
        if input_path is None:
            tmppath = tempfile.mkdtemp()
            input_path = os.path.join(tmppath, 'xrts_in.h5')
            dummy = h5py.File(input_path, 'w')


        # Init base class.
        super( ComptonScatteringCalculator, self).__init__(parameters, input_path, output_path)

        # Set state to not-initialized (e.g. input deck is not written).
        self.__is_initialized = False

        # Overwrite provided_data.
        #self.__expected_data = ['/data/snp_<7 digit index>/ff',
                                #'/data/snp_<7 digit index>/halfQ',
                                #'/data/snp_<7 digit index>/Nph',
                                #'/data/snp_<7 digit index>/r',
                                #'/data/snp_<7 digit index>/T',
                                #'/data/snp_<7 digit index>/Z',
                                #'/data/snp_<7 digit index>/xyz',
                                #'/data/snp_<7 digit index>/Sq_halfQ',
                                #'/data/snp_<7 digit index>/Sq_bound',
                                #'/data/snp_<7 digit index>/Sq_free',
                                #'/history/parent/detail',
                                #'/history/parent/parent',
                                #'/info/package_version',
                                #'/info/contact',
                                #'/info/data_description',
                                #'/info/method_description',
                                #'/version']

        #self.__provided_data = [
                                #'/data/',
                                #'/data/dynamic'
                                #'/data/dynamic/energy_shifts',
                                #'/data/dynamic/Skw_free',
                                #'/data/dynamic/Skw_bound',
                                #'/data/dynamic/collision_frequency',
                                #'/data/static'
                                #'/data/static/Sk_bound',
                                #'/data/static/Sk_ion',
                                #'/data/static/Sk_elastic',
                                #'/data/static/Sk_core_inelastic',
                                #'/data/static/Sk_free_inelastic',
                                #'/data/static/Sk_total',
                                #'/data/static/fk',
                                #'/data/static/qk',
                                #'/data/static/ionization_potential_delta'
                                #'/data/static/LFC',
                                #'/history/parent/detail',
                                #'/history/parent/parent',
                                #'/info/package_version',
                                #'/info/contact',
                                #'/info/data_description',
                                #'/info/method_description',
                                #'/info/units/energy'
                                #'/info/units/structure_factor'
                                #'/params/beam/photonEnergy',
                                #'/params/beam/spectrum',
                                #'/params/info',
                                #]

        self._input_data = {}

        self.energy_shifts = numpy.arange(-self.parameters.energy_range['max'],
                                          -self.parameters.energy_range['min'],
                                           self.parameters.energy_range['step'],
                                          )

        self.source_energy = self.parameters.photon_energy
        self.scattering_angle = self.parameters.scattering_angle
        self.electron_density = self.parameters.electron_density*1e6
        print self.electron_density
        self.temperature = self.parameters.electron_temperature

        self.pzs = _pz( self.source_energy, self.source_energy - self.energy_shifts, self.scattering_angle)


        self.fermi_energy = _fermiEnergy( self.electron_density )
        self.fermi_wavenumber = _fermiWavenumber( self.electron_density )
        self.chemical_potential = _chemicalPotential(self.electron_density, self.temperature)

        self.compton_profile = self._comptonProfile()

    def expectedData(self):
        """ Query for the data expected by the Diffractor. """
        return self.__expected_data

    def providedData(self):
        """ Query for the data provided by the Diffractor. """
        return self.__provided_data

    def backengine(self):
        """ This method drives the backengine xrts."""


    def _comptonProfile(self):
        """ Workhorse function that calculates the Compton profile. """

        # Fix variables and parameters.
        pF = self.fermi_wavenumber
        EF = self.fermi_energy
        theta = self.temperature / self.fermi_energy
        y = self.chemical_potential / self.temperature

        rho_z = (self.pzs*BOHR)**2 / self.temperature*RY - y

        # Calculate profile.
        J = 0.75 * theta * numpy.log( 1. + numpy.exp( -rho_z ) )

        # Return.
        return J

    @property
    def data(self):
        """ Query for the field data. """
        return self.__data

    def _readH5(self):
        """ """
        """ Private method for reading the hdf5 input and extracting the parameters and data relevant to initialize the object. """

        raise RuntimeError("Not implemented.")

    def saveH5(self):
        """ """
        """
        Method to save the data to a file.

        @param output_path : The file where to save the object's data.
        @type : string
        @default : None
        """
        raise RuntimeError("Not implemented.")

    def _printProfile(self):
        """ Method to write the Compton profile to stdout. """

        for i in range(len(self.compton_profile)):
            print self.pzs[i], self.energy_shifts[i], self.compton_profile[i]

##########################
# Check and set functions #
###########################
def checkAndSetParameters( parameters ):
    """ Utility to check if the parameters dictionary is ok ."""

    if not isinstance( parameters, AbstractCalculatorParameters ):
        raise RuntimeError( "The 'parameters' argument must be of the type PlasmaXRTSCalculatorParameters.")
    ### TODO: make an abstract parameters class.
    return parameters


def _fermiEnergy(ne):
    """ Calculates the Fermi energy from a given electron density. """

    # Get Fermi momentum in inverse Bohr.
    kF = _fermiWavenumber( ne ) * BOHR

    # Get Fermi energy in Rydberg
    EF = kF**2

    # Return Fermi energy in eV
    return EF * RY


def _fermiWavenumber( ne ):
    """ Calculate the Fermi wavenumber kF. """
    # Convert density to inverse qubic Bohr.
    neaB = ne * BOHR ** 3

    # Get Fermi momentum in inverse Bohr.
    kF = ( 3. * math.pi**2 * neaB )**(1./3.)

    # Return Fermi wavenumber in 1/m.
    return kF / BOHR


def _chemicalPotential(ne, T):
    """ Calculate the chemical potential at given electron density and temperature through inversion
    of the Fermi integral F_1/2. """

    EF = _fermiEnergy( ne )
    theta = T/EF
    # Thermal wavelength in Bohr.
    lambda_e_aB = 2.*math.sqrt(math.pi/T*RY)

    # Density in Bohr**-3
    neaB = ne * BOHR**3

    # Locate the root in the interval [3/2 ln(ne lambda_T**3 / 2) , EF/T ]
    search_interval_minimum = 1.5 * math.log( 0.5 * neaB * lambda_e_aB**3 )
    search_interval_maximum = 1./theta
    y = root(_chemicalPotentialRoot, a=search_interval_minimum, b=search_interval_maximum, args=(theta,0))

    return y * T


def fermihalf(x,sgn):
    """ Series approximation to the F_{1/2}(x) or F_{-1/2}(x)
        Fermi-Dirac integral.
        Credits: Greg von Winckel
        http://www.scientificpython.net/pyblog/approximate-fermi-dirac-integrals"""

    f = lambda k: numpy.sqrt(x**2+numpy.pi**2*(2*k-1)**2)


    if sgn>0: # F_{1/2}(x)
        a = numpy.array((1.0/770751818298,-1.0/3574503105,-13.0/184757992,
              85.0/3603084,3923.0/220484,74141.0/8289,-5990294.0/7995))
        g = lambda k:numpy.sqrt(f(k)-x)

    else:  # F_{-1/2}(x)
        a = numpy.array((-1.0/128458636383,-1.0/714900621,-1.0/3553038,
                      27.0/381503,3923.0/110242,8220.0/919))
        g = lambda k:-0.5*numpy.sqrt(f(k)-x)/f(k)

    F = numpy.polyval(a,x) + 2*numpy.sqrt(2*numpy.pi)*sum(map(g,range(1,21)))

    return  F # Prefactor to get normalized Fermi integral.

def _chemicalPotentialRoot(y, *args):

    # Get theta argument.
    theta = args[0]

    # Compute the function to root.
    ret =  2./3. / theta**1.5 - 0.5 * math.sqrt(math.pi) * fermihalf(y,1)

    # Return.
    return ret


def _pz( wi, wf, theta ):
    """ Calculate the z component of the scattering transfer momentum p. """

    # ALL IN RY UNITS.
    i = wi / RY
    f = wf / RY

    m0 = 0.5
    c = 2./ALPHA
    th = theta * math.pi / 180.


    nom = i - f - i*f/m0/c**2*(1.-math.cos(th))
    denom = numpy.sqrt( i**2 + f**2 - 2.*i*f*math.cos(th) )

    return m0 * c * nom / denom  / BOHR

