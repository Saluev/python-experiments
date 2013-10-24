# -*- coding: utf-8 -*-

import math
import numpy as np
from numpy import array
from regions import *

_bytes_alignment = 4

class Vertices(object):
  def __init__(self, d = 3, cache = 1024, dtype = np.float64):
    self.d, self.dtype, self.cache, self.used = d, dtype, cache, 0
    self.d_aligned = d_aligned = \
        int(math.ceil(self.d / float(_bytes_alignment)) * _bytes_alignment)
    self.array = np.ndarray(d_aligned * cache, dtype = dtype)
    self.__objects = []
  
  def _resize_cache(self, new_size):
    cache = self.cache
    self.array = np.append(
      self.array,
      np.ndarray((new_size - cache) * self.d_aligned, dtype = self.dtype)
    )
    self.cache = new_size
  
  def _check_cache(self):
    used, cache = self.used, self.cache
    if used >= cache:
      self._resize_cache(int(cache * 1.25))
  
  def append(self, vertex):
    self._check_cache()
    d, used = self.d, self.used
    self.array[used * d : (used + 1) * d] = vertex
    self.__objects.append(vertex)
    vertex.container, vertex.index = self, used
    vertex.dtype = self.dtype
    self.used += 1
  
  def __getitem__(self, i):
    return self.__objects[i]


class Vertex(np.ndarray): # TODO: make vertex be just a view of vertices array
  
  def __new__(cls, coords):
    result = np.ndarray.__new__(cls, len(coords))
    result[:] = coords
    return result
  
  def __init__(self, *args, **kwargs):
    super(Vertex, self).__init__(*args, **kwargs)
    self.container = None
    self.index = None
    self.elements = []


class Elements(Vertices): # TODO?
  def __init__(self, *args, **kwargs):
    kwargs['dtype'] = np.int32
    super(Elements, self).__init__(self, *args, **kwargs)
  
  def append(self, element):
    self._check_cache()
    d, used = self.d, self.used
    # . . .


_sum = lambda x, y: x + y # TODO import from `operators` or something

# grids
class Mesh(object):
  
  def __init__(self):
    self.vertices = Vertices()
    self.elements = []
  
  class Element(object):
    pass
  
  class PolygonalElement(Element):
    def __init__(self):
      self.vertices = []
      self.adjacent = set()
    def _process_vertices(self):
      # find adjacent shapes
      candidates = set(reduce(_sum, map(lambda v: v.elements, self.vertices), []))
      is_adjacent = lambda el: len(set(el.vertices) & set(self.vertices)) >= 2
      self.adjacent = self.adjacent | set(filter(is_adjacent, candidates))
      self.adjacent.discard(self) # just in case...
      # register self in adjacent elements
      [el.adjacent.add(self) for el in self.adjacent]
      # register self in vertices
      [v.elements.append(self) for v in self.vertices]
    
  class Square(PolygonalElement):
    def __init__(self, center, radius):
      super(Mesh.Square, self).__init__()
      self.center, self.radius = center, radius
  
  class Triangle(PolygonalElement):
    def __init__(self, v1, v2, v3):
      super(Mesh.Triangle, self).__init__()
      # TODO: sort points in CW or CCW order
      self.vertices = [v1, v2, v3]
      self._process_vertices()
  
  class Pair(tuple, Element):
    pass


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




