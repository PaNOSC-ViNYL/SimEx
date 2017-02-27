from HydrocodeInputCalculatorParameters import HydroParameters
import numpy as np

h = HydroParameters(2,"CH", 20.0, "Iron", 20.0, None, 0.0, 1064)

h._serialize()
