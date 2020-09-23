import unittest
from SimEx.Parameters.IonMatterInteractorParameters import IonMatterInteractorParameters
from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters


class IonMatterInteractorParametersTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def testConstructionFaultyInput(self):
        self.assertRaises(TypeError, IonMatterInteractorParameters, xsec_file=2.0)

    def testDefaultConstruction(self):
        parameters = IonMatterInteractorParameters()
        self.assertIsInstance(parameters, IonMatterInteractorParameters)
        self.assertIsInstance(parameters, AbstractCalculatorParameters)

        self.assertEqual(parameters.neutron_weight, 1.e4)
        self.assertEqual(parameters.energy_bin, 1.e4)

    def testShapedConstruction(self):
        parameters = IonMatterInteractorParameters(energy_bin=2.e4, ibeam_radius=15.e-6, target_density=6.e28)

        self.assertIsInstance(parameters, IonMatterInteractorParameters)
        self.assertIsInstance(parameters, AbstractCalculatorParameters)

        self.assertEqual(parameters.energy_bin, 2.e4)
        self.assertEqual(parameters.ibeam_radius, 1.5e-5)
        self.assertEqual(parameters.target_density, 6.e28)


if __name__ == '__main__':
    unittest.main()
