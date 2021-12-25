# -*- coding: utf-8 -*-

import os
from codecs import open

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# load the package's __version__.py module as a dictionary
about = {}
with open(os.path.join(here, "hwtest", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)

try:
    with open("README.md", "r") as f:
        readme = f.read()
except FileNotFoundError:
    readme = about["__description__"]

extras = {
    "testing": [
        "tox",
        "black",
        "isort",
        "mypy",
        "flake8",
        "pytest",
    ],
}

# fmt: off
# Pillow must be on its own line otherwise Debian packaging will fail
setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    python_requires="~=3.7,",
    license=about["__license__"],
    classifiers=[
        "Natural Language :: English",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    project_urls={
        "Documentation": "https://docs.wlanpi.com",
        "Source": "https://github.com/wlan-pi/wlanpi-hwtest",
    },
    include_package_data=True,
    extras_require=extras,
    install_requires=[
        "pytest==6.2.5",
        "pytest-html==3.1.1",
        "pytest-json-report==1.4.1",
        "luma.oled==3.8.1",
        "rpi.gpio==0.7.1a4",
        "gpiozero==1.6.2",
        "Pillow==8.4.0", 
    ],
    entry_points={"console_scripts": ["hwtest=hwtest.__main__:main"]},
)
