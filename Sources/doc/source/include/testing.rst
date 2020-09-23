Testing
-------
Testing the installation.

By default, the installation also creates the unittest suite.
You can switch this option off by appending the flag `-DINSTALL_TESTS=OFF` to the cmake command.

It is advised to run the test suite to check your installation in your source file path::

    $> ./get_testdata.sh
    $> cd Tests/python/unittest
    $> python Test.py -v 2>&1 | tee Test.log

This will run the entire test suite and pipe the output to the file `Test.log`.
A final test report is appended.
