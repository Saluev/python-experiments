import math
# -*- coding: utf-8 -*-

import math
import numpy as np
from numpy import array

# equations
class Operator(object):
  
  def __init__(self, name):
    self.name = name
  
  def __str__(self):
    return self.name
  
  def __neg__(self):
    return LinearCombination((self, -1.))
  
  def __add__(self, what):
    return LinearCombination((self, 1.), (what, 1.))
  
  def __radd__(self, what):
    return self.__add__(what)
  
  def __sub__(self, what):
    return LinearCombination((self, 1.), (what, -1.))
  
  def __rsub__(self, what):
    return self.__neg__().__add(what)
  
  def __mul__(self, what):
    if isinstance(what, Operator):
      return Superposition(self, what)
    else:
      return self.__rmul__(what)
  
  def __rmul__(self, what):
    try:
      coef = float(what)
      return LinearCombination((self, coef))
    except:
      # WTF?
      raise ValueError("Operator can be multiplied only by an operator or a number")


class LinearCombination(Operator):
  
  def __str__(self):
    s = "<"
    just_started = True
    for op, coef in zip(self.operators, self.coefficients):
      if abs(coef) < 1E-7:
	continue
      if not just_started or coef < 0:
	s += " - " if coef < 0 else " + "
      if abs(abs(coef) - 1.) >= 1E-7:
	s += "%g * " % abs(coef)
      s += str(op)
      just_started = False
    s += ">"
    return s
  
  def __init__(self, *args):
    self.operators = []
    self.coefficients = []
    for op, coef in args:
      self.operators.append(op)
      self.coefficients.append(coef)
  
  def __neg__(self):
    return LinearCombination(*zip(self.operators, list( - array(self.coefficients))))
  
  def __add_or_sub(self, what, sign):
    if isinstance(what, LinearCombination):
      ops = self.operators + what.operators
      coefs = self.coefficients + list(sign * array(what.coefficients))
    elif what in self.operators:
      ops = list(self.operators)
      coefs = list(self.coefficients)
      coefs[ops.index(what)] += sign
    else:
      ops = self.operators + [what]
      coefs = self.coefficients + [sign]
    return LinearCombination(*zip(ops, coefs))
  
  def __add__(self, what):
    return self.__add_or_sub(what,  1.)
  
  def __radd__(self, what):
    return self.__add_or_sub(what,  1.)
  
  def __sub__(self, what):
    return self.__add_or_sub(what, -1.)
  
  def __rsub__(self, what):
    return self.__neg__().__add__(what)


class Superposition(Operator):
  
  def __str__(self):
    return " ".join(map(str, self.operators))
    
  def __init__(self, *args):
    self.operators = args
  
  def __mul__(self, what):
    if isinstance(what, Superposition):
      ops = self.operators + what.operators
    elif isinstance(what, Operator):
      ops = self.operators + [what]
    else:
      return super(Superposition, self).__mul__(what)
    return Superposition(*ops)
  
  def __rmul__(self, what):
    if isinstance(what, Operator):
      ops = [what] + self.operators
      return Superposition(*ops)
    else:
      return super(Superposition, self).__rmul__(what)










