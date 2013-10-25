import math
# -*- coding: utf-8 -*-

import math
import numpy as np
from numpy import array

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
  
  def rhs(self, rhs, **kwargs):
    pass
  
  def operator(self, equation, **kwargs):
    pass
