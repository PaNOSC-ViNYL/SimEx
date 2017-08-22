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

In this tutorial, we will propagate one x-ray pulses of approximately 3 fs duration and a photon energy of 4.96 keV.
We begin the simulation with the x-ray pulse at the exit of the undulator section.
Pulse data files for a
wide range of pulse properties (electron bunch charge (which determines the pulse duration),
accelerator energy and photon energy, as well as the active undulator length, i.e. the saturation
level of the emitted radiation are provided through the XFEL pulse database https://in.xfel.eu/xpd.
To query a pulse file from the database, fill in the form like this:

.. image:: Tutorial/s2e_example/resources/xpd.png

Provide your email address and click "Submit request". You will then receive a request ID and an
email will notify you once the calculation has finished and provide you with a link where the
pulse data can be downloaded. Download and extract the zip file to a place of your liking.
In the following, we will assume that the file was extracted to directory "source/" in the working directory and is named "3fs_5keV_nz35_0000001.h5".

Beamline propagation
```````````````````````````````````

Using the Calculator
''''''''''''''''''''

Propagation of x-ray pulses through the SPB-SFX beamline will be performed by means of the
:code:`XFELPhotonPropagator` class (:py:class:`SimEx.Calculators.XFELPhotonPropagator.XFELPhotonPropagator`), that comes with simex_platform. It interfaces the wavefront propagation code
WPG. Below is a commented python script
that demonstrates setup and execution of the propagation.


.. literalinclude:: Tutorial/s2e_example/resources/propagation.py
   :linenos:

:download:`Download script<Tutorial/s2e_example/resources/propagation.py>`

The definition of the beamline (line 7) loads a WPG beamline from the beamline collection. Besides
the beamline, the user has to specify the location of the source files (see `Preparing the source
input`_). The variable :code:`input_path` can be either a file or a directory. In the latter case, all valid source
files in the directory will be processed.

The :code:`XFELPhotonPropagator` class
requires two input parameters, a parameters object (of type
:code:`WavePropagationParameters`, defined in line 10),
and the :code:`input_path`. After construction, the input files are read in using the method :code:`_readH5`,
and the calculation is executed by calling the :code:`backengine` method.

A third input parameter for the :code:`XFELPhotonPropagator`  class, :code:`output_path` can be used to specify where the results of the wavefront
propagation shall be saved. By default, they are stored in a directory called "prop/" below the
current working directory.

Analysis of wavefront propagation results
'''''''''''''''''''''''''''''''''''''''''

Confirm that the results of the wavefront propagation are saved to "prop/".
The script :code:`ScriptCollection/DataAnalysis/propagation/prop_diagnostics.py` provides utilities
to quickly diagnose single propagated x-ray pulses. The syntax is::

    $> prop_diagnostics.py <options> prop_out.h5

Running :code:`diagnostics.py` without arguments will return a small instruction how to use it.

E.g.::
    $> prop_diagnostics.py -I prop_out.h5

generates an intensity map of the radiation field in the focus. Likewise,::

    $> prop_diagnostics.py -R prop_out.h5

plots the intensity distribution in reciprocal (qx-qy) space.

The options :code:`-T, -X, -S` produce viewgraphs of the total power as function of time, the on-axis power as function of time,
and the power spectrum as a function of photon energy, respectively.

Running the script on the source file::

    $> prop_diagnostics.py <options> source/s2e_felsource.h5

will produce the same figures for the source. Comparison of source and propagated pulses can give
some information about the reliability of the propagation. E.g. a drastic loss in power would indicate that the area over which the wavefront was calculated, is too small or that the wavefront is insufficiently sampled.
The resulting graphs should look similar to these:

FEL power (averaged over x,y coordinates) as function of time, source (left) vs. focus (right)

.. image:: Tutorial/s2e_example/resources/power_vs_time.png


FEL on-axis power density as function of time, source (left) vs. focus (right)

.. image:: Tutorial/s2e_example/resources/powerdensity_vs_time.png


Intensity distribution, source (left) vs. focus (right)

.. figure:: Tutorial/s2e_example/resources/intensity_x-y.png


Intensity distribution in reciprocal space, source (left) vs. focus (right)

.. figure:: Tutorial/s2e_example/resources/intensity_qx-qy.png


Confirm that the pulse duration is approximately 9 fs (full width at half maximum, FWHM),
that the focus has a FWHM of approximately 100 nm and as well as that the reciprocal intensity distribution is smooth
and shows no artificial high frequency modes.

Photon-Matter Interaction
`````````````````````````

Using the Calculator
''''''''''''''''''''

simex_platform employs the atomistic simulation codes :code:`XMDYN` and :code:`XATOM` to simulate
the interaction of the sample with the x-ray pulse. Unfortunately, these codes are not Open Source
and simex_platform only provides a demo version of the code. The corresponding Calculator is the
:code:`XMDYNDemoPhotonMatterInteractor` (see API reference here: :py:class:`SimEx.Calculators.XMDYNDemoPhotonMatterInteractor.XMDYNDemoPhotonMatterInteractor`).

The following script shows how to use the :code:`XMDYNDemoPhotonMatterInteractor` to produce
photon-matter trajectories which will then be used to calculate the diffraction.

.. literalinclude:: Tutorial/s2e_example/resources/pmi.py
   :linenos:

:download:`Download script<Tutorial/s2e_example/resources/pmi.py>`


Analysing the results
'''''''''''''''''''''

Let's take a look at the results of the photon matter interaction calculation.
The script :code:`ScriptCollection/DataAnalysis/pmi/pmi_diagnostics.py` plots the average number of
bound electrons per atom species in the sample and the average displacement as a function of time.
The syntax is::

    $> pmi_diagnostics.py <project_directory> test

Since this is the demo version of the pmi code, the results are pretty boring, since no radiation damage happens, neither ionization nor atomic displacement.

Diffraction
```````````

Using the Calculator
''''''''''''''''''''

The next step is to calculate the diffraction of photons from the sample as it is exposed to the
beam, i.e. radiation damage and diffraction or scattering happen simultaneously. In the previous
section, we have
precalculated the atomic structure (atom positions as a function of time) and the electronic
structure as a function of time, and based on this information we can now proceed to calculate
the amount of scattered radiation into a given detector pixel as a function of time. The detector
signal will then be calculated by integrating over the exposure time or pulse duration, whichever is
shorter.

We use the simex Calculator :code:`SingFELPhotonDiffractor` (see API doc
:py:class:`SimEx.Calculators.SingFELPhotonDiffractor.SingFELPhotonDiffractor`). The following script
demonstrates its usage:

.. literalinclude:: Tutorial/s2e_example/resources/diffraction.py
    :linenos:

:download:`Download script<Tutorial/s2e_example/resources/diffraction.py>`


Analyzing the results
'''''''''''''''''''''

Run the script :code:`ScriptCollection/DataAnalysis/scatteing/diffr_diagnostics.py` to generate
statistical information about the number of scattered photons and a histogram. Envoke the script without any
arguments to get obtain usage instructions.

For example::

    $> diffr_diagnostics.py -p -P 1 diffr.h5

will show the detected photons in the detector pixel array for the first pattern.

A more complicated example is::

    $> diffr_diagnostics.py -p -P "range(1,11)" --logscale --operation "numpy.mean" diffr.h5

this will plot the average detector image on a logarithmic color scale for patterns 1 to 10.

To see a histogram over the number of photons per pattern::

    $> diffr_diagnostics.py -S -P "range(1,11)"  diffr.h5

.. figure:: Tutorial/s2e_example/resources/diffr_histogram_9fs.png
   :width: 50%
   :alt: Histogram over number of registered photons per diffraction pattern.
   :align: center

To create an animation of all selected patterns::

    $> diffr_diagnostics.py -A animation.gif -P "range(1,11)"  diffr.h5


