#!/usr/bin/env python

from wpg import Wavefront
from wpg.wpg_uti_wf import plot_t_wf,look_at_q_space
import numpy as np
import os
import pylab as plt
import sys

def show_diagnostics(FELsource_out_number):

      FELsource_out_file = FELsource_out_number

      if not os.path.exists(FELsource_out_file):
            print('Input file {} not found.'.format(FELsource_out_file))
            return

      wf = Wavefront()
      wf.load_hdf5(FELsource_out_file)

      plot_t_wf(wf)
      look_at_q_space(wf)
      # show two figures window 1: image of I(x,y) integral intensity, with real
      # x and y axis and title with file name
      J2eV = 6.24150934e18;
      mesh = wf.params.Mesh
      tmin = mesh.sliceMin;
      tmax = mesh.sliceMax;
      dt = (tmax - tmin) / (mesh.nSlices - 1);
      dx = (mesh.xMax - mesh.xMin) / (mesh.nx - 1);
      dy = (mesh.yMax - mesh.yMin) / (mesh.ny - 1);

      wf_intensity = wf.get_intensity(polarization='horizontal');
      total_intensity = wf_intensity.sum(axis=-1);
      data = total_intensity * dt
      plt.figure()
      plt.imshow(data*dx*dy*1e6*J2eV/wf.params.photonEnergy,extent=[mesh.xMin*1e6,mesh.xMax*1e6,mesh.yMin*1e6,mesh.yMax * 1e6], cmap="YlGnBu_r")
      title = 'Number of photons per %.2f x %.2f $\mu m ^2$ pixel'  %  (dx*1e6, dx*1e6)
      plt.title(title)
      plt.colorbar(); plt.xlabel('[$\mu m$]');

      # window 2: plot of 2 curves:
      #(1) history/parent/temporal_struct - FAST post-processing
      temporal_struct = wf.custom_fields['history']['parent']['misc']['temporal_struct']
      t0 = (temporal_struct[:, 0].max() + temporal_struct[:, 0].min()) / 2

      plt.figure()
      plt.plot(temporal_struct[:, 0] - t0, temporal_struct[:, 1] * 1e-9, 'b',label = 'output FAST-pp')
      plt.hold(True)
      #(2) integral intensity I(t) calculated for wavefront written in h5

      t = np.linspace(tmin, tmax, wf.params.Mesh.nSlices)
      pulse_energy = wf.get_intensity().sum(axis=0).sum(axis=0) #check it
      plt.plot(t * 1e15, pulse_energy*dx*dy*1e6*1e-9,'ro', label = 'wavefront data')

      title = 'FEL pulse energy %.2f %s ' % (pulse_energy.sum(axis=0) * dx * dy * 1e6 * dt * 1e3, 'mJ')
      plt.title(title)
      plt.xlabel('time [fs]');
      plt.ylabel('Instantaneous power [GW]');
      plt.legend()
      plt.grid(True)
      plt.show()

def main():
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option("--input-file", dest="in_fname", default="FELsource_out_0000001.h5",help="Input wavefront file: FELsource_out_***.h5")
	(options, args) = parser.parse_args()

	if not options.in_fname :   # if filename is not given
	    parser.error('Input filename not specified, use --input-file options')
	    return

	show_diagnostics(options.in_fname)

if __name__ == "__main__":
	main()
