from wpg import Beamline
from wpg.optical_elements import Drift, Aperture, CRL
from wpg.optical_elements import Use_PP
from wpg.useful_code import srwutils

import errno
import numpy
import os
import wpg

# Storage location for mirror height profile data.
mirror_data1 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mirror1.dat')
mirror_data2 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mirror2.dat')


def defineOPD(opTrErMirr, mdatafile, ncol, delim, orient, theta, scale=1., stretching=1.):
    """
    Define optical path difference (OPD) from mirror profile

    :param opTrErMirr: the struct with wave front distortions from mirror susrface errors
    :param mdatafile: an ascii file with mirror profile data
    :param ncol: number of columns in the mirror profile file
    :param delim: delimiter between numbers in an row, can be space (' '), tab '\t', etc
    :param orient: mirror orientation, 'x' (horizontal) or 'y' (vertical)
    :param theta: mirror incidence angle
    :param scale: scaling factor for the mirror profile height errors
    :param stretching: scaling factor for the mirror profile x-axis (a hack, should be removed ASAP)
    """
    heightProfData = numpy.loadtxt(mdatafile).T
    heightProfData[0,:] = heightProfData[0,:] * stretching
    srwutils.AuxTransmAddSurfHeightProfileScaled(opTrErMirr, heightProfData, orient, theta, scale)

def setupSPBDay1Beamline():
    """ Setup and return a WPG beamline corresponding to the SPB day 1 configuration. """


    ### Geometry ###
    src_to_hom1 = 257.8 # Distance source to HOM 1 [m]
    src_to_hom2 = 267.8 # Distance source to HOM 2 [m]
    src_to_crl = 887.8  # Distance source to CRL [m]
    src_to_exp = 920.42 # Distance source to experiment [m]

    #Incidence angle at HOM
    theta_om = 3.6e-3       # [rad]

    om_mirror_length = 0.8 # [m]
    om_clear_ap = om_mirror_length*theta_om


    #define the beamline:
    beamline = Beamline()
    zoom=1

    # Define HOM1 = Aperture + Wavefront distortion.
    aperture_x_to_y_ratio = 1
    hom1_aperture = Aperture(shape='r',ap_or_ob='a',Dx=om_clear_ap,Dy=om_clear_ap/aperture_x_to_y_ratio)

    # Append to beamline.
    beamline.append( hom1_aperture, Use_PP(semi_analytical_treatment=0, zoom=zoom, sampling=zoom) )

    # Free space propagation from hom1 to hom2
    hom1_to_hom2_drift = Drift(src_to_hom2 - src_to_hom1)
    beamline.append( hom1_to_hom2_drift, Use_PP(semi_analytical_treatment=0))

    # Define HOM2.
    zoom = 1.0
    hom2_aperture = Aperture('r','a', om_clear_ap, om_clear_ap/aperture_x_to_y_ratio)
    beamline.append( hom2_aperture,  Use_PP(semi_analytical_treatment=0, zoom=zoom, sampling=zoom))

    #drift to CRL aperture
    hom2_to_crl_drift = Drift( src_to_crl - src_to_hom2 )
    beamline.append( hom2_to_crl_drift, Use_PP(semi_analytical_treatment=1))

    # Circular Aperture before CRL.
    crl_front_aperture_diameter = 2.8e-3
    crl_front_aperture = Aperture('c','a', crl_front_aperture_diameter, crl_front_aperture_diameter)

    ### Define CRL
    crl_focussing_plane = 3 # Both horizontal and vertical.
    crl_delta = 4.8308e-06 # Refractive index decrement (n = 1- delta - i*beta) @ 8.4 keV
    crl_attenuation_length  = 6.053e-3    # Attenuation length [m], Henke data.
    crl_shape = 1         # Parabolic lenses
    crl_aperture = 3.0e-3 # [m]
    crl_curvature_radius = 5.8e-3 # [m]
    crl_number_of_lenses = 19
    crl_wall_thickness = 8.0e-5 # Thickness
    crl_center_horizontal_coordinate = 0.0
    crl_center_vertical_coordinate = 0.0
    crl_initial_photon_energy = 8.48e3 # [eV]
    crl_final_photon_energy = 8.52e3 # [eV]

    crl = CRL( _foc_plane=crl_focussing_plane,
               _delta=crl_delta,
               _atten_len=crl_attenuation_length,
               _shape=crl_shape,
               _apert_h=crl_aperture,
               _apert_v=crl_aperture,
               _r_min=crl_curvature_radius,
               _n=crl_number_of_lenses,
               _wall_thick=crl_wall_thickness,
               _xc=crl_center_horizontal_coordinate,
               _yc=crl_center_vertical_coordinate,
               _void_cen_rad=None,
               _e_start=crl_initial_photon_energy,
               _e_fin=crl_final_photon_energy,
               )

    zoom = 0.6
    beamline.append( crl_front_aperture, Use_PP(semi_analytical_treatment=0, zoom=zoom, sampling=zoom/0.1) )
    beamline.append( crl, Use_PP(semi_analytical_treatment=0, zoom=1, sampling=1) )

    # Drift to focus aperture
    crl_to_exp_drift = Drift( src_to_exp - src_to_crl )
    beamline.append( crl_to_exp_drift, Use_PP(semi_analytical_treatment=1, zoom=1, sampling=1) )

    return beamline


def setup_S2E_SPI_beamline():
    """ Utility function that returns the S2E SPI beamline (Yoon et al. Scientific Reports (2016). """

    distance0 = 300.
    distance1 = 630.
    distance = distance0 + distance1
    f_hfm    = 3.0       # nominal focal length for HFM KB
    f_vfm    = 1.9       # nominal focal length for VFM KB
    distance_hfm_vfm = f_hfm - f_vfm
    distance_foc =  1. /(1./f_vfm + 1. / (distance + distance_hfm_vfm))
    theta_om = 3.5e-3 # offset mirrors incidence angle
    theta_kb = 3.5e-3 # KB mirrors incidence angle

    drift0 = wpg.optical_elements.Drift(distance0)
    drift1 = wpg.optical_elements.Drift(distance1)
    drift_in_kb = wpg.optical_elements.Drift(distance_hfm_vfm)
    drift_to_foc = wpg.optical_elements.Drift(distance_foc)

    om_mirror_length = 0.8; om_clear_ap = om_mirror_length*theta_om
    kb_mirror_length = 0.9; kb_clear_ap = kb_mirror_length*theta_kb
    ap0   = wpg.optical_elements.Aperture('r','a', 120.e-6, 120.e-6)
    ap1   = wpg.optical_elements.Aperture('r','a', om_clear_ap, 2*om_clear_ap)
    ap_kb = wpg.optical_elements.Aperture('r','a', kb_clear_ap, kb_clear_ap)
    hfm    = wpg.optical_elements.Mirror_elliptical(
                    orient='x',p=distance, q=(distance_hfm_vfm+distance_foc),
                    thetaE=theta_kb, theta0=theta_kb, length=0.9)
    vfm    = wpg.optical_elements.Mirror_elliptical(
                    orient='y',p=(distance+distance_hfm_vfm), q=distance_foc,
                    thetaE=theta_kb, theta0=theta_kb, length=0.9)
    wf_dist_om = wpg.optical_elements.WF_dist(1500, 100, om_clear_ap, 2*om_clear_ap)

    defineOPD(wf_dist_om, mirror_data2, 2, '\t', 'x', theta_kb, scale=2)

    wf_dist_hfm = wpg.optical_elements.WF_dist(1500, 100, kb_clear_ap, kb_clear_ap)
    defineOPD(wf_dist_hfm,  mirror_data1, 2, '\t', 'x', theta_kb, scale=2, stretching=kb_mirror_length/0.8)

    wf_dist_vfm = wpg.optical_elements.WF_dist(1100, 1500, kb_clear_ap, kb_clear_ap)
    defineOPD(wf_dist_vfm, mirror_data2, 2, ' ', 'y', theta_kb, scale=2, stretching=kb_mirror_length/0.8)


    bl0 = Beamline()
    bl0.append(ap0,   Use_PP(semi_analytical_treatment=0, zoom=14.4, sampling=1/1.6))
    bl0.append(drift0,Use_PP(semi_analytical_treatment=0))
    bl0.append(ap1,    Use_PP(zoom=0.8))   #bl0.append(ap1,    Use_PP(zoom=1.6, sampling=1/1.5))
    bl0.append(wf_dist_om, Use_PP())
    bl0.append(drift1, Use_PP(semi_analytical_treatment=1))
    bl0.append(ap_kb,  Use_PP(zoom = 6.4, sampling = 1/16.))#bl0.append(ap_kb,    Use_PP(zoom=5.4, sampling=1/6.4))
    bl0.append(hfm, Use_PP())
    bl0.append(wf_dist_hfm, Use_PP())
    bl0.append(drift_in_kb, Use_PP(semi_analytical_treatment=1))
    bl0.append(vfm, Use_PP())
    bl0.append(wf_dist_vfm, Use_PP())
    bl0.append(drift_to_foc, Use_PP(semi_analytical_treatment=1))

    return bl0

