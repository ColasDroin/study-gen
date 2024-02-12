# study-gen

Study-gen is a package for programmatic generation of parametric studies. The base concept is to build upon a set
of "building blocks", that are simply standardized Python functions, and then combine them to build a study. This approach has several advantages:

- The building blocks can be reused in different studies, and easily shared between different users.
- The building blocks can be combined in different ways and/or with different parameter values, to build different studies.
- The building blocks can be tested individually, and the tests can be reused in different studies.
- A study made from a set of standardized building blocks is easier to understand and maintain than a study made from a set of ad-hoc scripts.
- A stidu made from a set of standardized building blocks is easily reproducible.
- A study made from a set of standardized building blocks can be easily  modified or extended with new building blocks.

## Installation

study-gen is available on PyPI and can be installed using pip:

```bash
pip install study-gen
```

## Usage


