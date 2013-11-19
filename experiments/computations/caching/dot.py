# -*- coding: utf-8 -*-

import math
import numpy as np

import experiments.computations as exc
from exc.utilities import dot


def dot_caching(f, g, __rec = False, **kwargs):
  # caching system
  
  def compile_cached(s):
    code = compile(s, '<string>', 'eval')
    def dot_cached(f, g, **kwargs): return eval(code)
    return dot_cached
  
  if not __rec:
    if isinstance(f, type) and not isinstance(g, type):
      return compile_cached("(%s).conjugate()" % dot_caching(g, f, __rec = True, **kwargs))
    elif isinstance(g, type):
      return compile_cached(dot_caching(f, g, __rec = True, **kwargs))
    else:
      value = dot(f, g)
      def dot_cached(f, g, **kwargs): return value
      return dot_cached
  else:
    priority_f = getattr(f, '__dot_priority__', 0)
    priority_g = getattr(g, '__dot_priority__', 0)
    if priority_f >= priority_g and hasattr(f, '__dot_caching__') or not hasattr(g, '__dot_caching__'):
      try:
        return f.__dot_caching__(g, fname = 'f', gname = 'g', **kwargs)
      except NotImplementedError, ValueError: pass
    if hasattr(g, '__dot_caching__'):
      try:
        return "(%s).conjugate()" % g.__dot_caching__(f, fname = 'g', gname = 'f', **kwargs)
      except NotImplementedError, ValueError: pass
    raise UserWarning("Couldn't optimize `dot`.")
    return "dot(f, g)"
