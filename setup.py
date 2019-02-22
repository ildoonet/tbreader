from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import setuptools

_VERSION = '0.1'

with open("README.md", "r") as fh:
    long_description = fh.read()

# 'opencv-python >= 3.3.1'
REQUIRED_PACKAGES = [
]

DEPENDENCY_LINKS = [
]

setuptools.setup(
    name='tbreader',
    version=_VERSION,
    description='Simple TensorBoard Log Parser',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=REQUIRED_PACKAGES,
    dependency_links=DEPENDENCY_LINKS,
    url='https://github.com/ildoonet/tbreader',
    license='MIT License',
    package_dir={},
    packages=setuptools.find_packages(exclude=['tests']),
)
