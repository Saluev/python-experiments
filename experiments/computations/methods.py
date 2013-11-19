# -*- coding: utf-8 -*-

import math
import numpy as np
from numpy import array
from utilities import dot

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
  
  def operator(self, operator, **kwargs):
    # TODO: choise between sparse and dense matrices, float and complex values
    blen = len(self.basis)
    matrix = np.zeros([blen] * 2, dtype = np.complex128)
    if operator.isLinear():
      for i in range(blen):
        print "Evaluating row #%d..." % i
        b1 = self.basis[i]
        for j in range(blen):
          b2 = self.basis[j]
          matrix[i, j] = dot(operator(b2), b1)
      return matrix
    else:
      # wat?
      raise ValueError("Galerkin method can't be applied to nonlinear problems")


