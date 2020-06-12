from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance


class IonMatterInteractorParameters(AbstractCalculatorParameters):
    """
    :class IonMatterInteractorParameters: Encapsulates parameters for the IonMatterInteractor calculator.
    """

    def __init__(self,
                energy_bin=None,
                neutron_weight=None,
                ibeam_radius=None,
                target_length=None,
                target_density=None,
                ion_name=None,
                xsec_file=None,
                **kwargs
                ):
        self.energy_bin = energy_bin
        self.neutron_weight = neutron_weight
        self.ibeam_radius = ibeam_radius
        self.target_length = target_length
        self.target_density = target_density
        self.ion_name = ion_name
        self.xsec_file = xsec_file

        super(IonMatterInteractorParameters, self).__init__(**kwargs)

    def _setDefaults(self):
        """ Set default for required inherited parameters. """
        self._AbstractCalculatorParameters__cpus_per_task_default = 1

    @property
    def energy_bin(self):

        return self.__energy_bin

    @energy_bin.setter
    def energy_bin(self, val):

        self.__energy_bin = checkAndSetInstance(float, val, 1.e4)

    @property
    def xsec_file(self):
        return self.__xsec_file

    @xsec_file.setter
    def xsec_file(self, val):
        self.__xsec_file = checkAndSetInstance(str, val, 'file.txt')

    @property
    def neutron_weight(self):
        return self.__neutron_weight

    @neutron_weight.setter
    def neutron_weight(self, val):
        self.__neutron_weight = checkAndSetInstance(float, val, 1.e4)

    @property
    def ibeam_radius(self):
        return self.__ibeam_radius

    @ibeam_radius.setter
    def ibeam_radius(self, val):
        self.__ibeam_radius = checkAndSetInstance(float, val, 1.e-5)

    @property
    def target_length(self):
        return self.__target_length

    @target_length.setter
    def target_length(self, val):
        self.__target_length = checkAndSetInstance(float, val, 1.e-2)

    @property
    def target_density(self):
        return self.__target_density

    @target_density.setter
    def target_density(self, val):
        self.__target_density = checkAndSetInstance(float, val, 1.e28)

    @property
    def ion_name(self):
        return self.__ion_name

    @ion_name.setter
    def ion_name(self, val):
        self.__ion_name = checkAndSetInstance(str, val, 'deuteron')