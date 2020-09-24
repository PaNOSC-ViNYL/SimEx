""":module TNSAIonMatterInteractor: Module that holds the TNSAIonMatterInteractor class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2020 Zsolt Lecz, Juncheng E                              #
# Contact: Juncheng E <juncheng.e@xfel.eu>                               #
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
from SimEx.Calculators.AbstractIonInteractor import AbstractIonInteractor
import sdf
import sys
import math
import numpy as np
from scipy.constants import e, m_p as mp
from numpy.random import random
import openpmd_api as api
import time
import pathlib
import os


class TNSAIonMatterInteractor(AbstractIonInteractor):
    data = []
    __dims = 8
    Nn = 0

    def __init__(self, parameters=None, input_path=None, output_path=None):
        super(TNSAIonMatterInteractor, self).__init__(parameters, input_path,
                                                      output_path)
        self.counts = []
        self.binedges = []

    def read_xsec(self):
        """Read in cross section from filename """
        masses = {'D': 2.014, 'T': 3.016, '3He': 3.016}
        parent_path = pathlib.Path(self.input_path).parent.absolute()
        file_path = os.path.join(parent_path, self.parameters.xsec_file)
        E, xs = np.genfromtxt(file_path,
                              comments='#',
                              skip_footer=2,
                              unpack=True)

        collider, target = self.parameters.xsec_file.split('_')[:2]
        m1, m2 = masses[target], masses[collider]
        E *= m1 / (m1 + m2)

        return E, xs

    def saveH5(self):
        SCALAR = api.Mesh_Record_Component.SCALAR
        Unit_Dimension = api.Unit_Dimension

        series = api.Series(self.output_path, api.Access_Type.create)
        dateNow = time.strftime('%Y-%m-%d %H:%M:%S %z', time.localtime())
        print("Default settings:")
        print("basePath: ", series.base_path)
        print("openPMD version: ", series.openPMD)
        print("iteration format: ", series.iteration_format)

        series.set_openPMD("1.1.0")
        # series.set_openPMD_extension("BeamPhysics;SpeciesType")
        series.set_attribute("openPMDextension", "BeamPhysics;SpeciesType")
        series.set_author("Zsolt Lecz<zsolt.lecz@eli-alps.hu>")
        series.set_particles_path("particles")
        series.set_date(dateNow)
        series.set_iteration_encoding(api.Iteration_Encoding.group_based)
        series.set_software("EPOCH", "4.8.3")
        # series.set_software_version("4.8.3")
        # series.set_attribute("forceField","eam/alloy")
        # series.set_attribute("forceFieldParameter","pair_coeff * * Cu_mishin1.eam.alloy Cu")

        curStep = series.iterations[0]
        curStep.set_time(0.0).set_time_unit_SI(1e-15)
        curStep.set_attribute("step", np.uint64(0))
        curStep.set_attribute("stepOffset", np.uint64(0))
        curStep.set_attribute("timeOffset", np.float32(0))

        neutrons = curStep.particles["neutrons"]
        neutrons.set_attribute("speciesType", "neutron")
        neutrons.set_attribute("numParticles", self.Nn)

        d = api.Dataset(self.data[6].dtype, self.data[6].shape)
        neutrons["id"][SCALAR].reset_dataset(d)
        neutrons["id"][SCALAR].store_chunk(self.data[6])

        d = api.Dataset(self.data[7].dtype, self.data[7].shape)
        neutrons["weight"][SCALAR].reset_dataset(d)
        neutrons["weight"][SCALAR].store_chunk(self.data[7])

        d = api.Dataset(self.data[0].dtype, self.data[0].shape)
        neutrons["position"]["x"].reset_dataset(d)
        neutrons["position"]["y"].reset_dataset(d)
        neutrons["position"]["z"].reset_dataset(d)
        neutrons["position"]["x"].set_unit_SI(1.e-6)
        neutrons["position"]["y"].set_unit_SI(1.e-6)
        neutrons["position"]["z"].set_unit_SI(1.e-6)
        neutrons["position"].set_unit_dimension({Unit_Dimension.L: 1})
        neutrons["position"]["x"].store_chunk(self.data[0])
        neutrons["position"]["y"].store_chunk(self.data[1])
        neutrons["position"]["z"].store_chunk(self.data[2])

        d = api.Dataset(self.data[0].dtype, self.data[0].shape)
        neutrons["velocity"]["x"].reset_dataset(d)
        neutrons["velocity"]["y"].reset_dataset(d)
        neutrons["velocity"]["z"].reset_dataset(d)
        neutrons["velocity"]["x"].set_unit_SI(1)
        neutrons["velocity"]["y"].set_unit_SI(1)
        neutrons["velocity"]["z"].set_unit_SI(1)
        neutrons["velocity"].set_unit_dimension({
            Unit_Dimension.L: 1,
            Unit_Dimension.T: -1
        })
        neutrons["velocity"]["x"].store_chunk(self.data[3])
        neutrons["velocity"]["y"].store_chunk(self.data[4])
        neutrons["velocity"]["z"].store_chunk(self.data[5])

        series.flush()
        del series

    def backengine(self):
        if not self.counts:
            [mom, weight] = self.readSDF()
            energy = np.square(mom) / (2 * mp * e)
            de = self.parameters.energy_bin
            nb = math.floor(np.max(energy) / de)
            self.counts = [0 for i in range(nb + 1)]
            self.binedges = [(i + 1) * de for i in range(nb + 1)]
            print("Number of energy bins: %s" % len(self.binedges))
            for en in energy:
                index = math.floor(en / de)
                self.counts[index] += weight[index]

        [E, xs] = self.read_xsec()
        xs = np.interp(self.binedges, E * 1.e6, xs * 1.e-28)

        vx = [0]
        self.Nn = 0
        for i in range(len(self.binedges)):
            px = np.sqrt(2 * mp * self.binedges[i] * e)
            Nd = self.counts[
                i] * self.parameters.ibeam_radius**2 / self.parameters.neutron_weight
            inc = int(
                round(Nd * self.parameters.target_density
                      * self.parameters.target_length * xs[i]))
            if inc > 0:
                vx = np.append(vx, np.ones(inc) * px / mp)
                self.Nn += inc

        print("Number of neutron macroparticles:", self.Nn)
        vx = vx[1:]

        self.data = np.zeros(shape=(self.__dims, self.Nn))
        vn = math.sqrt(2 * 2.45e6 * e / mp)
        self.data[0] = 1.e6 * self.parameters.target_length * random(self.Nn)
        r = 1.e6 * self.parameters.ibeam_radius * np.sqrt(random(
            self.Nn))  # positions will be saved in units of micron
        a = 2 * math.pi * random(self.Nn)

        self.data[1] = np.multiply(r, np.cos(a))
        self.data[2] = np.multiply(r, np.sin(a))

        aa = math.pi * random(self.Nn)
        b = 2 * math.pi * random(self.Nn)

        self.data[3] = np.add(vn * np.cos(aa), vx)
        velr = vn * np.sin(aa)
        self.data[4] = np.multiply(velr, np.cos(b))
        self.data[5] = np.multiply(velr, np.sin(b))
        self.data[6] = np.arange(1, self.Nn + 1)  # id
        self.data[7] = self.parameters.neutron_weight * np.ones(self.Nn)

        return 0

    def readSDF(self):
        if not os.path.exists(self.input_path):
            msg = 'File "{:s}" not found'.format(self.input_path)
            raise FileNotFoundError(msg)

        d = sdf.read(self.input_path)

        px = d.__dict__[self.expectedData[1]]
        wd = d.__dict__[self.expectedData[-1]]
        return px.data, wd.data

    def _readH5(self):
        pass