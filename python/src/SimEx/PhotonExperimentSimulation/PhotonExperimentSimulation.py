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

""" Module that hosts the PhotonExperimentSimulation class, i.e. the top level object for running photon based experiment simulations
    @author : CFG
    @institution : XFEL GmbH Hamburg, Germany
    @creation : 20151005
"""

from SimEx.Calculators.AbstractPhotonSource import checkAndSetPhotonSource
from SimEx.Calculators.AbstractPhotonPropagator import checkAndSetPhotonPropagator
from SimEx.Calculators.AbstractPhotonDiffractor import checkAndSetPhotonDiffractor
from SimEx.Calculators.AbstractPhotonInteractor import checkAndSetPhotonInteractor
from SimEx.Calculators.AbstractPhotonDetector import checkAndSetPhotonDetector
from SimEx.Calculators.AbstractPhotonAnalyzer import checkAndSetPhotonAnalyzer

class PhotonExperimentSimulation:
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
        @type : Child of AbstractPhotonSource

        @param photon_propagator : The calculator for the wave propagation from source to target.
        @type : Child of AbstractPhotonPropagator

        @param photon_interactor : The calculator for the photon-matter interaction.
        @type : Child of AbstractPhotonInteractor

        @param : photon_diffractor : The calculator for the photon diffraction.
        @type : Child of AbstractPhotonDiffractor

        @param photon_detector : The calculator for photon detection.
        @type : Child of AbstractPhotonDetector

        @param photon_analyzer : The calculator for  photon signal analysis.
        @type : Child of AbstractPhotonAnalyzer
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
            status = status and set(self.__calculators[i+1].expectedData()).issubset( set(calculator.providedData()) )
        return status
