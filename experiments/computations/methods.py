import math
# -*- coding: utf-8 -*-

import math
import numpy as np
from numpy import array
from functions import dot

# discretization methods
class Method(object):
  
  def __init__(self, basis):
    self.basis = basis
  
  def rhs(self, **kwargs):
    raise NotImplementedError
  
  def operator(self, **kwargs):
    raise NotImplementedError


class GalerkinMethod(Method):
  
  def __init__(self, basis, **kwargs):
    super(GalerkinMethod, self).__init__(basis)
    self.numberOfUnknowns = len(basis)
    
  
  def rhs(self, rhs, **kwargs):
    return np.array([dot(rhs, f_n) for f_n in self.basis])
  
  def operator(self, equation, **kwargs):
    operator = equation.operator()
    if operator.isLinear():
      # quick method
      pass
    else:
      # slow method
      raise NotImplementedError


