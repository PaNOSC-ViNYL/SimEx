.. simex_platform documentation master file, created by
   sphinx-quickstart on Wed Apr  6 14:14:07 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to simex_platform's documentation!
==========================================

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Why simex_platform?
===================

simex_platform is an environment for simulation of photon science experiments.
It can be used as a python library in a python source code (module or script) or in an interactive python session.


Features
--------

- Simulation of various photon sources, photon propagation, photon-matter interaction, scattering from samples and targets, detection of photons, and analysis of the detector response.
- Make things faster

Installation
------------

Install simex_platform through the following command line sequence (Linux/UNIX/Mac).

    mkdir build

    cd build

    cmake .. -DCMAKE_INSTALL_PREFIX=/path/to/installation ..

    make

    (sudo) make install (sudo required if installation path is outside of the user's realm.)

Finally, set your environment variables by calling

    bin/simex_vars.sh

Usage
-----
Import the simex library:

    import SimEx

in your python source file or interactive shell.
Consult the Examples page for usage examples to get started.

Contribute
----------

- Source Code github.com/eucall-software/simex_platform
- Issue Tracker: github.com/eucall-software/simex_platform/issues

Support
-------

If you are having issues, please let us know at carstendotgroteatxfeldoteu .

License
-------

The project is licensed under the GPL open source license version 3.

Reference Manual
================
.. autoclass:: SimEx.Calculators.AbstractBaseCalculator.AbstractBaseCalculator

.. autoclass:: SimEx.Calculators.AbstractPhotonAnalyzer.AbstractPhotonAnalyzer

.. autofunction:: SimEx.Calculators.AbstractPhotonAnalyzer.checkAndSetPhotonAnalyzer

.. autoclass:: SimEx.Calculators.AbstractPhotonDetector.AbstractPhotonDetector
    :members:
    :private-members:

.. autoclass:: SimEx.Calculators.AbstractPhotonDiffractor.AbstractPhotonDiffractor
    :members:
    :private-members:

.. autoclass:: SimEx.Calculators.AbstractPhotonInteractor.AbstractPhotonInteractor
    :members:
    :private-members:

.. autoclass:: SimEx.Calculators.AbstractPhotonPropagator.AbstractPhotonPropagator
    :members:
    :private-members:

.. autoclass:: SimEx.Calculators.AbstractPhotonSource.AbstractPhotonSource
    :members:
    :private-members:

.. autoclass:: SimEx.Calculators.DMPhasing.DMPhasing
    :members:
    :private-members:

.. autoclass:: SimEx.Parameters.DMPhasingParameters.DMPhasingParameters
    :members:
    :private-members:

.. autoclass:: SimEx.Calculators.EMCCaseGenerator.EMCCaseGenerator
    :members:
    :private-members:

.. autoclass:: SimEx.Calculators.EMCOrientation.EMCOrientation
    :members:
    :private-members:

.. autoclass:: SimEx.Parameters.EMCOrientationParameters.EMCOrientationParameters
    :members:
    :private-members:

.. autoclass:: SimEx.Calculators.OrientAndPhasePhotonAnalyzer.OrientAndPhasePhotonAnalyzer
    :members:
    :private-members:

.. autoclass:: SimEx.Calculators.PerfectPhotonDetector.PerfectPhotonDetector
    :members:
    :private-members:

.. autoclass:: SimEx.Calculators.PlasmaXRTSCalculator.PlasmaXRTSCalculator
    :members:
    :private-members:

.. autoclass:: SimEx.Calculators.S2EReconstruction.S2EReconstruction
    :members:
    :private-members:

.. autoclass:: SimEx.Calculators.SingFELPhotonDiffractor.SingFELPhotonDiffractor
    :members:
    :private-members:

.. autoclass:: SimEx.Parameters.SingFELPhotonDiffractorParameters.SingFELPhotonDiffractorParameters
    :members:
    :private-members:
    :special-members:

.. autoclass:: SimEx.Calculators.WavePropagator.WavePropagator
    :members:
    :private-members:

.. autoclass:: SimEx.Parameters.WavePropagatorParameters.WavePropagatorParameters
    :members:
    :private-members:

.. autoclass:: SimEx.Calculators.XFELPhotonPropagator.XFELPhotonPropagator
    :members:
    :private-members:

.. autoclass:: SimEx.Calculators.XFELPhotonSource.XFELPhotonSource
    :members:
    :private-members:

.. autoclass:: SimEx.Calculators.XMDYNDemoPhotonMatterInteractor.XMDYNDemoPhotonMatterInteractor
    :members:
    :private-members:

.. autoclass:: SimEx.Parameters.AbstractCalculatorParameters.AbstractCalculatorParameters
    :members:
    :private-members:
    :special-members:

.. autoclass:: SimEx::Parameters::PlasmaXRTSCalculatorParameters::PlasmaXRTSCalculatorParameters
    :members:
    :private-members:
    :special-members:


.. .. inheritance-diagram::
