#!/usr/bin/env python

import matplotlib
matplotlib.use('pdf')

from argparse import ArgumentParser
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D
from supp_py_modules import read_results
from supp_py_modules import rotateIntens
from supp_py_modules import viewRecon
import glob
import h5py
import numpy
import os
import time

def load_reference_intensites(ref_file):
    t_intens = (read_results.extract_value_from_h5(ref_file, "/data/data")).astype("float")
    intens_len = len(t_intens)
    qmax    = intens_len/2
    (q_low, q_high) = (15, int(0.9*qmax))
    qRange1 = numpy.arange(-q_high, q_high + 1)
    qRange2 = numpy.arange(-qmax, qmax + 1)
    qPos0   = numpy.array([[i,j,0] for i in qRange1 for j in qRange1 if numpy.sqrt(i*i+j*j) > q_low]).astype("float")
    qPos1   = numpy.array([[i,0,j] for i in qRange1 for j in qRange1 if numpy.sqrt(i*i+j*j) > q_low]).astype("float")
    qPos2   = numpy.array([[0,i,j] for i in qRange1 for j in qRange1 if numpy.sqrt(i*i+j*j) > q_low]).astype("float")
    qPos    = numpy.concatenate((qPos0, qPos1, qPos2))
    qPos_full = numpy.array([[i,j,k] for i in qRange2 for j in qRange2 for k in qRange2]).astype("float")
    return (qmax, t_intens, intens_len, qPos, qPos_full)

def load_quaternions(quat_fn):
    return (numpy.fromfile(quat_fn, sep=" ")[1:]).reshape(-1,5).astype("float")

def zero_neg(x):
    return 0. if x<=0. else x
v_zero_neg  = numpy.vectorize(zero_neg)

def find_two_means(vals, v0, v1):
    v0_t    = 0.
    v0_t_n  = 0.
    v1_t    = 0.
    v1_t_n  = 0.
    for vv in vals:
        if (numpy.abs(vv-v0) > abs(vv-v1)):
            v1_t    += vv
            v1_t_n  += 1.
        else:
            v0_t    += vv
            v0_t_n  += 1.
    return (v0_t/v0_t_n, v1_t/v1_t_n)

def cluster_two_means(vals):
    (v0,v1)     = (0.,0.1)
    (v00, v11)  = find_two_means(vals, v0, v1)
    err = 0.5*(numpy.abs(v00-v0)+numpy.abs(v11-v1))
    while(err > 1.E-5):
        (v00, v11)  = find_two_means(vals, v0, v1)
        err         = 0.5*(numpy.abs(v00-v0)+numpy.abs(v11-v1))
        (v0, v1)    = (v00, v11)
    return (v0, v1)

def support_from_autocorr(auto, qmax, thr_0, thr_1, kl=1, write=True):
    pos     = numpy.argwhere(numpy.abs(auto-thr_0) > numpy.abs(auto-thr_1))
    pos_set = set()
    pos_list= []
    kerl    = range(-kl,kl+1)
    ker     = [[i,j,k] for i in kerl for j in kerl for k in kerl]

    def trun(v):
        return int(numpy.ceil(0.5*v))
    v_trun = numpy.vectorize(trun)

    for (pi, pj, pk) in pos:
        for (ci, cj, ck) in ker:
            pos_set.add((pi+ci, pj+cj, pk+ck))
    for s in pos_set:
        pos_list.append([s[0], s[1], s[2]])

    pos_array = numpy.array(pos_list)
    pos_array -= [a.min() for a in pos_array.transpose()]
    pos_array = numpy.array([v_trun(a) for a in pos_array])

    if write:
        fp  = open("support.dat", "w")
        fp.write("%d %d\n"%(qmax, len(pos_array)))
        for p in pos_array:
            fp.write("%d %d %d\n" % (p[0], p[1], p[2]))
        fp.close()

    return pos_array

def show_support(support):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    (x,y,z) = support.transpose()
    ax.scatter(x, y, z, c='r', marker='s')
    plt.show()

################################################################################
# Options for running this program
################################################################################

def do_analysis(args):
    # Scan directories for reconstructions that were done.
    # Reference directory is the zeroth (or first) one.
    dirs        = glob.glob(args.input_directory+"/")
    cwd         = os.getcwd()
    curr_dir    = dirs[0]
    curr_file   = glob.glob(os.path.join(curr_dir, args.tmp_fn))[0]
    print "Will read default parameters from reconstruction in " + curr_file

    (qmax, t_intens, intens_len, qPos, qPos_full) = load_reference_intensites(curr_file)
    quats       = load_quaternions(os.path.join(curr_dir, "quaternion.dat"))

    num_dirs        = len(dirs)
    intens_stack    = numpy.zeros((num_dirs, intens_len, intens_len, intens_len))
    intens_stack[0] = t_intens.copy()
    dir_ct          = 1
    i_off           = 1.E-7
    tt_intens       = (t_intens>0.)*t_intens
    tt_intens       /= tt_intens.max()
    tt_intens       = numpy.abs(numpy.log(tt_intens+i_off))

    if num_dirs > 1:
        for dir_ct in range(num_dirs):
            dir         = dirs[dir_ct]
            t0          = time.time()
            curr_file   = glob.glob(os.path.join(dir, args.tmp_fn))[0]
            c_intens    = (read_results.extract_value_from_h5(curr_file, "/data/data")).astype("float")
            cc_intens   = (c_intens>0.)*c_intens
            cc_intens   /= cc_intens.max()
            cc_intens   = numpy.abs(numpy.log(cc_intens+i_off))
            scores      = rotateIntens.orient_two_intensities(tt_intens.ravel(), cc_intens.ravel(), qPos.ravel(), quats.ravel(), intens_len)
            ml_quat     = quats[(scores.argsort())[0]]
            out_intens  = numpy.zeros_like(cc_intens)
            rotateIntens.interp_intensities(c_intens.ravel(), out_intens.ravel(), qPos_full.ravel(), ml_quat, intens_len)
            t1          = time.time()
            intens_stack[dir_ct] = out_intens.copy()
            print "Done orienting intensity %d of %d. Took %lf s."%(dir_ct, num_dirs, t1-t0)

    # Save stack.
    h5 = h5py.File("3d_stack.h5", "w")
    h5.create_group("data")
    h5.create_dataset("data/oriented_diffraction_volumes", data=intens_stack )
    h5.close()
    # Make diagnostic images from individual reconstructions
    # only if make_diag_imgs option is true
    if args.make_diag_imgs:
        for dir in dirs:
            os.chdir(dir)
            tmp_file = glob.glob(args.tmp_fn)[0]
            print tmp_file
            print "="*80
            print "Making images for %s "%dir + "."*20
            try:
                viewRecon.make_panel_of_intensity_slices(tmp_file, c_n=16)
            except:
                print "Making of intensity slices failed!"
            viewRecon.make_error_time_plot(tmp_file)
            try:
                viewRecon.make_mutual_info_plot(tmp_file)
            except:
                print "Making of mutual information plot failed!"
            print "="*80
            os.chdir(cwd)

        tarBallName = (os.getcwd().split('/')[-1])+".tgz"
        os.system("tar -czf  %s  "%tarBallName + ''.join([s+"*.pdf " for s in dirs]))
        print "Images saved in %s" % tarBallName

    # Make images from merging individual reconstructions
    # only if merge_imgs option is true
    if args.merge_imgs:
        (rows, cols)= (3, max([2,num_dirs/3+1]))
        matplotlib.rcParams.update({'font.size': 13})
        fig, ax     = plt.subplots(rows, cols, sharex=True, sharey=True, figsize=(2.5*cols, 2.5*rows))
        fig.subplots_adjust(wspace=0.01)
        stack_ct    = 0
        for r in range(rows):
            for c in range(cols):
                if stack_ct >= num_dirs:
                    break
                out_intens  = intens_stack[stack_ct]
                im          = ax[r, c].imshow(numpy.log(numpy.abs(out_intens[qmax])+1.E-7), cmap=plt.cm.coolwarm, aspect='auto')
                plt.draw()
                stack_ct    += 1

        cbar_ax         = fig.add_axes([0.9, 0.1, 0.025, 0.8])
        fig.colorbar(im, cax=cbar_ax, label="log10(intensities)")
        (shx, shy)      = t_intens[qmax].shape
        (h_shx, h_shy)  = (shx/2, shy/2)
        xt              = numpy.linspace(0.5*h_shx, shx-.5*h_shx-1, 3).astype('int')
        xt_l            = numpy.linspace(-0.5*h_shx, 0.5*h_shx, 3).astype('int')
        yt              = numpy.linspace(0, shy-1, 3).astype('int')
        yt_l            = numpy.linspace(-1*h_shy, h_shy, 3).astype('int')
        plt.setp(ax, xticks=xt, xticklabels=xt_l, yticks=yt, yticklabels=yt_l)
        img_name        = "slices.pdf"
        plt.savefig(img_name, bbox_inches='tight')
        plt.close(fig)

        fig2, ax2       = plt.subplots(1, 1)
        im              = ax2.imshow(numpy.log(numpy.abs((numpy.median(intens_stack, axis=0))[qmax])+1.E-7))
        fig2.subplots_adjust(wspace=0.01)
        cbar_ax2        = fig2.add_axes([0.9, 0.1, 0.025, 0.8])
        fig2.colorbar(im, cax=cbar_ax2, label="log10(intensities)")
        plt.setp(ax2, xticks=xt, xticklabels=xt_l, yticks=yt, yticklabels=yt_l)
        img_name        = "merged.pdf"
        plt.savefig(img_name, bbox_inches='tight')
        plt.close(fig2)

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("input_directory",
                        metavar="input_directory",
                        help="Wildcard expression for directories to scan for input files.")
    parser.add_argument("-d",
                        "--diagnostic_imgs",
                        action="store_true",
                        dest="make_diag_imgs",
                        default=True,
                        help="create images from intermediate files")
    parser.add_argument("-m",
                        "--merge_imgs",
                        action="store_true",
                        dest="merge_imgs",
                        default=True,
                        help="create images from merging intensities")
    parser.add_argument("-f",
                        "--file_name",
                        dest="tmp_fn",
                        default="orient*.h5",
                        help="name of temporary file from EMC recon")

    args = parser.parse_args()

    do_analysis(args)

