# study-gen

Study-gen is a package for programmatic generation of parametric studies. The base concept is to build upon a set
of "building blocks", that are simply standardized Python functions, and then combine them to build an easily reproducible, explicit study.

## Installation

study-gen is available on PyPI and can be installed using pip:

```bash
pip install study-gen
```

## Usage

Examples studies are provided in the ```example_folder```.

Let's illustrate what happens with the ```dummy``` study.
First, one needs to define the building blocks. In the ```dummy``` study, the building blocks are defined in the ```blocks``` folder. The building blocks are simply Python functions that take a set of parameters as input, and return a set of results as output. The building blocks should not be modified once they are ready, such that they can be easily reused in different studies. Here is a minimal example of building block:

```python
dict_imports = {"numpy": "import numpy as np"}
def power_function(b: float, c: float) -> float:
    return np.power(b, c)
power = Block("power", power_function, dict_imports=dict_imports)
```

The first parameter of the ```Block```contructor is simply the name of the block (to be used later in the study definition). The second parameter is the function that will be called when the block is used. The third parameter is a dictionary of imports that are needed by the block.

Once one has defined the required building blocks, one can define the study. The study is defined in a yaml file, which simply states the hierarchy of the study, and the parameters that will be scanned. A study contains several generations (self-contained Python scripts), organized into layers. Each layer will usually depend on the layer above it.

Here is an example of a study definition, with only one generation per layer. In this study, the parameters ```a``` and ```b``` are scanned, and the results are saved in a file. Note that the parameters that are not defined 
here are in the ```config.yaml``` file of the study.

```yaml
name: study_dummy
structure:
  layer_1:
    generations:
      - some_dummy_computations
    scans:
      a:
        linspace: [1, 2, 3]
      b:
        list: [1, 2]
  layer_2:
    generations:
      - some_more_computations

some_dummy_computations:
  script:
    multiply:
      args: [b, c]
      output: bc
    add:
      args: [a, bc]
      output: a_bc
    gamma:
      args: a_bc
      output: fact_a_bc
    save_npy:
      args: [fact_a_bc, path_fact_a_bc]
      output:

some_more_computations:
  script:
    load_npy:
      args: path_fact_a_bc
      output: fact_a_bc
    power:
      args: [a, fact_a_bc]
      output: a_bc_c
    save_pkl:
      args: [ a_bc_c, path_result]
      output:
```

The corresponding ```config.yaml``` file, containing the remaining parameters, is:

```yaml
some_ints:
  c: 4

a_float:
  d: 0.5

some_paths:
  path_fact_a_bc: "../fact_a_bc.npy"
  path_result: "result.pkl"
```

From here, what can generate the study in Python:

```python
from study_gen import StudyGen
from blocks import dict_ref_blocks
study = StudyGen(path_configuration='config.yaml', path_master='master.yaml', dict_ref_blocks = dict_ref_blocks)
study.create_study()
```

This will write a tree of folders and files in the ```dummy``` folder, containing the full study. The tree can be represented as follows:

```text
dummy
├── layer_1
│   ├── a_1_b_1
│   │   ├── some_dummy_computations.py
│   │   └── some_more_computation
│   │       └── some_more_computation.py
│   ├── a_1_b_2
│   │   ├── some_dummy_computations.py
│   │   └── some_more_computation
│   │       └── some_more_computation.py
│   ├── a_1.5_b_1
│   │   ├── some_dummy_computations.py
│   │   └── some_more_computation
│   │       └── some_more_computation.py
│   ├── a_1.5_b_2
│   │   ├── some_dummy_computations.py
│   │   └── some_more_computation
│   │       └── some_more_computation.py
│   ├── a_2_b_1
│   │   ├── some_dummy_computations.py
│   │   └── some_more_computation
│   │       └── some_more_computation.py
│   └── a_2_b_2
│       ├── some_dummy_computations.py
│       └── some_more_computation
│           └── some_more_computation.py
```

Each Python file in this script contains the blocks defined in the master file, called sequentially with the proper set of parameters. For instance, the topmost file ```some_dummy_computations.py``` contains the following code:

```python
# ==================================================================================================
# --- Imports
# ==================================================================================================

import math
import numpy as np
from typing import Any

# ==================================================================================================
# --- Blocks
# ==================================================================================================

def multiply_function(a: float, b: float) -> float:
    return a * b

def add_function(a: float, b: float) -> float:
    return a + b

def gamma_function(a: float) -> float:
    return math.gamma(a)


def save_npy_function(output: Any, path_output: str) -> None:
    np.save(path_output, output)

# ==================================================================================================
# --- Main
# ==================================================================================================

def main(b: float, c: float, a: float, path_fact_a_bc: str) -> None:

    bc = multiply_function(b, c)
    a_bc = add_function(a, bc)
    fact_a_bc = gamma_function(a_bc)
    save_npy_function(fact_a_bc, path_fact_a_bc)

# ==================================================================================================
# --- Parameters
# ==================================================================================================

# Declare parameters
b = 1
c = 4
a = 1
path_fact_a_bc = "fact_a_bc.npy"

# ==================================================================================================
# --- Script
# ==================================================================================================

if __name__ == "__main__":
    main(b, c, a, path_fact_a_bc)
```

## Advanced usage

More advanced uses are also possible. For instance, to avoid repeating sequences of blocks, one can merge several blocks into a single block. Alternatively, one can define a block that makes use of other blocks. All these examples are provided in the ```example_folder```.

## Motivation

The approach used in study-gen has several advantages:

- The building blocks can be reused in different studies, and easily shared between different users.
- The building blocks can be combined in different ways and/or with different parameter values, to build different studies.
- The building blocks can be tested individually, and the tests can be reused in different studies.
- A study made from a set of standardized building blocks is easier to understand and maintain than a study made from a set of ad-hoc scripts.
- A study made from a set of standardized building blocks is easily reproducible.
- A study made from a set of standardized building blocks can be easily  modified or extended with new building blocks (which any user can implement in a matter of minutes).
- A study generated from a set of standardized building blocks remains explicit (no internal functions or classes are hidden), and can be easily inspected and modified.

Finally, if a user doesn't want to code 'blocks' because it feels too complicated, he can just generate a template study from the set of available blocks, and personalize it the way he wants.

## Documentation

A proper documentation will be provided in the future. For now, the best way to understand how to use study-gen is to look at the examples provided in the ```example_folder```.
