#!/usr/bin/env python
#
# Copyright (c) 2015-2016, Axel Huebl, Remi Lehe, Carsten Fortmann-Grote
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

from dateutil.tz import tzlocal
import collections
import datetime
import h5py
import numpy
import re
import string
import sys, getopt, os.path

ext_list = {"ED-PIC": numpy.uint32(1),
            "HYDRO1D": numpy.uint32(2)}


def get_basePath(f, iteration):
    """
    Get the basePath for a certain iteration

    Parameter
    ---------
    f : an h5py.File object
        The file in which to write the data
    iteration : an iteration number

    Returns
    -------
    A string with a in-file path.
    """
    iteration_str = numpy.string_(str(iteration))
    return numpy.string_(f.attrs["basePath"]).replace(b"%T", iteration_str)

def setup_base_path(f, iteration, time, time_step):
    """
    Write the basePath group for `iteration`

    Parameters
    ----------
    f : an h5py.File object
        The file in which to write the data

    iteration : int
        The iteration number for this output
    """
    # Create the corresponding group
    base_path = get_basePath(f, iteration)
    f.create_group( base_path )
    bp = f[ base_path ]

    # Required attributes
    bp.attrs["time"] = time  # Value expressed in seconds
    bp.attrs["dt"] = time_step   # Value expressed in seconds
    bp.attrs["timeUnitSI"] = numpy.float64(1.0) # Conversion factor.

def setup_root_attr(f, extension=None):
    """
    Write the root metadata for this file

    Parameter
    ---------
    f : an h5py.File object
        The file in which to write the data
    """

    if extension is None:
        extension = "ED-PIC"

    # Required attributes
    f.attrs["openPMD"] = numpy.string_("1.0.0")
    f.attrs["openPMDextension"] = ext_list[extension]
    f.attrs["basePath"] = numpy.string_("/data/%T/")
    f.attrs["meshesPath"] = numpy.string_("meshes/")
    f.attrs["particlesPath"] = numpy.string_("particles/")
    f.attrs["iterationEncoding"] = numpy.string_("groupBased")
    f.attrs["iterationFormat"] = numpy.string_("/data/%T/")

    # Recommended attributes
    f.attrs["author"] = numpy.string_("NN")
    f.attrs["software"] = numpy.string_("simex_platform")
    f.attrs["softwareVersion"] = numpy.string_("0.2")
    f.attrs["date"] = numpy.string_( datetime.datetime.now(tzlocal()).strftime('%Y-%m-%d %H:%M:%S %z'))
