# -*- coding: utf-8 -*-

import math
import numpy as np

from functions import *
from equations import *


def dot(f, g, **kwargs):
  """This function calculates dot product of two functions."""
  priority_f = getattr(f, '__dot_priority__', 0)
  priority_g = getattr(g, '__dot_priority__', 0)
  if priority_f >= priority_g and hasattr(f, '__dot__') or not hasattr(g, '__dot__'):
    try:
      return f.__dot__(g, **kwargs)
    except NotImplementedError, ValueError: pass
  if hasattr(g, '__dot__'):
    try:
      return g.__dot__(f, **kwargs).conjugate()
    except NotImplementedError, ValueError: pass
  raise NotImplementedError("dot operation is not implemented in any of the arguments")




def outer(f, g, **kwargs):
  """This function returns Function object implementing q(x, y) = f(x) * g(y)."""
  result = BivariateFunction()
  def evaluate(self, x, y):
    return f(x) * g(y)
  result.__call__ = evaluate
  result.__call__.__doc__ = "%s ⊗ %s" % (f.__call__.__doc__, g.__call__.__doc__)
  result.factor_x = f
  result.factor_y = g
  return result




