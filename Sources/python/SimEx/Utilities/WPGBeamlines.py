from wpg import Beamline
from wpg.optical_elements import Drift, Aperture, CRL
from wpg.optical_elements import Use_PP
from wpg.useful_code import srwutils

# Import the prop beamline.
from prop import exfel_spb_kb_beamline
from prop import exfel_spb_day1_beamline

import errno
import numpy
import os
import wpg

def setupSPBDay1Beamline():
    """ Setup and return a WPG beamline corresponding to the SPB day 1 configuration. """

    return exfel_spb_day1_beamline

def setup_S2E_SPI_beamline():
    """ Utility function that returns the S2E SPI beamline (Yoon et al. Scientific Reports (2016). """
    return exfel_spb_kb_beamline

