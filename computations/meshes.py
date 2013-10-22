# -*- coding: utf-8 -*-

import math
import numpy as np
from numpy import array
from regions import *

# grids
class Mesh(object):
  
  def __init__(self):
    self.vertices = []
    self.shapes = []
  
  class Element(object):
    pass
  
  class Square(Element):
    def __init__(self, center, radius):
      self.center, self.radius = center, radius
  class Triangle(Element):
    def __init__(self, v0, v1, v2):
      # TODO: sort points in CW or CCW order
      self.v0, self.v1, self.v2 = v0, v1, v2

class UniformGrid(Mesh):
  
  def __init__(self, h):
    super(UniformGrid, self).__init__()
    self.h = h
  
  def __call__(self, region, **kwargs):
    cube = region.container()
    h = self.h
    n, d = int(cube.edge / h), cube.d
    # FIXME: using a dumb way
    a = np.zeros([n] * d)
    it = np.nditer(a, flags=['multi_index'])
    while not it.finished:
      pt = it.multi_index * h
      if pt in cube:
	self.vertices.append(array(pt))
      pt += 0.5 * h # TEST
      if pt in cube:
	self.shapes.append(Mesh.Square(pt, 0.5 * h))
    if len(self.vertices) == 0 and len(self.shapes) == 0:
      raise ValueError("Mesh type incompatible with given region!")
    return self
