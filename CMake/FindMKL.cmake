# - Find MKL
# very simple check if environment variable MKLROOT is set
#
#  
#  MKL_ROOT        - Set to $ENV(MKLROOT)
#  MKL_FOUND       - True if FFTW found.

if (MKL_ROOT)
  # Already in cache, be silent
  set (MKL_FIND_QUIETLY TRUE)
endif (MKL_ROOT)

if(DEFINED ENV{MKLROOT})
    set (MKL_ROOT $ENV{MKLROOT})
endif()


# handle the QUIETLY and REQUIRED arguments and set MKL_FOUND to TRUE if
# all listed variables are TRUE
include (FindPackageHandleStandardArgs)
find_package_handle_standard_args (MKL DEFAULT_MSG MKL_ROOT)

mark_as_advanced (MKL_ROOT)

