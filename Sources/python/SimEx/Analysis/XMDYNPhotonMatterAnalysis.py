#!/usr/bin/env python2.7

import h5py
import numpy
import os
import pylab

from SimEx.Analysis.AbstractAnalysis import AbstractAnalysis


class XMDYNPhotonMatterAnalysis(AbstractAnalysis):
    """ Class to encapsulate diagnostics of photon matter interaction trajectories. """

    def __init__( self, input_path=None,):
        """ Constructor an instance of  XMDYNPhotonMatterAnalysis.

        :param input_path: Path to the data to analyze.
        :type input_path: str

        """

        self.input_path = input_path

        self.__num_digits = 7
        self.__prj = '.'

    @property
    def input_path(self):
        """ Query the input path. """
        return self.__input_path
    @input_path.setter
    def input_path(self, value):
        """ Set the input path to a value.

        :param value: The input path to set.
        :type value: str

        """
        error_message = "The parameter 'input_path' must be a str indicating an existing file or directory. "
        if not isinstance(value, str):
            raise TypeError(error_message)
        if not os.path.exists(value):
            raise ValueError(error_message)

        self.__input_path = value

    def load_snapshot(self, snapshot_index):
        """ Load snapshot data from hdf5 file into memory. """

        snp = snapshot_index
        dbase_root = "/data/snp_" + str( snp ).zfill(self.__num_digits) + "/"
        xsnp = dict()

        with h5py.File(self.input_path) as fp:
            xsnp['Z']   = fp.get( dbase_root + 'Z' )   .value
            xsnp['T']   = fp.get( dbase_root + 'T' )   .value
            xsnp['ff']  = fp.get( dbase_root + 'ff' )  .value
            xsnp['xyz'] = fp.get( dbase_root + 'xyz' ) .value
            xsnp['r']   = fp.get( dbase_root + 'r' )   .value
            xsnp['Nph']   = fp.get( dbase_root + 'Nph' )   .value
            N = xsnp['Z'].size
            xsnp['q'] = numpy.array( [ xsnp['ff'][ pylab.find( xsnp['T'] == x ) , 0 ]  for x in xsnp['xyz'] ] ) .reshape(N,)
            xsnp['snp'] = snp ;

        return xsnp

    def number_of_snapshots(self) :
        """ Get number of valid snapshots. """
        with h5py.File( self.input_path, 'r') as xfp:
            count = len([k for k in xfp['data'].keys() if "snp_" in k])
        return count

def load_sample(sample_path) :
    """ Load a sample file into memory. """

    sample = dict()

    with h5py.File( sample_path , "r" ) as xfp:
        sample['Z'] = xfp.get('Z').value
        sample['r'] = xfp.get('r').value

    sample['selZ'] = dict()

    for sel_Z in numpy.unique(sample['Z']) :
        sample['selZ'][sel_Z] = pylab.find(sel_Z == sample['Z'])

    return sample

def read_h5_dataset( path , dataset ) :
    """ Read a dataset from hdf5 file. """
    with h5py.File( path , "r" ) as xfp:
        data = xfp.get( dataset ).value
    return data

def calculate_displacement(snapshot, r0, sample) :
    """ Calculate the average displacement per atomic species in a snapshot.

    :param snapshot: The snapshot to analyze
    :type snapshot: dict

    :param r0: Unperturbed positions of the sample atoms.
    :type r0: numpy.array (shape=(Natoms, 3))
    ### CHECKME: Can't we read r0 from the sample dict?

    :param sample: Sample data
    :type sample: dict

    """

    num_Z = len( list(sample['selZ'].keys()) )
    all_disp = numpy.zeros( ( num_Z , ) )

    count = 0

    for sel_Z in list(sample['selZ'].keys()) :
        dr = snapshot['r'][sample['selZ'][sel_Z],:] - r0[sample['selZ'][sel_Z],:]
        all_disp[count] = numpy.mean( numpy.sqrt( numpy.sum( dr * dr , axis = 1 ) ) ) / 1e-10
        count = count + 1

    return all_disp

def calculate_ion_charge(snapshot, sample):
    """ Calculate the remaining electric charge per atomic species of a given snapshot.

    :param snapshot: The snapshot to analyze
    :type snapshot: dict

    :param sample: The sample data.
    :type sample: dict

    """

    num_Z = len( list(sample['selZ'].keys()) )
    all_numE = numpy.zeros( ( num_Z , ) )
    count = 0

    for sel_Z in list(sample['selZ'].keys()) :
        all_numE[count] = numpy.mean( snapshot['q'][sample['selZ'][sel_Z]] )
        count = count + 1

    return all_numE
