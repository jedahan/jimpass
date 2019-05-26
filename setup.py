""" Setup.py """
from setuptools import setup, find_packages


setup(
    name="Pybiro",
    author="Remy Rojas",
    install_requires=[
        "Click",
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pbr=pybiro.cli:cli'
        ]
    },
)