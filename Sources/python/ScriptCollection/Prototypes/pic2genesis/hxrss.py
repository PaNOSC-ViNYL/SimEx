'''
hard x-ray self-seeding
launch as python3 hxrss.py
'''

import sys, os
sys.path.insert(0, '/home/grotec/Codes')
import matplotlib.pyplot as plt
from ocelot.gui.accelerator import *
from ocelot.utils import xfel_utils
from ocelot.utils.xfel_utils import *
from ocelot.cpbd.magnetic_lattice import MagneticLattice
from ocelot.gui.genesis_plot import *
import time
from ocelot.common.globals import *  #import of constants like "h_eV_s" and "speed_of_light"
from ocelot.rad.undulator_params import *

param_dir = os.path.join( os.getcwd(), 'parameters' )
from parameters.sase1.sase1 import * #import sase1 undulator parameters

##################################################
###########                            ###########
###########         BEGIN OF           ###########
###########  USER-DEFINED QUANTITIES   ###########
###########                            ###########
##################################################

debug = 1 #show plots and write info in console
savefig = 0 #save figures to project directory

# exp_dir = '/gpfs/exfel/data/scratch/svitozar/projects/ocelot_test/Shan/Replica_2_cut_noquantum/' #directory where the output will be stored
exp_dir = os.path.join( os.getcwd(), 'exp')

beam_fileName = os.path.join( param_dir , 'beams', 'non-nominal', 'beam_0.02nC_wake.txt') #path to beam file
#dist_fileName = os.path.join( param_dir , 'beams', 'non-nominal', '0.5nC_8.5GeV_slotted_2um_Feng_collim_core.dist') #path to dist file
dist_fileName = 'beam.dist'

# Beam and photon parameters.
beta_av = 25.0 # beta function for the ebeam in undulator
E_beam = 2.0   # Electon beam energy (e.g.14.4) [GeV]
E_photon   = 800.0   # FEL Resonance photon energy e.g. 8000.0 [eV]

# Range of statistical runs to execute, from 0 to n-1 - (0,n)
#run_ids = range(1,11)
run_ids = [1]
# Simulation stages to execute
start_stage = 0
#stop_stage = 6
stop_stage = 1

# Length of undulator cells for stages 1,3,5
N1 = 7
N3 = 7
N5 = 10
# 5-th stage tapering:
n0 = [0,20,60]
a1 = [0.0, -0.000]
a2 = [0.0, -0.000]


# Genesis simulation parameters
npart = 8192 # number of macroparticles in Genesis
ncar =101 # genesis transverse mesh size
dgrid = 2e-4 # genesis transverse mesh half-length
# dgrid = 0 # genesis transverse mesh half-length
ncar5= 101#201 # -|-  for stage 5 (due to tapering beneficial to increase the mesh size)
dgrid5= 2e-4 #4e-4 # -|-  for stage 5 (due to tapering beneficial to increase the mesh size)
zsep=30 #z-separation between slices in radaition wavelengths (if 0 - then calculated based of beam peak current parameters)


#####################################################
###########                            ##############
###########         END OF             ##############
###########  USER-DEFINED QUANTITIES   ##############
###########                            ##############
#####################################################


t0 = time.time()

launcher = get_genesis_launcher()

create_exp_dir(exp_dir, run_ids) # creates experimental directory with 'run_# subdirectories
#copy_this_script(os.path.basename(__file__),os.path.realpath(__file__),exp_dir) # write copy of this script to the exp_dir

# read and prepare beam file
beam = read_beam_file(beam_fileName)
# beam.ex*=1.2
# beam.ey*=1.2
beam = cut_beam(beam,[-4e-6, 1e-6])
# beam=set_beam_energy(beam, E_beam)
beam_pk=get_beam_peak(beam) #another object containing beam parameters at peak current position, get_beam_s() gets parameters at given position s
#beam=zero_wake_at_ipk(beam)

lat = MagneticLattice(sase1_segment(n=20))
und_l=l_fodo # undulator cell length
# lat,beam_pk=lat_beam_rematch(lat,beam_pk,beta_av) tbd
rematch(beta_av, l_fodo, qdh, lat, extra_fodo, beam_pk, qf, qd) # jeez...
#beam =transform_beam_twiss(beam,transform=[ [beam_pk.beta_x,beam_pk.alpha_x], [beam_pk.beta_y,beam_pk.alpha_y] ])
#plot_beam(beam,showfig=0,savefig=0)

#if debug:
    #tw0 = Twiss(beam_pk)
    #tws=twiss(lat, tw0, nPoints = 100) # to make sure the average beta exists, show twiss if needed

und.Kx = Ephoton2K(E_photon, und.lperiod, E_beam)
# calculate UR parameters (required later for input generation)
up = UndulatorParameters(und,E_beam)

if debug: up.printParameters()

a0 = und.Kx
taper_func_5 = lambda n : f1(n, n0, a0, a1, a2 )

lat1 = deepcopy(lat)
#lat3 = cut_lattice(lat1,N1)
#lat5 = cut_lattice(lat3,N3)
#lat5 = taper(lat5, taper_func_5)

# possibility to override the automatic zsep calculations (based on rho)
if zsep==0:
    zsep = generate_input(up, beam_pk, itdp=True).zsep


#################
stage=1  #(SASE)#
#################

if start_stage <= stage and stop_stage >= stage:
    print ('Start STAGE ' + str(stage))
    for run_id in run_ids:
        inp = generate_input(up, beam_pk, itdp=True)
        inp.stageid=stage
        inp.runid = run_id
        inp.run_dir = exp_dir+'run_'+str(run_id)
        # inp.ipseed = 6123*(run_id + 1)
        inp.ipseed = 26 + run_id*200

        inp.lat=lat1
        inp.lattice_str = generate_lattice(lattice=lat1, energy=E_beam)
#def generate_lattice(lattice, unit=1.0, energy = None, debug = False):
        inp.beam=beam

        inp.iphsty = 2 # Generate output in the main output file at each IPHSTYth integration step. To disable output set IPHSTY to zero.
        inp.ishsty = 1 # Generate output in the main output file for each ISHSTYth slice.

        inp.isravg = 0 #we assume it is compensated by proper tapering on top of ours
        inp.isrsig = 1 #use it wisely, due to causality problems (affects initial parameters?)
        inp.ncar = ncar
        inp.zstop = und_l*N1
        # inp.zstop = 42.56
        inp.dgrid = dgrid
        inp.zsep=zsep
        inp.npart=npart
        inp.idmppar = 1
        inp.idmpfld = 1

        #test!
        inp.delz=2
        inp.nslice=0
        # inp.gamma0=30000
        # inp.fbess0=0.810854
        # inp.xlamds=8.265645E-11
        #
        print(inp.fbess0)

        out = xfel_utils.run(inp, launcher, readout=0)

        if savefig:
            background('''plot_gen_out_all("'''+out.filePath+'''",savefig='png',choice=(1,1,1,1,6.14,1,0,0,0,1,0),showfig=False)''')


