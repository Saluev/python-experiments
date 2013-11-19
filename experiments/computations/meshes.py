# -*- coding: utf-8 -*-

import math
import numpy as np
from numpy import array
from operator import add

from regions import *


################################################################################
############################### Vertices buffer ################################
################################################################################
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
    d, d_aligned, used = self.d, self.d_aligned, self.used
    self.array[used * d_aligned : used * d_aligned + d] = vertex
    self.__objects.append(vertex)
    vertex.container, vertex.index = self, used
    vertex.dtype = self.dtype
    self.used += 1
  
  def extend(self, lst):
    map(self.append, lst)
  
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




################################################################################
################################# Mesh objects #################################
################################################################################

# grids
class Mesh(object):
  
  def __init__(self):
    self.vertices = Vertices()
    self.elements = []
  
  ############################################################
  ###################### Mesh elements #######################
  ############################################################
  
  class Element(object):
    def __init__(self):
      self.adjacent = set()
    def __contains__(self, r):
      raise NotImplementedError
    def square(self):
      raise NotImplementedError
  
  
  class ComposedElement(Element):
    def __init__(self):
      super(Mesh.ComposedElement, self).__init__()
      self.elements = []
    def __contains__(self, r):
      return any([r in el for el in self.elements])
    def square(self):
      return sum([el.square() for el in self.elements])
    def _process_elements(self):
      # just in case: we should still count adjacent elements.
      # ... 
      pass
  
  
  class PolygonalElement(Element):
    def __init__(self):
      super(Mesh.PolygonalElement, self).__init__()
      self.vertices = []
    def __contains__(self, r):
      raise NotImplementedError # TODO
    def _process_vertices(self):
      # find adjacent shapes
      candidates = set(reduce(add, map(lambda v: v.elements, self.vertices), []))
      is_adjacent = lambda el: len(set(el.vertices) & set(self.vertices)) >= 2
      self.adjacent = self.adjacent | set(filter(is_adjacent, candidates))
      self.adjacent.discard(self) # just in case...
      # register self in adjacent elements
      [el.adjacent.add(self) for el in self.adjacent]
      # register self in vertices
      [v.elements.append(self) for v in self.vertices]
  
  
  class Triangle(PolygonalElement):
    def __init__(self, v1, v2, v3):
      super(Mesh.Triangle, self).__init__()
      # TODO: sort points in CW or CCW order?
      self.vertices = [v1, v2, v3]
      self._process_vertices()
      # linear algebra data
      self.__cross = np.cross(v2 - v1, v3 - v1)
      self.__mtx = np.array([v2 - v1, v3 - v1, self.__cross]).T
      self.__mtx_inv = np.linalg.inv(self.__mtx)
    def __contains__(self, r):
      v1, v2, v3 = self.vertices
      coords = np.dot(self.__mtx_inv, r)
      return 0. <= coords[0] <= 1. and \
             0. <= coords[1] <= 1. and \
               abs(coords[2]) < 1E-6
    def square(self):
      v1, v2, v3 = self.vertices
      return 0.5 * np.linalg.norm(self.__cross)
    def center(self):
      v1, v2, v3 = self.vertices
      return (v1 + v2 + v3) / 3.


#################### Uniform grid ####################
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




