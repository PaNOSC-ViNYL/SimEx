""" Module for entity checks.
    @author CFG
    @institution XFEL
    @creation 20151006
"""

import exceptions

def checkAndSetInstance(cls, var=None, default=None):
    """
    Utility to check if the passed object is an instance of the given class (or derived class).

    @param cls : The class against which to check.
    @param var : The object to check.
    @param default : The default to use if no var is given.
    @return : The checked object or default.
    @throw : TypeError if var is not an instance of cls or a derived class.
    """

    if var is None:
        if default is None:
            return None
        elif not isinstance(default, cls):
            raise exceptions.TypeError("The default is not of correct type.")
        else: return default

    elif not isinstance(var, cls):
        raise exceptions.TypeError("The parameter 'var' is not of correct type.")

    return var
