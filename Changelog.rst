CHANGELOG
=========
Changes in 0.4
--------------
    * 0.4.1: Bugfix to compensate for no longer supported matplolib feature (set_aspect('datalim'))

Changes from 0.3 to 0.4
-----------------------
    * Debugged XCSITPhotonDetector
    * Added phase grating simulation to WPG (wavefront propagation)
    * Added SASE model for low gain FEL via ocelot
    * GAPDPhotonDiffractor for polychromatic diffraction from large samples (>10^5 atoms. (GAPD code).
    * Many new data analysis utilities
    * Integration of python-pint to support pysical units and constants
    * New XMDYNPhotonMatterInteractor to wrap XMDYN photon-matter interaction code
    * New SLURM Submitter

Changes from 0.2 to 0.3
-----------------------
New in 0.3.4
''''''''''''
    * New classes DetectorGeometry and DetectorPanel as interfaces to 2D pixel area detectors.
    * Use of physical units in Diffractors, DiffractofParameters, and DetectorGeometry.
    * Compatible with new pysingfel interface.
    * Fixed FindHDF cmake utility (Thanks to Andrea Dotti).
    * Small improvements in Analysis classes.

New in 0.3.3
''''''''''''

New features
""""""""""""
* EstherExperiment: A workflow for radiation-hydrodynamics simulations
* Added CrystFEL to external libraries (building simex_platform will download, build, and install CrystFEL as well). Controllable via the DCrystFELPhotonDiffractor flag to cmake.

Bug fixes
"""""""""
* Various small bug fixes related to Esther interfaces, enabled minimal working example with the EstherPhotonMatterInteractor.

Tests
"""""
* Disabled lengthy tests on the CI server.


New in 0.3.2
''''''''''''

Documentation
"""""""""""""
* Tutorial for PlasmaXRTSCalculator  (in the wiki).
* Tutorial for CrystFELPhotonDiffracto (in the wiki).

Bug fix
"""""""
* Fixed a bug in WPG leading to segfault if wavefront mesh not quadratic shape (nx != ny).
* Various bug fixes in PlasmaXRTSCalculator and CrystFELPhotonDiffractor which were discovered while writing the tutorial.

New in 0.3.1
''''''''''''

New features
""""""""""""
* FEFFPhotonMatterInteractor: Calculator for the opensource part of FEFF8.5 allowing calculation
 of EXAFS spectra for a given sample specification.

Documentation
"""""""""""""
* Including more utility functions and new calculators (added since version 0.2) to the reference manual.

Bug fixes and enhancements
""""""""""""""""""""""""""
* Fixed missing documentation in 0.3.0



New in 0.3.0
''''''''''''

New features
""""""""""""
* CrystFELPhotonDiffractor for serial crystallography simulation (backengine: CrystFEL.pattern_sim http://www.desy.de/~twhite/crystfel/). Beam parameters can be extracted from wavefront data.

* PhotonBeamParameters to parametrize photon beams.

* XCSITPhotonDetector and XCSITPhotonDetectorParameters for 2D pixel detector simulation. Requires Geant4 and XCSIT being installed, these are not part of the external libraries shipped with simex_platform (partly due to licensing issues). Disabled in the build system by default.

* PlasmaXRTSCalculator reads propagated wavefront data to synthesize scattering spectrum with instrumental broadening.

* XFELPhotonAnalysis for diagnostics of wavefront data stored in native FAST/WPG wavefront format. OpenPMD currently not supported. bin/prop_diagnostics.py added as CLI.

* DiffractionAnalysis for diagnostics of diffraction data. CLI: bin/diffr_diagnostics.py

* Added option for no rotation in SingFELPhotonDiffractor.

* ComptonScatteringCalculator for Compton scattering from plasmas.

* Support for sample structures in xyz format.

* GenesisPhotonSource to describe FELs using Genesis and conversion utilities to convert genesis output to wpg readable format, as well as PIC openPMD data to genesis readable format.

* Conversion from PIC openPMD to simplex FEL code input.

* Adding ocelot electron beam simulation framework and FEL code to external libraries.

* Various tools to steer Esther radiation-hydrodynamics simulations and experiment design.

* Converter for Shadow3 raytracing beams into OpenPMD particle-mesh data. To be used as python script in Oasys.

Bug fixes and enhancements
""""""""""""""""""""""""""
* Removed random rotation in XMDYNDemoPhotonMatterInteractor since done in SingFELPhotonDiffractor

* Improve MPI parallelization in EMCOrientation

* Make use of units more consistent in PlasmaXRTSCalculator

* Replaced singfel by pysingfel (reimplementation in python, less dependencies on fat libraries like boost, armadillo).

* Exposing most Calculators, Parameters, Utilities, and Analysis objects in SimEx top level module. (>>> from SimEx import SingFELPhotonDiffractor).

* Azimuthal integration of diffraction patterns uses pyFAI.

* Fixing pdb parser to parse large (>100000 atoms) pdbs.

* WPG uses threaded version (openmp) of SRW.

* Ability to process time-independent wavefront data (one slice in frequency space).

* PhotonDiffractors write one single hdf5 file which links to individual patterns.

* Using xraydb (github/scikit-beam/xraydb) for x-ray material properties and atomic levels.

* Automated collection of system variables to setup MPI parameters for parallel backengine execution.

* Various bugs in XMDYNDemoPhotonMatterInteractor

* EMCOrientation: Parallel improvements to create backengine input data photons.dat

* Fixing EMC for new diffr data format.

* Adding parameters cpus_per_task and forced_mpi_command and default handling.

* Adding parallel backengines for high performance backengine execution.


Documentation
"""""""""""""
* SimEx single-particle imaging tutorial moved to wiki (github.com/eucall-software/simex_platform/wiki

* New tutorial for usage of Esther rad-hydro simulations

* Demonstration of new diagnostics tools for wavefront and diffraction data.


Build system and deployment
"""""""""""""""""""""""""""
* Various improvements in docker image generation and usage.

* Added pyqt to dockerfiles

* Added --bind-to none to mpi command

* Updated Docker files
