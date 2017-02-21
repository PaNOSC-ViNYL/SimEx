'''
input deck for XFEL SASE3 beamline
'''
from ocelot.cpbd.elements import *
from ocelot.cpbd.beam import *
from ocelot.cpbd.magnetic_lattice import *
from ocelot.optics.elements import Crystal
from ocelot.optics.bragg import *
import numpy as np


und = Undulator (nperiods=124,lperiod=0.040,Kx=0.0, eid = "und")

d = Drift (l=1.0, eid = "d")

d1 = Drift (l=0.55, eid = "d1")
d2 = Drift (l=0.24, eid = "d2")
d3 = Drift (l=0.17+0.08, eid = "d0.05nm3")

b1 = RBend (l=0.0575, angle=0.0, eid = "b1")
b2 = RBend (l=0.0575, angle=-0.0, eid = "b2")

psu= Drift (l=b1.l*2 + b2.l*2 + d3.l, eid = "d1")

qf = Quadrupole (l=0.4, eid = "qf")
qd = Quadrupole (l=0.4, eid = "qd")
qfh = Quadrupole (l=qf.l / 2., k1=-1)#, id = "qfh")
qdh = Quadrupole (l=qd.l / 2., k1=-1)#, id = "qdh")

cell_ps = (und, d2, qf, psu, und, d2, qd, psu)

sase1 = (und, d2, qd, psu) + 17*cell_ps
def sase1_segment(n=0): return (und, d2, qd, psu) + n*cell_ps


# for matching
extra_fodo = (und, d2, qdh)
# l_fodo = qf.l / 2 + (b1.l + b2.l + b2.l + b1.l + d3.l) + und.l + d2.l + qf.l / 2 
l_fodo= MagneticLattice(cell_ps).totalLen/2
und_l=l_fodo

# sase1_cell = (und, d2, qf, psu, und)
#self-seeding
# chicane1 = Drift(l=5.1)
# chicane1.cryst = Crystal(r=[0,0,0*cm], size=[5*cm,5*cm,100*mum], no=[0,0,-1])
# chicane1.cryst.lattice =  CrystalLattice('C')
# chicane1.cryst.psi_n = -pi/2. #input angle psi_n according to Authier (symmetric reflection, Si)
# chicane1.cryst.ref_idx = (4,0,0)

# chicane2 = Drift(l=5.1)
# chicane2.cryst = Crystal(r=[0,0,0*cm], size=[5*cm,5*cm,100*mum], no=[0,0,-1])
# chicane2.cryst.lattice =  CrystalLattice('C')
# chicane2.cryst.psi_n = -pi/2. #input angle psi_n according to Authier (symmetric reflection, Si)
# chicane2.cryst.ref_idx = (4,0,0)

# m = 1.0
# cm = 1.e-2
# mm = 1.e-3
# mum = 1.e-6
'''
TODO: for future
geo = Geometry([cr1])
chicane.geo = geo
chicane.geo_transform = t
'''

# uncomment this for simplified SR calculation
## und = Undulator (nperiods=125*35,lperiod=0.040,Kx=1.9657, eid = "und")
## sase1=(und)


# example settings 28m beta, 0.05nm wavelength
und.Kx = 1.9657
qf.k1 = 0.7181242
qd.k1 = -0.7181242
qfh.k1 = 0.7181242
qdh.k1 = -0.7181242
b1.angle = 1.7926311e-5
b2.angle =-1.7926311e-5


# setting xxxnm wavelength
#und.Kx = 1.8

und.Kx = 2.395

beam = Beam()
beam.E = 14.0
beam.sigma_E = 0.002
beam.emit_xn = 1.36059e-7
beam.emit_yn = 2.40048e-7

beam.gamma_rel = beam.E / (0.511e-3)
beam.emit_x = beam.emit_xn / beam.gamma_rel
beam.emit_y = beam.emit_yn / beam.gamma_rel
beam.beta_x = 33.7
beam.beta_y = 23.218
beam.alpha_x = 1.219
beam.alpha_y = -0.842

beam.tpulse = 80    # electron bunch length in fs (rms)
beam.C = 1.0        # bunch charge (nC)
beam.I = 1.0e-9 * beam.C / ( np.sqrt(2*pi) * beam.tpulse * 1.e-15 ) 

#beam.emit = {0.02: [0.32e-6,0.32e-6], 0.1: [0.39e-6,0.39e-6], 0.25: [0.6e-6,0.6e-6], 0.5: [0.7e-6,0.7e-6], 1.0: [0.97e-6,0.97e-6]}
beam.emit = {0.02: [0.2e-6,0.18e-6], 0.1: [0.32e-6,0.27e-6], 0.25: [0.4e-6,0.36e-6], 0.5: [0.45e-6,0.42e-6], 1.0: [0.8e-6,0.84e-6]}

def f1(n, n0, a0, a1, a2):
    '''
    piecewise-quadratic tapering function
    '''
    for i in range(1,len(n0)):
        if n < n0[i]:
            return a0 + (n-n0[i-1])*a1[i-1] + (n-n0[i-1])**2 * a2[i-1]
        a0 += (n0[i]-n0[i-1])*a1[i-1] + (n0[i]-n0[i-1])**2 * a2[i-1]
    
    return 1.0

def f2(n, n0, a0, a1, a2):
    '''
    exponential tapering
    '''
    if n <= n0:
        return a0
    
    return a0 * (  1 + a1 * (n - n0)**a2 )



def get_taper_coeff(ebeam, ephoton):
    if ebeam == 14:
        if ephoton > 400 and ephoton < 1000:
            n0 = [0,6,25,35]
            a0 = 0.999
            a1 = [-0., -0.001,  -0.00 ]
            a2 = [0., -0.00012, -0.000 ]
            return n0, a0, a1, a2
        if ephoton >= 1000 and ephoton < 2000:
            n0 = [0,7, 25,35]
            a0 = 0.999
            a1 = [-0., -0.001,  -0.00 ]
            a2 = [0., -0.00012, -0.000 ]
            return n0, a0, a1, a2
        if ephoton >= 2000 and ephoton < 2999:
            n0 = [0,8, 25,35]
        #n0 = [0,10, 25,35] # 1nc
            a0 = 0.999
            a1 = [-0., -0.001,  -0.00 ]
            a2 = [0., -0.0001, -0.000 ]
        #a2 = [0., -0.00005, -0.000 ]
            return n0, a0, a1, a2
        if ephoton >= 2999:
            n0 = [0,10, 25,35]
        #n0 = [0,13, 25,35] # 1nc
            a0 = 0.999
            a1 = [-0., -0.001,  -0.00 ]
            a2 = [0., -0.0001, -0.000 ]
            return n0, a0, a1, a2

    if ebeam == 8.5:
        pass


