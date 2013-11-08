import math
# -*- coding: utf-8 -*-

import math
import numpy as np
from numpy import array
import numbers

from functions import Function

# equations
class Equation(object):
  # TODO: equation systems support
  
  def __init__(self, left, right, region = None):
    self.left, self.right, self.region = left, right, region
  
  def __str__(self):
    result = "%s = %s" % (str(self.left), str(self.right))
    if self.region:
      result += " at %s" % str(self.region)
    return result
  
  def __call__(self, region):
    self.region = region
    return self
  
  def rhs(self, **kwargs):
    return self.right if self.left.isUnknown() else self.left
  
  def operator(self, **kwargs):
    lhs = self.left if self.left.isUnknown() else self.right
    if isinstance(lhs, MappedFunction):
      return lhs.operator
    elif isinstance(lhs, UnknownFunction):
      return identity
    else:
      raise NotImplementedError




# unknowns
class UnknownFunction(Function):
  
  def isUnknown(self):
    return True
  
  def __str__(self):
    return "u"
  
  def __eq__(self, what):
    return Equation(self, what)


class MappedFunction(Function):
  """
    Operator A such that (Au)(x) = f(x) u(x) for some f.
  """
  def __init__(self, operator, f):
    self.operator, self.f = operator, f
  
  def isUnknown(self):
    return self.f.isUnknown()
  
  def __eq__(self, what):
    if isinstance(self.f, UnknownFunction):
      return Equation(self, what)
  
  def __call__(self, *args):
    return self.operator.evaluate(self.f, *args)
  
  def __str__(self):
    if isinstance(self.operator, (LinearCombination, Superposition, ScalarOperator)):
      return "(%s)(%s)" % (str(self.operator), str(self.f))
    elif self.operator is not None:
      return "%s(%s)" % (str(self.operator), str(self.f))
    else:
      return str(self.f)
  
  def __dot__(self, g, **kwargs):
    if hasattr(self.operator, '__dot__'):
      return self.operator.__dot__(self.f, g, **kwargs)
    else:
      return dot(g, self).conjugate()
  
  @property
  def __dot_priority__(self):
    if hasattr(self.operator, '__dot_priority__'):
      return self.operator.__dot_priority__ 
    else:
      return 0




# operators
class Operator(object):
  
#  def __dot__(self, f, g, **kwargs):
#    """This function should calculate (Af, g) in a way."""
#    raise NotImplementedError
  
  def isLinear(self):
    return False
  
  def __init__(self, name = "?"):
    self.name = name
  
  def __call__(self, f):
    return MappedFunction(self, f)
  
  def __eq__(self, what):
    return Equation(self, what)
  
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
      coef = complex(what)
      try:
        coef = float(what)
      finally:
        return LinearCombination((self, coef))
    except:
      # WTF?
      raise ValueError("Operator can be multiplied only by an operator or a number")


class LinearOperator(Operator):
  
  def isLinear(self):
    return True
  # TODO: use linearity for formulae optimization


class IdentityOperator(LinearOperator):
  
  def __init__(self):
    super(IdentityOperator, self).__init__("I" or "E")

identity = IdentityOperator()


class ScalarOperator(LinearOperator):
  """
    Operator A such that (Au)(x) = f(x) u(x) for some f.
  """
  def __init__(self, f):
    self.f = f
  
  def __str__(self):
    return str(self.f)
  
  def evaluate(self, f, *args):
    return f(*args) * self.f(*args)


class LinearCombination(Operator):
  
  def __dot__(self, f, g, **kwargs):
    values = [dot(operator(f), g) for operator in self.operators]
    return np.dot(values, self.coefficients)
  
  __dot_priority__ = 10
  
  def isLinear(self):
    return all([op.isLinear() for op in self.operators])
  
  def __check_scalar(self, op, coef):
    if isinstance(op, numbers.Number):
      coef *= op
      op = identity
    return op, coef
  
  def __str__(self):
    s = ""
    just_started = True
    for op, coef in zip(self.operators, self.coefficients):
      if abs(coef) < 1E-6:
        continue
      if not just_started:
        s += " + "
      if abs(coef - 1.) >= 1E-6:
        s += "%s * " % str(coef)
      s += str(op)
      just_started = False
    return s
  
  def __init__(self, *args):
    self.operators = []
    self.coefficients = []
    for op, coef in args:
      op, coef = self.__check_scalar(op, coef)
      self.operators.append(op)
      self.coefficients.append(coef)
  
  def __neg__(self):
    return LinearCombination(*zip(self.operators, list( - array(self.coefficients))))
  
  def __add_or_sub(self, what, sign):
    if isinstance(what, LinearCombination):
      ops, coefs = zip(*map(lambda t: self.__check_scalar(*t), zip(what.operators, what.coefficients)))
      #ops = self.operators + what.operators
      #coefs = self.coefficients + list(sign * array(what.coefficients))
      ops = self.operators + ops
      coefs = self.coefficients + coefs
    elif id(what) in map(id, self.operators): # because "==" is overloaded...
      ops = list(self.operators)
      coefs = list(self.coefficients)
      coefs[ops.index(what)] += sign
    else:
      what, sign = self.__check_scalar(what, sign)
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
  
  def __call__(self, f):
    operator = self.operators[0]
    if len(self.operators) > 1:
      subsup = Superposition(*self.operators[1:])
      return operator(subsup(f))
    else:
      return operator(f)
  
  """def evaluate(self, f, *args):
    operator = self.operators[0]
    if len(self.operators) > 1:
      subsup = Superposition(*self.operators[1:])
      return operator.evaluate(subsup(f), *args)
    else:
      return operator.evaluate(f, *args)
  
  def __dot__(self, f, g, **kwargs):
    operator = self.operators[0]
    if len(self.operators) > 1:
      subsup = Superposition(*self.operators[1:])
      return dot(operator(subsup(f)), g)
    else:
      return dot(operator(f), g)"""
  
  def isLinear(self):
    return all([op.isLinear() for op in self.operators])
  
  def __str__(self):
    return " ".join(map(str, self.operators))
    
  def __init__(self, *args):
    self.operators = list(args)
  
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


class Divergence(LinearOperator):
  
  def __init__(self):
    super(Divergence, self).__init__("div")
  
  def __call__(self, f, **kwargs):
    if hasattr(f, 'div'):
      return f.div()
    else:
      return super(Divergence, self).__call__(f, **kwargs)
  
  def __dot__(self, f, g, **kwargs):
    # (div f, g) = - (f, grad g)
    if hasattr(f, 'div'):
      return  dot(f.div(), g)
    if hasattr(g, 'grad'):
      return -dot(f, g.grad())
  
  __dot_priority__ = 5


class Gradient(LinearOperator):
  
  def __init__(self):
    super(Gradient, self).__init__("grad")
  
  def __call__(self, f, **kwargs):
    if hasattr(f, 'grad'):
      return f.grad()
    else:
      return super(Gradient, self).__call__(f, **kwargs)
  
  def __dot__(self, f, g, **kwargs):
    # (grad f, g) = - (f, div g)
    if hasattr(f, 'grad'):
      return  dot(f.grad(), g)
    if hasattr(g, 'div'):
      return -dot(f, g.div())
  
  __dot_priority__ = 5


class FredholmOperator(LinearOperator):
  
  def __init__(self, kernel):
    super(FredholmOperator, self).__init__()
    self.kernel = kernel
  
  def __str__(self):
    return "(S %s ..dx)" % str(self.kernel)
  
  def __dot__(self, f, g, **kwargs):
    # calculating (Kf, g)... # DON'T USE THIS
    biv = outer(f, g)
    return dot(self.kernel, biv)
  
  def evaluate(self, f, *args):
    return self.kernel.__dot_x__(f, *args)




# instantiating
div = Divergence()
grad = Gradient()

from utilities import dot, outer

