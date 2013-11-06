# -*- coding: utf-8 -*-

import math
import numpy as np
from numpy import array

class Function(object):
  
  def __call__(self, r):
    """?"""
    # This method's primary purpose is to document
    # what the function is doing.
    # The docstring is used in string representations.
    raise NotImplementedError
  
  def __str__(self):
    return self.__call__.__doc__ or "?"
  
  def isUnknown(self):
    return NotImplementedError
  
  # TODO think of set of methods

class BivariateFunction(Function):
  
  def __call__(self, r1, r2):
    raise NotImplementedError


def dot(f, g, **kwargs): # this function is kinda awkward
  if hasattr(f, '__dot__') and  hasattr(g, '__dot__') and \
    (hasattr(f.__dot__, 'priority') or hasattr(g.__dot__, 'priority')):
    try:
      priority_f = f.__dot__.priority if hasattr(f.__dot__, 'priotity') else 0
      priority_g = g.__dot__.priority if hasattr(g.__dot__, 'priotity') else 0
      if priority_f >= priority_g:
        return f.__dot__(g, **kwargs)
      else:
        return g.__dot__(f, **kwargs) # TODO: conjugate
    finally:
      pass
  if hasattr(f, '__dot__'):
    try:
      return f.__dot__(g, **kwargs)
    finally:
      pass
  if hasattr(g, '__dot__'):
    try:
      return g.__dot__(f, **kwargs) # TODO: conjugate
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
  raise NotImplementedError

