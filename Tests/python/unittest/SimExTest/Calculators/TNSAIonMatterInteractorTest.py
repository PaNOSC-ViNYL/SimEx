import unittest
from SimEx.Calculators.TNSAIonMatterInteractor import TNSAIonMatterInteractor
from SimEx.Parameters.IonMatterInteractorParameters import IonMatterInteractorParameters
from SimEx.Calculators.AbstractIonInteractor import AbstractIonInteractor
import os


class TNSAIonMatterInteractorTest(unittest.TestCase):

    def setUp(self):
        self.params = IonMatterInteractorParameters(ion_name='proton')
        self.params.xsec_file = 'D_D_-_3He_n.txt'
        self.__files_to_remove = ['NeutronData.h5']

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)


    def testConstructor(self):
        interact = TNSAIonMatterInteractor(self.params, input_path='something', output_path='')
        self.assertIsInstance(interact, TNSAIonMatterInteractor)
        self.assertIsInstance(interact, AbstractIonInteractor)

    def testRun(self):
        mysource = TNSAIonMatterInteractor(parameters=self.params,
                                           input_path=generateTestFilePath('0010.sdf'),
                                           output_path='Data/NeutronData.h5')

        try:
            mysource.backengine()
            throws = False
        except:
            throws = True

        self.assertFalse(throws)

        mysource.saveH5()


if __name__ == '__main__':
    unittest.main()
