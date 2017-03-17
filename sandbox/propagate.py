#! /usr/bin/env python2.7

import sys

from SimEx.Calculators.XFELPhotonPropagator import XFELPhotonPropagator

#pulse_file = '5keV_9fs_0000001.h5'
pulse_file = sys.argv[1]
out_file = sys.argv[2]


propagator = XFELPhotonPropagator(
        parameters=None,
        input_path=pulse_file,
        output_path=out_file,
        )

propagator.backengine()
