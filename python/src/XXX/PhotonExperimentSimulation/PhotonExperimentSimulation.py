""" Module that hosts the PhotonExperimentSimulation class, i.e. the top level object for running photon based experiment simulations
    @author : CFG
    @institution : XFEL GmbH Hamburg, Germany
    @creation : 20151005
"""

from XXX.Calculators.AbstractPhotonSource import checkAndSetPhotonSource
from XXX.Calculators.AbstractPhotonPropagator import checkAndSetPhotonPropagator

class PhotonExperimentSimulation:
    """ The PhotonExperimentSimulation is the top level object for running photon experiment simulations. It hosts the modules (calculators) ."""

    def __init__(self, photon_source=None,
                       photon_propagator=None,
                       photon_interactor=None,
                       photon_diffractor=None,
                       photon_detector=None,
                       photon_analyser=None):
        """
        Constructor for the PhotonExperimentSimulation object.

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

        @param photon_analyser : The calculator for  photon signal analysis.
        @type : Child of AbstractPhotonAnalyser
        """

        self.__photon_source = checkAndSetPhotonSource(photon_source)
        self.__photon_propagator = checkAndSetPhotonPropagator(photon_propagator)
        #self.__photon_interactor = checkAndSetPhotonInteractor(photon_interactor)
        #self.__photon_diffractor = checkAndSetPhotonDiffractor(photon_diffractor)
        #self.__photon_detector = checkAndSetPhotonDetector(photon_detector)
        #self.__photon_analyser = checkAndSetPhotonAnalyser(photon_analyser)

    def run(self):
        """ Method to start the photon experiment simulation workflow. """

        self.__photon_source._readH5()
        self.__photon_source.saveH5()

        self.__photon_propagator._readH5()
        self.__photon_propagator.backengine()
        self.__photon_propagator.saveH5()
