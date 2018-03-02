#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(name="sugestio",
      version="0.6",
      description="Sugestio library for python",
      url="https://github.com/sugestio/sugestio-python",
      packages=find_packages(),
      install_requires=['oauth2'],
      license = "MIT License",
      keywords="sugestio recommendations library")
