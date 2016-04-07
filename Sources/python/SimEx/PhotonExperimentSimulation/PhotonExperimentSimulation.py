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

""" Module that hosts the PhotonExperimentSimulation class, i.e. the top level object for running photon based experiment simulations
    @author : CFG
    @institution : XFEL GmbH Hamburg, Germany
    @creation : 20151005
"""



from SimEx.Calculators.AbstractPhotonAnalyzer   import checkAndSetPhotonAnalyzer
from SimEx.Calculators.AbstractPhotonDetector   import checkAndSetPhotonDetector
from SimEx.Calculators.AbstractPhotonDiffractor import checkAndSetPhotonDiffractor
from SimEx.Calculators.AbstractPhotonInteractor import checkAndSetPhotonInteractor
from SimEx.Calculators.AbstractPhotonPropagator import checkAndSetPhotonPropagator
from SimEx.Calculators.AbstractPhotonSource import checkAndSetPhotonSource

from SimEx.Utilities.EntityChecks import checkAndSetInstance

class PhotonExperimentSimulation(object):
    """ The PhotonExperimentSimulation is the top level object for running photon experiment simulations. It hosts the modules (calculators) ."""

    def __init__(self, photon_source=None,
                       photon_propagator=None,
                       photon_interactor=None,
                       photon_diffractor=None,
                       photon_detector=None,
                       photon_analyzer=None):
        """
        !@brief  Constructor for the PhotonExperimentSimulation object.

        @param photon_source: The calculator for the photon source.
        <br/><b>type</b> : Child of AbstractPhotonSource

        @param photon_propagator : The calculator for the wave propagation from source to target.
        <br/><b>type</b> : Child of AbstractPhotonPropagator

        @param photon_interactor : The calculator for the photon-matter interaction.
        <br/><b>type</b> : Child of AbstractPhotonInteractor

        @param : photon_diffractor : The calculator for the photon diffraction.
        <br/><b>type</b> : Child of AbstractPhotonDiffractor

        @param photon_detector : The calculator for photon detection.
        <br/><b>type</b> : Child of AbstractPhotonDetector

        @param photon_analyzer : The calculator for  photon signal analysis.
        <br/><b>type</b> : Child of AbstractPhotonAnalyzer
        """
        self.__photon_source = checkAndSetPhotonSource(photon_source)
        self.__photon_propagator = checkAndSetPhotonPropagator(photon_propagator)
        self.__photon_interactor = checkAndSetPhotonInteractor(photon_interactor)
        self.__photon_diffractor = checkAndSetPhotonDiffractor(photon_diffractor)
        self.__photon_detector = checkAndSetPhotonDetector(photon_detector)
        self.__photon_analyzer = checkAndSetPhotonAnalyzer(photon_analyzer)

        self.__calculators = [
                self.__photon_source,
                self.__photon_propagator,
                self.__photon_interactor,
                self.__photon_diffractor,
                self.__photon_analyzer,
                ]


        if self.__photon_detector is not None:
            self.__calculators.insert(-1, self.__photon_detector )

        if any([calc is None for calc in self.__calculators]):
            raise( TypeError, "No calculator can be None.")

    #######################
    # Queries and setters #
    #######################
    @property
    def photon_source(self):
        """ Query for the photon source attached to this workflow. """
        return self.__photon_source
    @photon_source.setter
    def photon_source(self, value):
        self.__photon_source = checkAndSetPhotonSource( value )

    @property
    def photon_propagator(self):
        """ Query for the photon propagator attached to this workflow. """
        return self.__photon_propagator
    @photon_propagator.setter
    def photon_propagator(self, value):
        self.__photon_propagator = checkAndSetPhotonPropagator( value )

    @property
    def photon_interactor(self):
        """ Query for the photon interactor attached to this workflow. """
        return self.__photon_interactor
    @photon_interactor.setter
    def photon_interactor(self, value):
        self.__photon_interactor = checkAndSetPhotonInteractor( value )

    @property
    def photon_diffractor(self):
        """ Query for the photon diffractor attached to this workflow. """
        return self.__photon_diffractor
    @photon_diffractor.setter
    def photon_diffractor(self, value):
        self.__photon_diffractor = checkAndSetPhotonDiffractor( value )

    @property
    def photon_detector(self):
        """ Query for the photon detector attached to this workflow. """
        return self.__photon_detector
    @photon_detector.setter
    def photon_detector(self, value):
        self.__photon_detector = checkAndSetPhotonDetector( value )

    @property
    def photon_analyzer(self):
        """ Query for the photon analyzer attached to this workflow. """
        return self.__photon_analyzer
    @photon_analyzer.setter
    def photon_analyzer(self, value):
        self.__photon_analyzer = checkAndSetPhotonAnalyzer( value )

    def run(self):
        """ Method to start the photon experiment simulation workflow. """

        if not self._checkInterfaceConsistency():
            raise RuntimeError(" Interfaces are not consistent, i.e. at least one module's expectations with respect to incoming data sets are not satisfied.")

        print '\n'.join(["#"*80,  "# Starting SIMEX run.", "#"*80])
        print '\n'.join(["#"*80,  "# Starting SIMEX photon source.", "#"*80])
        self.__photon_source._readH5()
        self.__photon_source.backengine()
        self.__photon_source.saveH5()

        print '\n'.join(["#"*80,  "# Starting SIMEX photon propagation.", "#"*80])
        self.__photon_propagator._readH5()
        self.__photon_propagator.backengine()
        self.__photon_propagator.saveH5()

        print '\n'.join(["#"*80,  "# Starting SIMEX photon-matter interaction.", "#"*80])
        self.__photon_interactor._readH5()
        self.__photon_interactor.backengine()
        self.__photon_interactor.saveH5()

        print '\n'.join(["#"*80,  "# Starting SIMEX photon diffraction.", "#"*80])
        self.__photon_diffractor._readH5()
        self.__photon_diffractor.backengine()
        self.__photon_diffractor.saveH5()

        if self.__photon_detector is not None:
            print '\n'.join(["#"*80,  "# Starting SIMEX photon detection.", "#"*80])
            self.__photon_detector._readH5()
            self.__photon_detector.backengine()
            self.__photon_detector.saveH5()

        print '\n'.join(["#"*80,  "# Starting SIMEX photon signal analysis.", "#"*80])
        self.__photon_analyzer._readH5()
        self.__photon_analyzer.backengine()
        self.__photon_analyzer.saveH5()

        print '\n'.join(["#"*80,  "# SIMEX  done.", "#"*80])


    def _checkInterfaceConsistency(self):
        """
        Check that all calculators provide the data expected by the next downstream
        calculator.
        """
        status = True
        for i,calculator in enumerate(self.__calculators[:-1]):
            provided_data_set = set(calculator.providedData())
            expected_data_set = set(self.__calculators[i+1].expectedData())
            if not expected_data_set.issubset( provided_data_set ):
                raise RuntimeError( "Dataset expected by %s is not a subset of data provided by %s.\n Provided data are:\n%s.\n\n Expected data are:\n%s" % (self.__calculators[i+1], calculator, str(provided_data_set).replace(',', '\n'), str(expected_data_set).replace(',', '\n') ) )
        return status
