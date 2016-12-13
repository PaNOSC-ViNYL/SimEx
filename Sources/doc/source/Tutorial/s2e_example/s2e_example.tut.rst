.. simex_platform tutorial file, created by Carsten Fortmann-Grote

Single particle imaging example workflow
________________________________________

This entry level tutorial demonstrates the usage of simex_platform by showing how to simulate a single-particle imaging experiment at the SPB-SFX instrument of the European XFEL.

In this tutorial, you will learn how to

* Propagate x-ray pulses from the photon source to the experimental interaction region using the
  wave propagation calculator "WavePropagator".
* Specify a sample using the corresponding PDB code.
* Calculate the interaction of x-ray photons with the sample using a demo version of the x-ray
  photon - matter interaction codes XMDYN and XATOM.
* Simulate the diffraction of x-ray photons from the sample in a number of random orientations as it
  is exposed to the x-ray pulse.
* Orient the simulated diffraction patterns using the Expand-Maximize-Compress (EMC) orientation
  algorithm into a 3D mesh.
* Calculate the 3D electron density using the Difference-Map (DM) phasing algorithm.

Preparing the source input
``````````````````````````

We begin the simulation with the x-ray pulse at the exit of the undulator section. Data files for a
wide range of pulse properties (electron bunch charge (which determines the pulse duration),
accelerator energy and photon energy, as well as the active undulator length, i.e. the saturation
level of the emitted radiation are provided through the XFEL pulse database https://in.xfel.eu/xpd.

In this tutorial, we will use x-ray pulses of approximately 9 fs duration and a photon energy of
4.96 keV. Fill in the database query webform such that it looks like this:

.. image:: Tutorial/s2e_example/resources/xpd_filled_9fs_5keV_nz35.png
   :width: 50%
   :alt: Filling in remaining options.
   :align: center

Provide your email address and click "Submit request". You will then receive a request ID and an
email will notify you once the calculation has finished and provide you with a link where the
pulse data can be downloaded. Download and extract the zip file to a place of your liking.


Beamline propagation
```````````````````````````````````

Propagation of x-ray pulses through the SPB-SFX beamline will be performed by means of the
:code:`WavePropagator` class, that comes with simex_platform. It interfaces the wavefront propagation code
WPG. Below is a commented python script that demonstrates setup and execution of the propagation.
:download:`Download it here.<Tutorial/s2e_example/resources/propagation.py>`

.. literalinclude:: Tutorial/s2e_example/resources/propagation.py
   :linenos:

The definition of the beamline (line 7) loads a WPG beamline from the beamline collection. Besides
the beamline, the user has to specify the location of the source files (see `Preparing the source
input`_). The variable :code:`input_path` can be either a file or a directory. In the latter case, all valid source
files in the directory will be processed.

The :code:`WavePropagator` class requires two input parameters, a parameters object (of type
:code:`WavePropagationParameters`, defined in line 10),
and the :code:`input_path`. After construction, the input files are read in using the method :code:`_readH5`,
and the calculation is executed by calling the :code:`backengine` method.

A third input parameter for the :code:`WavePropagator` class, :code:`output_path` can be used to specify where the results of the wavefront
propagation shall be saved. By default, they are stored in a directory called "prop" below the
current working directory.

