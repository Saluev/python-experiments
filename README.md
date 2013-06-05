# python-experiments

This is a package aimed to simplify running of multiple
computational experiments, with support of logging,
multithreading and collecting statistics.

## Installation

To install the package, just do the following in your favorite directory:

    git clone git://github.com/Saluev/python-experiments.git
    cd python-experiments
    sudo python setup.py install

## Usage

Usage example is provided in `test.py`. The main routine to do
experiments is `experiments.start`. Run it like the following:

```python
def my_big_computational_function(a, b, ..., z):
    ...
    return something # or not

import experiments
experiments.start(my_big_computational_function, iterations=10, cores=2, a=[a1, a2], b=my_b, c=range(10), ...)
```

&copy; [Saluev](http://github.com/Saluev)
