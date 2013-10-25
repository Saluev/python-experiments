# -*- coding: utf-8 -*-

import math
import numpy as np
from numpy import array


from regions import *
from meshes  import *
from equations import *


class Problem(object):
  
  region      = None    # the region to build mesh in
  mesh        = None    # the mesh builder class
  basis       = None    # the basis function class
  method      = None    # the method for discretization
  equation    = None    # the equation to discretize
  solver      = None    # the linear systems solver
  
  def solve(self, rhs, initial_solution = 0, **kwargs):
    # TODO: boundary conditions
    mesh     = self.mesh(region = self.region, **kwargs)
    basis = [self.basis(el, **kwargs) for el in mesh.elements] # TODO: more flexible
    equation = self.equation(region = self.region, **kwargs)
    rhs      = equation.rhs(**kwargs)
    method   = self.method(basis = basis, **kwargs)
    rhs      = method.rhs(rhs = rhs, **kwargs)
    operator = method.operator(equation = equation, **kwargs)
    initial  = operator.initial(**kwargs)
    solution = self.solver(operator = operator, initial = initial, rhs = rhs, **kwargs)
    return solution

