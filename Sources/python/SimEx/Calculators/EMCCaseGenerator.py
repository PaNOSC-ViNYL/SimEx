##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 Carsten Fortmann-Grote                         #
# Based on simS2E script provided by N.-D. Loh.                          #
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

import h5py
import numpy
import os
import sys
import time

def _print_to_log(msg, log_file=None):
    if not os.path.exists(log_file):
        fp = open(log_file, "w")
    else:
        fp = open(log_file, "a")
    t_msg = time.asctime() + ":: " + msg
    fp.write(t_msg)
    fp.write("\n")
    fp.close()

    print msg
    sys.stdout.flush()

def _create_directory(dir_name, logging=True, log_file=None, err_msg=""):
    if os.path.exists(dir_name):
        if logging:
            _print_to_log(dir_name + " exists! " + err_msg, log_file=log_file)
        else:
            print dir_name + " exists! "
    else:
        os.makedirs(dir_name)
        if logging:
            _print_to_log("Creating " + dir_name, log_file=log_file)
        else:
            print "Creating " + dir_name

def load_intensities(ref_file):

    with h5py.File(ref_file, 'r') as fp:
        data_format_version = (fp["version"].value()).astype("float")
        if data_format_version < 0.2:
            t_intens = (fp["data/data"].value()).astype("float")

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

            fp.close()
            return (qmax, t_intens, intens_len, qPos, qPos_full)

        else: # for data format version >= 0.2
            t_intens = []
            tasks_in_file = fp.keys()
            for task in tasks_in_file["data"]:
                t_intens.append( (fp["data"][key]["data"].value()).astype("float") )

            t_intens = numpy.array(t_intens)
            intens_len = t_intens.shape[1]
            qmax    = intens_len/2
            (q_low, q_high) = (15, int(0.9*qmax))
            qRange1 = numpy.arange(-q_high, q_high + 1)
            qRange2 = numpy.arange(-qmax, qmax + 1)
            qPos0   = numpy.array([[i,j,0] for i in qRange1 for j in qRange1 if numpy.sqrt(i*i+j*j) > q_low]).astype("float")
            qPos1   = numpy.array([[i,0,j] for i in qRange1 for j in qRange1 if numpy.sqrt(i*i+j*j) > q_low]).astype("float")
            qPos2   = numpy.array([[0,i,j] for i in qRange1 for j in qRange1 if numpy.sqrt(i*i+j*j) > q_low]).astype("float")
            qPos    = numpy.concatenate((qPos0, qPos1, qPos2))
            qPos_full = numpy.array([[i,j,k] for i in qRange2 for j in qRange2 for k in qRange2]).astype("float")

            fp.close()
            return (qmax, t_intens, intens_len, qPos, qPos_full)

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


###############################################################
# Convert photons into sparse format, split into multiple files
# Create detector.dat, creation of beamstop
# Test data is in: /data/S2E/data/simulation_test/diffr
###############################################################

class EMCCaseGenerator(object):
    """ Class that represents an EMC case. """
    def __init__(self, runLog=None):
        """
        Wrapper for initializing the essential data for EMC recon.

        :param runLog: Flag that indicates where to save the runtime log.
        :type runLog: str, default None (don't save log.)"

        """
        #Initialize essential parameters
        self.z = 0
        self.sigma = 0
        self.qmax = 0
        self.qmin = 0
        self.numPixToEdge = 0
        self.detectorDist = 0
        self.maxScatteringAng = 0
        self.detector = None
        self.beamstop = None
        self.intensities = None
        self.runLog = runLog

        #Initialize non-essential parameters
        self.density = []
        self.support = []
        self.supportPositions = []

    def writeDetectorToFile(self, filename="detector.dat"):
        """
        Writes computed detector and beamstop coordinates to output.

        :param filename: Path of file where to write the detector data.
        :type filename: str
        """

        _print_to_log("Writing detector to %s"%(filename), log_file=self.runLog)
        header = "%d\t%d\t%d\n" % (numpy.ceil(self.qmax), len(self.detector), len(self.beamstop))
        f = open(filename, 'w')
        f.write(header)
        for i in self.detector:
            text = "%e\t%e\t%e\n" % (i[0], i[1], i[2])
            f.write(text)
        for i in self.beamstop:
            text = "%d\t%d\t%d\n" % (i[0], i[1], i[2])
            f.write(text)
        f.close()

    def placePixel(self, ii, jj, zL):
        """
        Gives (qx,qy,qz) position of pixels on Ewald sphere when given as input
        the (x,y,z)=(ii,jj,zL) position of pixel in the diffraction laboratory.
        The latter is measured in terms of the size of each realspace pixel.

        :param ii: Pixel index in x direction
        :type ii: int

        :param jj: Pixel index in y direction
        :type jj: int

        :param zL: Distance of pixel from detector in units of detector size.
        :type zL: float
        """

        v = numpy.array([ii,jj,zL])
        vDenom = numpy.sqrt(1 + (ii*ii + jj*jj)/(zL*zL))

        return v/vDenom - numpy.array([0,0,zL])

    def readGeomFromPhotonData(self, fn,thisProcess):
        """
        Extract detector geometry from S2E photon files.

        :param fn: Path to file to read.
        :type fn: str
        """
        if thisProcess==0:
            _print_to_log("Reading geometry file using file %s"%fn, log_file=self.runLog)
        f = h5py.File(fn, 'r')
        self.detectorDist = (f["params/geom/detectorDist"].value)

        #We expect the detector to always be square of length 2*self.numPixToEdge+1
        (r,c) = f["params/geom/mask"].shape
        if (r == c and (r%2==1)):
            self.numPixToEdge = (r-1)/2
        else:
            msg = "Your array has shape %d %d, Only odd-length square detectors allowed now. Quitting"%(r,c)
            _print_to_log(msg, log_file=self.runLog)
            sys.exit()

        pixH = (f['params/geom/pixelHeight'].value)
        pixW = (f['params/geom/pixelWidth'].value)
        if(pixH == pixW):
            self.pixSize = pixH
        maxScattAng = numpy.arctan(self.numPixToEdge * self.pixSize / self.detectorDist)
        zL = self.detectorDist / self.pixSize
        self.qmax = int(2 * self.numPixToEdge * numpy.sin(0.5*maxScattAng) / numpy.tan(maxScattAng))

        #Write detector to file
        [x,y] = numpy.mgrid[-self.numPixToEdge:self.numPixToEdge+1, -self.numPixToEdge:self.numPixToEdge+1]
        tempDetectorPix = [self.placePixel(i,j,zL) for i,j in zip(x.flat, y.flat)]
        qualifiedDetectorPix = [i for i in tempDetectorPix if (numpy.sqrt(i[0]*i[0] +i[1]*i[1] + i[2]*i[2])>self.qmin and numpy.sqrt(i[0]*i[0] +i[1]*i[1] + i[2]*i[2])<self.qmax and numpy.abs(i[0])>3)]
        self.detector = numpy.array(qualifiedDetectorPix)

        # qmin defaults to 2 pixel beamstop
        self.qmin = 2
        fQmin = numpy.floor(self.qmin)
        [x,y,z] = numpy.mgrid[-fQmin:fQmin+1, -fQmin:fQmin+1, -fQmin:fQmin+1]
        self.beamstop = numpy.array([[xx,yy,zz] for xx,yy,zz in zip(x.flat, y.flat, z.flat) if numpy.sqrt(xx*xx + yy*yy + zz*zz)<=self.qmin])

    def readGeomFromDetectorFile(self, fn="detector.dat"):
        """
        Read qx,qy,qz coordinates of detector and beamstop from detector.dat.
        """
        with open(fn, "r") as f:
            line1 = [int(x) for x in f.readline().split("\t")]
            self.qmax = int(line1[0])
            self.qmin = 2

            d = f.readlines()
        f.close()

        dLoc = [[float(y) for y in x.split("\t")] for x in d]
        self.detector = numpy.array(dLoc[:line1[1]])
        self.beamstop = numpy.array(dLoc[line1[1]:])

        return

    def writeSparsePhotonFile(self, fileList, outFN, outFNH5Avg,thisProcess,numProcesses):
        """
        Convert dense S2E file format to sparse EMC photons.dat format.

        :param fileList: List of files to convert into one sparse photon file.
        :type fileList: List ot str.

        :param outFN: Filename of sparse photon file.
        :type outFN: str, default 'photons.dat'

        :param outFNH5Avg: Filename for averaged photon file.
        :type outFNH5Avg: str
        """

        # Check if we deal with v0.2 file.
        if len(fileList) == 1 and h5py.File(fileList[0], 'r')['version'].value == 0.2:
            if thisProcess==0:
                self._writeSparsePhotonFileFromSingleH5(fileList[0], outFN, outFNH5Avg)
            return

        # Log: destination output to file
        if thisProcess==0:
            msg = "Writing diffr output to %s"%os.path.dirname(outFN)
            _print_to_log(msg, log_file=self.runLog)

        # Define in-plane detector x,y coordinates
        [x,y] = numpy.mgrid[-self.numPixToEdge:self.numPixToEdge+1, -self.numPixToEdge:self.numPixToEdge+1]

        # Compute qx,qy,qz positions of detector
        zL = self.detectorDist / self.pixSize
        tmpQ = numpy.array([self.placePixel(i,j,zL) for i,j in zip(x.flat, y.flat)])

        # Enumerate qualified detector pixels with a running index, currPos
        pos = -1 + 0*x.flatten()
        currPos = 0
        flatMask = 0.*pos
        for p,v in enumerate(tmpQ):
            if numpy.sqrt(v[0]*v[0] +v[1]*v[1] + v[2]*v[2])<self.qmax and numpy.sqrt(v[0]*v[0] +v[1]*v[1] + v[2]*v[2])>self.qmin and numpy.abs(v[0])>3:
                    pos[p] = currPos
                    flatMask[p] = 1.
                    currPos += 1

        outf = open(outFN, "w")
        if thisProcess==0:
            # Compute mean photon count.
            meanPhoton = 0.
            totPhoton = 0.
            count=0 # counts the processed images. Loop breaks if count goes above 200.
            for fn in fileList:
                f = h5py.File(fn, 'r')
                data_format_version = (f["version"].value).astype("float")
                if data_format_version < 0.2:
                    meanPhoton += numpy.mean((f["data/data"].value).flatten())
                    totPhoton += numpy.sum((f["data/data"].value).flatten())
                    f.close()
                    count +=1
                else:
                    tasks = f["data"].keys()
                    for task in tasks:
                        meanPhoton += numpy.mean((f["data"][task]["data"].value).flatten())
                        totPhoton += numpy.sum((f["data"][task]["data"].value).flatten())
                        count += 1
                    f.close()
                if count >= 200:
                    break
            meanPhoton /= 1.*count
            totPhoton /= 1.*count

            print "Found %f mean and %f total photons on average." % (meanPhoton, totPhoton)

            # Start stepping through diffraction images and writing them to sparse format
            msg = "Average intensities: %lf"%(totPhoton)
            _print_to_log(msg, log_file=self.runLog)
            outf.write("%d %lf \n"%(len(fileList), meanPhoton))


        mask = flatMask.reshape(2*self.numPixToEdge+1, -1)
        avg = 0.*mask

        if thisProcess==0:
            msg = "Converting individual data frames to sparse format %s"%("."*20)
            _print_to_log(msg, log_file=self.runLog)

        for n,fn in enumerate(fileList):
            if n % numProcesses != thisProcess:
                continue
            #try:
            if True:
                f = h5py.File(fn, 'r')
                data_format_version = (f["version"].value).astype("float")
                if data_format_version < 0.2:
                    v = f["data/data"].value
                    avg += v
                    temp = {"o":[], "m":[]}

                    for p,vv in zip(pos, v.flat):
                        # Todo: remove this
                        vv = int(vv)
                        if (p < 0) or (vv==0):
                            pass
                        else:
                            if vv == 1:
                                temp["o"].append(p)
                            if vv > 1:
                                temp["m"].append([p,vv])

                    [num_o, num_m] = [len(temp["o"]), len(temp["m"])]
                    strNumO = str(num_o)
                    ssO = ' '.join([str(i) for i in temp["o"]])
                    strNumM = str(num_m)
                    ssM = ' '.join(["%d %d "%(i[0], i[1]) for i in temp["m"]])
                    outf.write(' '.join([strNumO, ssO, strNumM, ssM]) + "\n")
                    f.close()

                else:
                    tasks = f["data"].keys()
                    for task in tasks:
                        v = f["data"][task]["data"].value
#                        print "In %s/%s/data, found max. %f and avg %f photons." % (fn, task, v.max(), v.mean())
                        avg += v
                        temp = {"o":[], "m":[]}

                        for p,vv in zip(pos, v.flat):
                            # Todo: remove this
                            vv = int(vv)
                            if (p < 0) or (vv==0):
                                pass
                            else:
                                if vv == 1:
                                    temp["o"].append(p)
                                if vv > 1:
                                    temp["m"].append([p,vv])

                        [num_o, num_m] = [len(temp["o"]), len(temp["m"])]
                        strNumO = str(num_o)
                        ssO = ' '.join([str(i) for i in temp["o"]])
                        strNumM = str(num_m)
                        ssM = ' '.join(["%d %d "%(i[0], i[1]) for i in temp["m"]])
                        outf.write(' '.join([strNumO, ssO, strNumM, ssM]) + "\n")
                    f.close()

            #except:
            else:
                msg = "Failed to read file #%d %s." % (n, fn)
                _print_to_log(msg, log_file=self.runLog)

            if n%10 == 0:
                msg = "Translated %d patterns"%n
                _print_to_log(msg, log_file=self.runLog)

        outf.close()

        # Write average photon and mask patterns to file
        outh5 = h5py.File(outFNH5Avg, 'w')
        outh5.create_dataset("average", data=avg, compression="gzip", compression_opts=9)
        if thisProcess==0:
            outh5.create_dataset("mask", data=mask, compression="gzip", compression_opts=9)
        outh5.close()

    def _writeSparsePhotonFileFromSingleH5(self, dense_file, outFN, outFNH5Avg):
        """
        Convert dense S2E file format to sparse EMC photons.dat format.

        :param dense_file: List of files to convert into one sparse photon file.
        :type dense_file: List ot str.

        :param outFN: Filename of sparse photon file.
        :type outFN: str, default 'photons.dat'

        :param outFNH5Avg: Filename for averaged photon file.
        :type outFNH5Avg: str
        """

        # Log: destination output to file
        msg = "Writing diffr output to %s"%outFN
        _print_to_log(msg, log_file=self.runLog)

        # Define in-plane detector x,y coordinates
        [x,y] = numpy.mgrid[-self.numPixToEdge:self.numPixToEdge+1, -self.numPixToEdge:self.numPixToEdge+1]

        # Compute qx,qy,qz positions of detector
        zL = self.detectorDist / self.pixSize
        tmpQ = numpy.array([self.placePixel(i,j,zL) for i,j in zip(x.flat, y.flat)])

        # Enumerate qualified detector pixels with a running index, currPos
        pos = -1 + 0*x.flatten()
        currPos = 0
        flatMask = 0.*pos
        for p,v in enumerate(tmpQ):
            if numpy.sqrt(v[0]*v[0] +v[1]*v[1] + v[2]*v[2])<self.qmax and numpy.sqrt(v[0]*v[0] +v[1]*v[1] + v[2]*v[2])>self.qmin and numpy.abs(v[0])>3:
                    pos[p] = currPos
                    flatMask[p] = 1.
                    currPos += 1

        # Compute mean photon count from the first 200 diffraction images
        # (or total number of images, whichever is smaller)
        # Open dense file.
        h5_dense = h5py.File( dense_file, 'r')
        number_of_patterns = len(h5_dense.keys()) - 3
        numFilesToAvgForMeanCount = min([200, number_of_patterns])
        meanPhoton = 0.
        totPhoton = 0.

        # Open dense file.
        h5_dense = h5py.File( dense_file, 'r')
        excluded_keys = ["version", "params", "info"]
        all_keys = h5_dense.keys()
        relevant_keys = [k for k in all_keys if not k in excluded_keys]
        relevant_keys.sort()
        for fn in relevant_keys[:numFilesToAvgForMeanCount]:
            f = h5_dense[fn]
            meanPhoton += numpy.mean((f["data/data"].value).flatten())
            totPhoton += numpy.sum((f["data/data"].value).flatten())

        meanPhoton /= 1.*numFilesToAvgForMeanCount
        totPhoton /= 1.*numFilesToAvgForMeanCount

        # Start stepping through diffraction images and writing them to sparse format
        msg = "Average intensities: %lf"%(totPhoton)
        _print_to_log(msg, log_file=self.runLog)
        outf = open(outFN, "w")
        outf.write("%d %lf \n"%(number_of_patterns, meanPhoton))
        mask = flatMask.reshape(2*self.numPixToEdge+1, -1)
        avg = 0.*mask

        msg = "Converting individual data frames to sparse format %s"%("."*20)
        _print_to_log(msg, log_file=self.runLog)

        for n,fn in enumerate(h5_dense.keys()):
            try:
                f = h5_dense[fn]
                v = f["data/data"].value
                avg += v
                temp = {"o":[], "m":[]}

                for p,vv in zip(pos, v.flat):
                    # Todo: remove this
                    vv = int(vv)
                    if (p < 0) or (vv==0):
                        pass
                    else:
                        if vv == 1:
                            temp["o"].append(p)
                        if vv > 1:
                            temp["m"].append([p,vv])

                [num_o, num_m] = [len(temp["o"]), len(temp["m"])]
                strNumO = str(num_o)
                ssO = ' '.join([str(i) for i in temp["o"]])
                strNumM = str(num_m)
                ssM = ' '.join(["%d %d "%(i[0], i[1]) for i in temp["m"]])
                outf.write(' '.join([strNumO, ssO, strNumM, ssM]) + "\n")
            except:
                msg = "Failed to read pattern #%d %s." % (n, fn)
                _print_to_log(msg, log_file=self.runLog)

            if n%10 == 0:
                msg = "Translated %d patterns"%n
                _print_to_log(msg, log_file=self.runLog)

        h5_dense.close()
        outf.close()

        # Write average photon and mask patterns to file
        outh5 = h5py.File(outFNH5Avg, 'w')
        outh5.create_dataset("average", data=avg, compression="gzip", compression_opts=9)
        outh5.create_dataset("mask", data=mask, compression="gzip", compression_opts=9)
        outh5.close()


    def showDetector(self):
        """
        Shows detector pixels as points on scatter plot; could be slow for large detectors.
        """
        # Commented out to avoid poping up of plots during calculation.
        pass
        #if self.detector is not None:
            #fig = plt.figure()
            #ax = fig.add_subplot(111, projection='3d')
            #ax.scatter(self.detector[:,0], self.detector[:,1], self.detector[:,2], c='r', marker='s')
            #ax.set_zlim3d(-self.qmax, self.qmax)
            #plt.show()
        #else:
            #msg = "Detector not initiated."
            #_print_to_log(msg, log_file=self.runLog)

    # The following functions have not been tested. Use with caution!!!


    def makeTestParticleAndSupport(self, inParticleRadius=5.9, inDamping=1.5, inFrac=0.5, inPad=1.8):
        """
        Recipe for creating random, "low-passed-filtered binary" contrast by
        alternating binary projection and low-pass-filter on an random, 3D array of numbers.

        Variables defined here:
        support             =   sphereical particle support (whose radius is less than particleRadius given),
        density             =   3D particle contrast,
        supportPositions    =   voxel position of support used in phasing.
        """
        self.particleRadius = inParticleRadius
        self.damping = inDamping
        self.frac = inFrac
        self.pad = inPad

        self.radius = int(numpy.floor(self.particleRadius) + numpy.floor(self.pad))
        self.size = 2*self.radius + 1
        [x,y,z] = numpy.mgrid[-self.radius:self.radius+1, -self.radius:self.radius+1, -self.radius:self.radius+1]
        self.support = numpy.sqrt(x*x + y*y + z*z) < self.particleRadius
        filter = numpy.fft.ifftshift(numpy.exp(-self.damping * (x*x + y*y + z*z) / (self.radius*self.radius)))
        suppRad = numpy.floor(self.radius)
        flatSupport = self.support.flatten()

        lenIter = self.size * self.size * self.size
        iter = numpy.random.rand(lenIter)
        numPixsToKeep = numpy.ceil(self.frac * self.support.sum())

        #Recipe for making binary particle.
        for i in range(4):
            #Sets the largest numPixsToKeep pixels to one
            #   and the rest to zero
            iter *= flatSupport
            ordering = iter.argsort()[-1:-numPixsToKeep-1:-1]
            iter[:] = 0
            iter[ordering] = 1.

            #Smoothing with Gaussian filter
            temp = numpy.fft.fftn(iter.reshape(self.size, self.size, self.size))
            iter = numpy.real(numpy.fft.ifftn(filter*temp).flatten())

        self.density = iter.reshape(self.size, self.size, self.size)

        #Create padded support
        paddedSupport = numpy.sqrt(x*x + y*y + z*z) < (self.particleRadius + self.pad)
        self.supportPositions = numpy.array([[self.radius+i,self.radius+j,self.radius+k] for i,j,k,l in zip(x.flat, y.flat, z.flat, paddedSupport.flat) if l >0]).astype(int)

    def createTestScatteringGeometry(self):
        """
        Contains recipe to create, diffract and show a low-pass-filtered, random particle contrast.

        If particle and diffraction parameters are not given, then default ones are used:
        particleRadius  = 5.9   (num. of pixels; good results if number is x.9, where x is an integer),
        damping         = 1.5   (larger damping=larger DeBye-Waller factor),
        frac            = 0.5   (frac. of most intense realspace voxels forced to persist in iterative particle generation),
        pad             = 1.8   (extra voxels to pad on 3D particle density to create support for phasing),
        radius          = numpy.floor(particleRadius) + numpy.floor(pad) (half length of cubic volume that holds particle),
        size            = 2*radius + 1 (length of cubic volume that holds particle).

        """

        self.z = 1.
        self.sigma = 6.0
        self.qmax = numpy.ceil(self.sigma * self.particleRadius)
        self.qmin = 1.4302966531242025 * (self.qmax / self.particleRadius)
        zSq = self.z*self.z
        self.numPixToEdge = numpy.floor(self.qmax / numpy.sqrt(zSq/(1.+zSq) + (zSq/numpy.sqrt(1+zSq) -self.z)))
        self.detectorDist = self.z * self.numPixToEdge
        msg = time.asctime() + ":: " +"(qmin, qmax, detectorDist)=(%lf, %lf, %lf)"%(self.qmin, self.qmax, self.detectorDist)
        _print_to_log(msg, log_file=self.runLog)

        #make detector
        [x,y] = numpy.mgrid[-self.numPixToEdge:self.numPixToEdge+1, -self.numPixToEdge:self.numPixToEdge+1]
        tempDetectorPix = [self.placePixel(i,j,self.detectorDist) for i,j in zip(x.flat, y.flat)]
        qualifiedDetectorPix = [i for i in tempDetectorPix if (self.qmin<numpy.sqrt(i[0]*i[0] +i[1]*i[1] + i[2]*i[2])<self.qmax)]
        self.detector = numpy.array(qualifiedDetectorPix)

        #make beamstop
        fQmin = numpy.floor(self.qmin)
        [x,y,z] = numpy.mgrid[-fQmin:fQmin+1, -fQmin:fQmin+1, -fQmin:fQmin+1]
        if op.beamstop:
            tempBeamstop = [[i,j,k] for i,j,k in zip(x.flat, y.flat, z.flat) if (numpy.sqrt(i*i + j*j + k*k) < (self.qmin - numpy.sqrt(3.)))]
        else:
            tempBeamstop = [[0,0,0]]
        self.beamstop = numpy.array(tempBeamstop).astype(int)

    def diffractTestCase(self, inMaxScattAngDeg=45., inSigma=6.0, inQminNumShannonPix=1.4302966531242025):
        """
        Requires makeMonster() to first be called, so that particle density is created.

        Function diffract() needs the maximum scattering angle to the edge of the detector, the
        sampling rate of Shannon pixels (inSigma=6 means each Shannon pixel is sampled
        by roughly 6 pixels), and the central missing data region has a radius of
        inQminNumShannonPix (in units of Shannon pixels).

        Variables redefined here:
        z               =   cotangent of maximum scattering angle,
        sigma           =   sampling rate on Shannon pixels,
        qmax            =   number of pixels to edge of detector,
        numPixToEdge    =   same as qmax,
        detectorDist    =   detector-particle distance (units of detector pixels),
        beamstop        =   voxel positions of central disk of missing data on detector,
        detector        =   pixel position of 2D area detector (projected on Ewald sphere),
        intensities     =   3D Fourier intensities of particle.
        """
        self.z = 1/numpy.tan(numpy.pi * inMaxScattAngDeg / 180.)
        self.sigma = inSigma
        self.qmax = numpy.ceil(self.sigma * self.particleRadius)
        zSq = self.z*self.z
        self.numPixToEdge = numpy.floor(self.qmax / numpy.sqrt(zSq/(1.+zSq) + (zSq/numpy.sqrt(1+zSq) -self.z)))
        self.detectorDist = self.z * self.numPixToEdge
        self.qmin = inQminNumShannonPix * (self.qmax / self.particleRadius)

        #make fourier intensities
        intensSize = 2 * self.qmax + 1
        self.intensities = numpy.zeros((intensSize, intensSize, intensSize))
        self.intensities[:self.size, :self.size, :self.size] = self.density
        self.intensities = numpy.fft.fftshift(numpy.fft.fftn(self.intensities))
        self.intensities = numpy.abs(self.intensities * self.intensities.conjugate())

    def showDensity(self):
        """
        Shows particle density as an array of sequential, equal-sized 2D sections.
        """
        subplotlen = int(numpy.ceil(numpy.sqrt(len(self.density))))
        #fig = plt.figure(figsize=(9.5, 9.5))
        for i in range(len(self.density)):
            pass
            #ax = fig.add_subplot(subplotlen, subplotlen, i+1)
            #ax.imshow(self.density[:,:,i], vmin=0, vmax=1.1, interpolation='nearest', cmap=plt.cm.bone)
            #ax.set_title('z=%d'%i, color='white', position=(0.85,0.))
        #plt.show()

    def showLogIntensity(self, inSection=0):
        """
        Show a particular intensities section of Fourier intensities.
        Sections range from -qmax to qmax.
        """
        plotSection = inSection
        if(plotSection<=0):
            plotSection += self.qmax

        #fig = plt.figure(figsize=(13.9,9.5))
        #ax = fig.add_subplot(111)
        #ax.set_title("log(intensities) of section q=%d"%plotSection)
        #self.currPlot = plt.imshow(numpy.log(self.intensities[:,:,plotSection]), interpolation='nearest')
        #self.colorbar = plt.colorbar(self.currPlot, pad=0.02)
        #plt.show()

    def showLogIntensitySlices(self):
        """
        Shows Fourier intensities as an array of sequential, equal-sized 2D sections.
        Maximum intensities set to logarithm of maximum intensity in 3D Fourier volume.
        """
        subplotlen = int(numpy.ceil(numpy.sqrt(len(self.intensities))))
        maxLogIntens = numpy.log(self.intensities.max())
        minLogIntens = numpy.log(self.intensities.min())
        #fig = plt.figure(figsize=(13.5, 9.5))
        for i in range(len(self.intensities)):
            pass
            #ax = fig.add_subplot(subplotlen, subplotlen, i+1)
            #ax.imshow(numpy.log(self.intensities[:,:,i]+1.E-7), vmin=minLogIntens, vmax=maxLogIntens, interpolation='nearest')
            #ax.set_xticks(())
            #ax.set_yticks(())
            #ax.set_title('%d'%(i-self.qmax), color='white', position=(0.85,0.))
        #plt.show()

    def writeSupportToFile(self, filename="support.dat"):
        """ Write the support range to a file.
        :param filename: Path to file.
        :type filename: str
        """

        header = "%d\t%d\n" % (self.qmax, len(self.supportPositions))
        with open(filename, 'w') as f:
            f.write(header)
            for i in self.supportPositions:
                text = "%d\t%d\t%d\n" % (i[0], i[1], i[2])
                f.write(text)
            f.close()

    def writeDensityToFile(self, filename="density.dat"):
        """ Write electron density to a file.
        :param filename: Path to file.
        :type filename: str
        """

        with open(filename, "w") as f:
            self.density.tofile(f, sep="\t")
            f.close()

    def writeAllOuputToFile(self, supportFileName="support.dat", densityFileName="density.dat", detectorFileName="detector.dat", intensitiesFileName="intensity.dat"):
        """
        Convenience function for writing output

        :param supportFileName: Path to file for support data.
        :type supportFileName: str, default 'support.dat'

        :param densityFileName: Path to file for density data.
        :type densityFileName: str, default 'density.dat'

        :param detectorFileName: Path to file for detector data.
        :type detectorFileName: str, default 'detector.dat'

        :param intensitiesFileName: Path to file for intensities data.
        :type intensitiesFileName: str, default intensities.dat'
        """
        self.writeSupportToFile(supportFileName)
        self.writeDensityToFile(densityFileName)
        self.writeDetectorToFile(detectorFileName)
        self.writeIntensitiesToFile(intensitiesFileName)
