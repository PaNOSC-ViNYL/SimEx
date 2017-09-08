Testing
-------
Testing the installation.

By default, the installation also creates the unittest suite.
You can switch this option off by appending the flag `-DINSTALL_TESTS=OFF` to the cmake command.

It is advised to run the test suite to check your installation::

    $> cd Tests/python/unittest
    $> python Test.py -v 2>&1 | tee Test.log

This will run the entire test suite and pipe the output to the file `Test.log`.
A final test report is appended.

NOTE 4 (Large Test Files): If you pulled the sources via git and encounter test failures where
the test log mentions something like "hdf file could not be read", make sure you issued a "git lfs pull" command at least once.
This is not a standard git command, you have to install git-lfs (e.g. via https://git-lfs.github.com/).



