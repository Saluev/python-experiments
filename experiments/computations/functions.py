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
    return False #NotImplementedError
  
  # TODO think of set of methods

class BivariateFunction(Function):
  
  def __call__(self, r1, r2):
    raise NotImplementedError


