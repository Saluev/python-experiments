# -*- coding: utf-8 -*-

import math
import numpy as np

from functions import *
from equations import *

def dot(f, g, **kwargs): # this function is kinda awkward
  """This function calculates dot product of two functions."""
  if hasattr(f, '__dot_priority__') or hasattr(g, '__dot_priority__'):
    try:
      priority_f = f.__dot_priority__ if hasattr(f, '__dot_priority__') else 0
      priority_g = g.__dot_priority__ if hasattr(g, '__dot_priority__') else 0
      if priority_f >= priority_g:
        return f.__dot__(g, **kwargs)
      else:
        return g.__dot__(f, **kwargs).conjugate()
    finally:
      pass
  if hasattr(f, '__dot__'):
    try:
      return f.__dot__(g, **kwargs)
    finally:
      pass
  if hasattr(g, '__dot__'):
    try:
      return g.__dot__(f, **kwargs).conjugate()
    finally:
      pass
  if "grid" in kwargs:
    #try:
      grid = kwargs["grid"]
      result = 0.0
      for pt, h in grid:
        result += f(*pt) * g(*pt).conjugate() * h
      return result
    #finally:
    #  pass
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




