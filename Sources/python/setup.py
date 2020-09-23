from setuptools import setup

from SimEx import version

setup(
    name='SimEx',
    packages=['SimEx',
             ],
    license='GPL-v3',
    version=version.__version__
)
