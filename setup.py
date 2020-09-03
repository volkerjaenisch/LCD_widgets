"""Installer for the inqbus.rpi.widgets package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
])


setup(
    name='inqbus.rpi.widgets',
    version='0.1',
    description="Widgets for RPi Character displays ",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: RaspberryPi",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    keywords='Python',
    author='Volker Jaenisch',
    author_email='volker.jaenisch@inqbus.de',
    url='https://inqbus.de',
    license='MIT',
    packages=find_packages('src'),
    package_dir = {'' : 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'rplcd',
        'smbus2',
        'pigpio',
        'pigpio-encoder',
        'zope.component',
        'pynput',
        'wrapt',
        'pytest',
        'sphinx',
        'sphinx-rtd-theme',
    ],
    extras_require={
        'test': [
        ],
    },
    entry_points="""
    [console_scripts]
    """,
)
