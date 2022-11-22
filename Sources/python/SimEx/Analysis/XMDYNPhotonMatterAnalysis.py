#!/usr/bin/env python
""":module XMDYNPhotonMatterAnalysis: Hosting utilities to analyse and visualize photon-matter trajectories generated by XMDYN."""

from random import sample
import h5py
import numpy
import os
import periodictable as pte

ELEMENT_SYMBOL = ['All'] + [e.symbol for e in pte.elements]
from SimEx.Analysis.AbstractAnalysis import AbstractAnalysis, plt
from SimEx.Utilities.IOUtilities import loadPDB, loadXYZ


class XMDYNPhotonMatterAnalysis(AbstractAnalysis):
    """:class XMDYNPhotonMatterAnalysis: Class to encapsulate diagnostics of photon matter interaction trajectories. """

    def __init__( self, input_path=None, snapshot_indices=None, elements=None, sample_path=None):
        """

        :param input_path: Path to the data to analyze.
        :type input_path: str

        :param snapshot_indices: Snapshot (indices or IDs) to analyze (Default: All).
        :type snapshot_indices: list

        :param elements: Which elements to include in the analysis (Default: All).
        :type elements: list

        """
        self.input_path = input_path
        self.sample_path = sample_path
        self.snapshot_indices=snapshot_indices
        self.elements=elements

        self.__num_digits = 7
        self.__prj = '.'

        self.load_trajectory()

    @property
    def t(self):
        return self.__trajectory["time"]

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

    @property
    def sample_path(self):
        """ Query the sample path. """
        return self.__sample_path
    @sample_path.setter
    def sample_path(self, value):
        """ Set the sample path to a value.

        :param value: The sample path to set.
        :type value: str

        """
        error_message = "The parameter 'sample_path' must be a str indicating an existing file or directory. "
        if not isinstance(value, str):
            raise TypeError(error_message)
        if not os.path.exists(value):
            raise ValueError(error_message)

        self.__sample_path = value

    @property
    def snapshot_indices(self):
        """ Query the snapshot indices. """
        return self.__snapshot_indices
    @snapshot_indices.setter
    def snapshot_indices(self, value):
        """ Set the snapshot indices.

        :param value: The snapshot indices.
        :type value: list

        """
        error_message = "The parameter 'snapshot_indices' must be a list of integers."
        if value is None or value == 'All':
            value = ['All']
        if isinstance(value, int):
            value = [value]
        if not hasattr(value, "__iter__"):
            raise TypeError(error_message)
        if not all([(isinstance(i, int) or i=="All") for i in value]):
            raise TypeError(error_message)

        self.__snapshot_indices = value

    @property
    def elements(self):
        """ Query the elements to include. """
        return self.__elements
    @elements.setter
    def elements(self, value):
        """ Set the elements to include in the analysis.

        :param value: Which elements to include.
        :type value: list of symbols or element numbers.

        """
        error_message = "The parameter 'elements' must be a list of chemical element symbols or integers indicating which elements to include in the analysis. "

        if value is None or value == 'All':
            value = ['All']
        if isinstance(value, int) or value in ELEMENT_SYMBOL:
            value = [value]
        if not hasattr(value, "__iter__"):
            raise TypeError(error_message)
        if not all([(isinstance(i, int) or i in ELEMENT_SYMBOL) for i in value]):
            raise ValueError(error_message)

        self.__elements = value

    def get_element_symbols(self):
        """return the symbol of the amalyzed elements as a list of str"""
        sample = self.get_sample()
        z = sample['selZ'].keys()
        if self.elements != ["All"]:
            z = [a for a in z if a in self.elements]
        return [pte.elements[a] for a in z]


    def load_snapshot(self, snapshot_index):
        """ Load snapshot data from hdf5 file into memory. """

        snp = snapshot_index
        dbase_root = "/data/snp_" + str( snp ).zfill(self.__num_digits) + "/"
        time_path = "/misc/time/snp_" + str( snp ).zfill(self.__num_digits) + "/"
        xsnp = dict()

        with h5py.File(self.input_path) as fp:
            xsnp['t'] = fp.get(time_path).value.item()
            xsnp['Z'] = fp.get(dbase_root+ 'Z').value
            xsnp['T'] = fp.get(dbase_root + 'T').value
            xsnp['ff'] = fp.get(dbase_root + 'ff').value
            xsnp['xyz'] = fp.get(dbase_root + 'xyz').value
            xsnp['r'] = fp.get(dbase_root + 'r').value
            xsnp['Nph'] = fp.get(dbase_root + 'Nph').value
            N = xsnp['Z'].size
            xsnp['q'] = numpy.array([xsnp['ff'][numpy.nonzero(numpy.ravel(xsnp['T']==x))[0], 0] for x in xsnp['xyz']]).reshape(N,)
            # xsnp['q'] = numpy.array([xsnp['ff'][(numpy.array(xsnp['T'])==numpy.array(x)), 0] for x in xsnp['xyz']]).reshape(N,)
            # xsnp['q'] = numpy.array([xsnp['ff'][(numpy.equals(xsnp['T'],x), 0] for x in xsnp['xyz']]).reshape(N,)
            #xsnp['q'] = numpy.array([numpy.array(xsnp['ff'][xsnp['T']==x][0] for x in xsnp['xyz']]).reshape(N,)
            xsnp['snp'] = snp

        return xsnp

    def number_of_snapshots(self) :
        """ Get number of valid snapshots. """
        with h5py.File( self.input_path, 'r') as xfp:
            count = len([k for k in xfp['data'].keys() if "snp_" in k])
        return count

    def get_avg_displacement(self):
        """ Get the average displacement per atomic species as function of time. """
        return self.__trajectory['displacement'].T

    def get_max_displacement(self):
        """ Get the average displacement per atomic species as function of time. """
        return self.__trajectory['max_displacement'].T

    def plot_displacement(self):
        """ Plot the average displacement per atomic species as function of time. """

        for d, sym in zip(self.get_avg_displacement(), self.get_element_symbols()):
            plt.plot(self.t*1e15, d, label=sym) # self.trajectory['disp'][ : , pylab.find( sel_Z == pylab.array( list(data['sample']['selZ'].keys()) ) ) ] , xcolor  )
        plt.xlabel( 'Time [fs]' )
        plt.ylabel( 'Average displacement [$\AA$]' )
        plt.legend()

    def get_sample(self):
        """Load the sample and return it."""
        try:
            sample = load_sample(self.sample_path)
        except:
            if os.path.splitext(self.sample_path)[1] in ['.xy', '.xyz']:
                try:
                    sample = loadXYZ(self.sample_path)
                    print("Using experimental XYZ loader")
                except:
                    sample = loadPDB(self.sample_path)
            else:
                sample = loadPDB(self.sample_path)

        return sample

    def get_avg_charge(self):
        """ Plot the average number of electrons per atom per atomic species as function of time. """
        return self.__trajectory['charge'].T

    def plot_charge(self):
        """ Plot the average number of electrons per atom per atomic species as function of time. """

        # for d in self.__trajectory['charge'].T:
        for d, sym in zip(self.get_avg_charge(), self.get_element_symbols()):
            plt.plot(self.t*1e15, d, label=sym)

        ### TODO: time axis, labels, legend
        plt.xlabel( 'Time [fs]' )
        plt.ylabel( 'Number of bound electrons per atom' )
        plt.legend()

    def plot_energies(self):
        """ Plot the evolution of MD energies over the simulation time. """
        raise RuntimeError("Not implemented yet.")

    def get_angle(self):
        """ Get the angle quaternion of the sample. """

        with h5py.File(self.input_path) as fp:
            qt = fp.get("/params/angle/").value
        return qt

    def load_trajectory(self):
        """ Load the selected snapshots and extract data to analyze. """

        trajectory = dict()

        sample = None
        disp = []
        max_disp = []
        charge = []
        time = []

        sample = self.get_sample()

        # Read sample data.
        # try:
        #     sample = load_sample(self.sample_path)
        # except:
        #    sample = loadPDB(self.sample_path)

        snapshot_indices = self.snapshot_indices
        if snapshot_indices == "All" or snapshot_indices == ["All"]:
            snapshot_indices = range(1, self.number_of_snapshots() + 1)

        for si in snapshot_indices:
            snapshot = self.load_snapshot(si)
            time.append(snapshot['t'])
            disp.append(calculate_displacement(snapshot, r0=sample['r'], sample=sample))
            max_disp.append(calculate_max_displacement(snapshot, r0=sample['r'], sample=sample))
            charge.append(calculate_ion_charge(snapshot, sample))

        trajectory['displacement'] = numpy.array(disp)
        trajectory['max_displacement'] = numpy.array(max_disp)
        trajectory['charge'] = numpy.array(charge)
        trajectory['time'] = numpy.array(time)

        self.__trajectory = trajectory


    def animate(self):
        """ Generate an animation of atom trajectories and their ionization. """
        pass

def load_sample(sample_path) :
    """ Load a sample file into memory. """

    sample = dict()

    with h5py.File( sample_path , "r" ) as xfp:
        sample['Z'] = xfp.get('Z').value
        sample['r'] = xfp.get('r').value

    sample['selZ'] = dict()

    for sel_Z in numpy.unique(sample['Z']) :
        sample['selZ'][sel_Z] = (numpy.array(sel_Z) == numpy.array(sample['Z']))

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

    return numpy.array(all_disp)


def calculate_max_displacement(snapshot, r0, sample) :
    """ Find the highest displacement value per atomic species in a snapshot.

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
        all_disp[count] = numpy.amax(numpy.sqrt(numpy.sum(dr*dr, axis=1))) / 1e-10
        count = count + 1

    return numpy.array(all_disp)


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

    return numpy.array(all_numE)