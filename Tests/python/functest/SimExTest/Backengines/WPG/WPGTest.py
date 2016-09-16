##########################################################################
#                                                                        #
# Copyright (C) 2015, 2016 Carsten Fortmann-Grote                        #
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

""" Functional test for WPG.

    @author : CFG
    @institution : XFEL
    @creation 20160818

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import h5py
import math
import numpy
import os, shutil
import paths
import unittest

import wpg

from wpg import Wavefront, Beamline
from wpg.optical_elements import Drift
from wpg.optical_elements import Aperture
from wpg.optical_elements import CRL
from wpg.optical_elements import WF_dist
from wpg.optical_elements import calculateOPD
from wpg.optical_elements import Use_PP


#import SRW core functions
from wpg.srwlib import srwl

##Gaussian beam generator
from wpg.generators import build_gauss_wavefront

from wpg.wpg_uti_wf import calculate_fwhm
from wpg.wpg_uti_wf import plot_t_wf, look_at_q_space
from wpg.wpg_uti_oe import show_transmission

from TestUtilities import TestUtilities

class WPGTest(unittest.TestCase):
    """
    Test class for the WPG backengine.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """

        for f in self.__files_to_remove:
            if os.path.isfile(f): os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d): shutil.rmtree(d)

    def testGaussianReference(self, debug=False):
        """ Check that propagation of a Gaussian pulse (in t,x,y) through vacuum reproduces reference data. """


        # Central photon energy.
        ekev = 8.4 # Energy [keV]

        # Pulse parameters.
        qnC = 0.5               # e-bunch charge, [nC]
        pulse_duration = 9.0e-15 # [s]
        pulseEnergy = 1.5e-3    # total pulse energy, J

        # Coherence time
        coh_time = 0.25e-15 # [s]

        # Distance in free space.
        z0 = 10. # (m), position where to build the wavefront.
        z1 = 10. # (m), distance to travel in free space.

        # Beam divergence.
        theta_fwhm = 2.5e-6 # rad

        wlambda = 12.4*1e-10/ekev # wavelength, m
        w0 = wlambda/(numpy.pi*theta_fwhm) # beam waist, m
        zR = (math.pi*w0**2)/wlambda #Rayleigh range, m
        fwhm_at_zR = theta_fwhm*zR #FWHM at Rayleigh range, m
        sigmaAmp = w0/(2.0*math.sqrt(math.log(2.0))) #sigma of amplitude, m

        if debug:
            print (" *** Pulse properties ***")
            print (" lambda = %4.3e m" % (wlambda) )
            print (" w0 = %4.3e m" % (w0) )
            print (" zR = %4.3e m" % (zR) )
            print (" fwhm at zR = %4.3e m" % (fwhm_at_zR) )
            print (" sigma = %4.3e m" % (sigmaAmp) )

        # expected beam radius after free space drift.
        expected_beam_radius = w0*math.sqrt(1.0+(z0/zR)**2)


        # Number of points in each x and y dimension.
        np=400

        # Sampling window = 6 sigma of initial beam.
        range_xy = 6.*expected_beam_radius
        dx = range_xy / (np-1)
        nslices = 20

        if debug:
            print (" Expected beam waist at z=%4.3f m : %4.3e m." % (z0, expected_beam_radius) )
            print ("Setting up mesh of %d points per dimension on a %4.3e x %4.3e m^2 grid with grid spacing %4.3e m." % (np, range_xy, range_xy, dx) )

        # Construct srw wavefront.
        srwl_wf = build_gauss_wavefront(np, np, nslices, ekev, -range_xy/2., range_xy/2.,
                                        -range_xy/2., range_xy/2., coh_time/math.sqrt(2.),
                                        sigmaAmp, sigmaAmp, z0,
                                        pulseEn=pulseEnergy, pulseRange=8.)

        # Convert to wpg.
        wf = Wavefront(srwl_wf)

        if debug:
            print('*** z=%4.3e m ***' % (z0))
            fwhm = calculate_fwhm(wf)
            print('fwhm_x = %4.3e\nfwhm_y = %4.3e' % (fwhm['fwhm_x'], fwhm['fwhm_y']) )
            plot_t_wf(wf)
            look_at_q_space(wf)

        # Construct the beamline.
        beamline = Beamline()

        # Add free space drift.
        drift = Drift(z1)
        beamline.append( drift, Use_PP(semi_analytical_treatment=1))

        # Propagate
        srwl.SetRepresElecField(wf._srwl_wf, 'f') # <---- switch to frequency domain
        beamline.propagate(wf)
        srwl.SetRepresElecField(wf._srwl_wf, 't')

        if debug:
            print('*** z=%4.3e m ***' % (z0+z1))
            fwhm = calculate_fwhm(wf)
            print('fwhm_x = %4.3e\nfwhm_y = %4.3e' % (fwhm['fwhm_x'], fwhm['fwhm_y']) )
            plot_t_wf(wf)
            look_at_q_space(wf)


        # Get propagated wavefront data.
        wf_intensity = wf.get_intensity()

        # Project on t axis.
        wf_onaxis = wf_intensity.sum(axis=(0,1))

        # Get hash of the data.
        wf_hash = hash( wf_intensity.tostring() )

        # Load reference hash.
        with open(TestUtilities.generateTestFilePath("reference_wf_gauss_10m.hash.txt"), 'r') as hashfile:
            ref_hash = hashfile.readline()
            hashfile.close()
        ref_onaxis = numpy.loadtxt(TestUtilities.generateTestFilePath("reference_wf_gauss_onaxis_10m.txt"))

        # Weak test.
        for x,y in zip(wf_onaxis, ref_onaxis):
            self.assertAlmostEqual( x, y, 14 )

        # Strong test.
        self.assertEqual( str(wf_hash), ref_hash)

        # Save wavefront data for reference.
        #########################################################################################
        ## ATTENTION: Overwrites reference data, use only if you're sure you want to do this. ###
        #########################################################################################
        #with open(TestUtilities.generateTestFilePath("reference_wf_gauss_10m.hash.txt", 'w')) as hashfile:
            #hashfile.write(str(wf_hash))
            #hashfile.close()
        #numpy.savetxt( TestUtilities.generateTestFilePath("reference_wf_gauss_onaxis_10m.txt", wf_onaxis ))
        #########################################################################################

    def testGaussianVsAnalytic(self, debug=False):
        """ Check that propagation of a Gaussian pulse (in t,x,y) through vacuum gives the correct result, compare
        to analytic solution. """


        # Central photon energy.
        ekev = 8.4 # Energy [keV]

        # Pulse parameters.
        qnC = 0.5               # e-bunch charge, [nC]
        pulse_duration = 9.0e-15 # [s]
        pulseEnergy = 1.5e-3    # total pulse energy, J

        # Coherence time
        coh_time = 0.25e-15 # [s]

        # Distance in free space.
        z0 = 10. # (m), position where to build the wavefront.
        z1 = 20. # (m), distance to travel in free space.
        z2 = z0 + z1 #  distance where to build the reference wavefront.

        # Beam divergence.
        theta_fwhm = 2.5e-6 # rad

        wlambda = 12.4*1e-10/ekev # wavelength, m
        w0 = wlambda/(numpy.pi*theta_fwhm) # beam waist, m
        zR = (math.pi*w0**2)/wlambda #Rayleigh range, m
        fwhm_at_zR = theta_fwhm*zR #FWHM at Rayleigh range, m
        sigmaAmp = w0/(2.0*math.sqrt(math.log(2.0))) #sigma of amplitude, m

        if debug:
            print (" *** Pulse properties ***")
            print (" lambda = %4.3e m" % (wlambda) )
            print (" w0 = %4.3e m" % (w0) )
            print (" zR = %4.3e m" % (zR) )
            print (" fwhm at zR = %4.3e m" % (fwhm_at_zR) )
            print (" sigma = %4.3e m" % (sigmaAmp) )

        # expected beam radius after free space drift.
        expected_beam_radius = w0*math.sqrt(1.0+(z0/zR)**2)

        # Number of points in each x and y dimension.
        np=600

        # Sampling window = 6 sigma of initial beam.
        range_xy = 6.*expected_beam_radius
        dx = range_xy / (np-1)
        nslices = 20

        #if debug:
            #print (" Expected beam waist at z=%4.3f m : %4.3e m." % (z0, expected_beam_radius) )
            #print ("Setting up mesh of %d points per dimension on a %4.3e x %4.3e m^2 grid with grid spacing %4.3e m." % (np, range_xy, range_xy, dx) )

        # Construct srw wavefront.
        srwl_wf = build_gauss_wavefront(np, np, nslices, ekev, -range_xy/2., range_xy/2.,
                                        -range_xy/2., range_xy/2., coh_time/math.sqrt(2.),
                                        sigmaAmp, sigmaAmp, z0,
                                        pulseEn=pulseEnergy, pulseRange=8.)

        # Convert to wpg.
        wf = Wavefront(srwl_wf)

        # Construct reference srw wavefront.
        reference_srwl_wf = build_gauss_wavefront(np, np, nslices, ekev, -1.5*range_xy/2., 1.5*range_xy/2.,
                                        -1.5*range_xy/2., 1.5*range_xy/2., coh_time/math.sqrt(2.),
                                        sigmaAmp, sigmaAmp, z2,
                                        pulseEn=pulseEnergy, pulseRange=8.)

        reference_wf = Wavefront(reference_srwl_wf)

        if debug:
            print('*** z=%4.3e m ***' % (z0))
            fwhm = calculate_fwhm(wf)
            print('wf:\nfwhm_x = %4.3e\nfwhm_y = %4.3e' % (fwhm['fwhm_x'], fwhm['fwhm_y']) )
            plot_t_wf(wf)
            #look_at_q_space(wf)

        # Construct the beamline.
        beamline = Beamline()

        # Add free space drift.
        drift = Drift(z1)
        beamline.append( drift, Use_PP(semi_analytical_treatment=0, zoom=2.0, sampling=0.5))

        # Propagate
        srwl.SetRepresElecField(wf._srwl_wf, 'f')
        beamline.propagate(wf)
        srwl.SetRepresElecField(wf._srwl_wf, 't')

        fwhm = calculate_fwhm(wf)
        reference_fwhm = calculate_fwhm(reference_wf)
        if debug:
            print('*** z=%4.3e m ***' % (z0+z1))
            print('wf :\nfwhm_x = %4.3e\nfwhm_y = %4.3e' % (fwhm['fwhm_x'], fwhm['fwhm_y']) )
            plot_t_wf(wf)
            print('ref:\nfwhm_x = %4.3e\nfwhm_y = %4.3e' % (reference_fwhm['fwhm_x'], reference_fwhm['fwhm_y']) )
            plot_t_wf(reference_wf)
            #look_at_q_space(wf)

        # Calculate difference
        reference_norm = numpy.linalg.norm(numpy.array([reference_fwhm['fwhm_x'], reference_fwhm['fwhm_y']]))
        difference_norm = numpy.linalg.norm(numpy.array([fwhm['fwhm_x'], fwhm['fwhm_y']]) - numpy.array([reference_fwhm['fwhm_x'], reference_fwhm['fwhm_y']]))

        if debug:
            print ("|ref_fwhm_xy| = %4.3e" % (reference_norm) )
            print ("|ref_fwhm_xy - fhwm_xy| = %4.3e" % (difference_norm) )

        self.assertLess(difference_norm / reference_norm, 0.01)

if __name__ == '__main__':
    unittest.main()
