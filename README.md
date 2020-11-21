Convert Codemeta
=====================================================

Python utility for converting and validating codemeta.json files using the codemeta crosswalk

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Latest release](https://img.shields.io/badge/Latest_release-0.0.1-b44e88.svg?style=flat-square)](http://shields.io)


Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Known issues and limitations](#known-issues-and-limitations)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Authors and history](#authors-and-history)
* [Acknowledgments](#authors-and-acknowledgments)


Introduction
------------

This application copies some functionality of
[codemetar](https://github.com/ropensci/codemetar), but in python. It includes
codemeta validation and crosswalk functions.

Installation
------------

Clone from github

Type `pip install .`

Usage
-----

Validate codemeta in a python script: `validate_codemeta(codemeta)`

Convert to codemeta in a python script by providing the input format:
`crosswalk(data, "bio.tools")`

Convert from codemeta to a different format in a python script by providing both formats:
`crosswalk(data, "codemeta", "Zenodo")`

Run tests by typing `pytest tests`


Known issues and limitations
----------------------------

In active development

Getting help
------------

Submit issues on GitHub, or send me a note at tmorrell@caltech.edu

Contributing
------------

Contributions are welcome! See [Contributing](CONTRIBUTING) for more details.

License
-------

Software produced by the Caltech Library is Copyright (C) 2019, Caltech.  This software is freely distributed under a BSD/MIT type license.  Please see the [LICENSE](LICENSE) file for more information.


Authors and history
---------------------------

Tom Morrell

Acknowledgments
---------------

This work was funded by the [Alfred P. Sloan Foundation](https://sloan.org/) as
part of the [2019 Scientific Software Registry Collaboration
Workshop](http://asclnet.github.io/SWRegistryWorkshop). It is maintained by the California Institute of Technology Library.


<div align="center">
  <br>
  <a href="https://www.caltech.edu">
    <img width="100" height="100" src=".graphics/caltech-round.png">
  </a>
</div>
