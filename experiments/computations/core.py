# -*- coding: utf-8 -*-

import math
import numpy as np
from numpy import array


from regions import *
from meshes  import *
from equations import *


class Problem(object):
  
  region      = None
  mesh        = None
  discretizer = None
  equation    = None
  solver      = None
  
  def solve(self, rhs, initial_solution = 0, **kwargs):
    mesh = self.mesh(self.region, **kwargs)
    rhs = self.discretizer(mesh, rhs, **kwargs)
    x = self.discretizer(mesh, initial_solution, **kwargs)
    operator = self.discretizer(mesh, equation, **kwargs)
    solution = self.solver(operator, x, rhs, **kwargs)
    return solution

