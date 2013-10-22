# -*- coding: utf-8 -*-

import math
import numpy as np
from numpy import array

# regions
class Region(object):
  
  def container(self):
    """ This function should return Cube containing the whole region. """
    raise NotImplementedError
  
  def project(self, pt):
    """ This function should return point of the region closest to the given one. """
    raise NotImplementedError
  
  def __contains__(self, pt):
    raise NotImplementedError


class Cube(Region):
  
  def __init__(self, edge = 1., d = 3):
    self.edge = edge
    self.__min = np.zeros(d)
    self.__max = edge * np.ones(d)
    self.d = d
  
  def container(self):
    return self
  
  def project(self, pt):
    return np.maximum(self.__min, np.minimum(self.__max, pt))
  
  def __contains__(self, pt):
    return np.all(self.__min <= pt) and np.all(pt <= self.__max)


class Sphere(Region):
  
  def __init__(self, radius = 1., d = 3):
    self.radius = radius
    self.d = d
    
  def container(self):
    return Cube(self.radius * 2., self.d).shift(self.radius)
  
  def project(self, pt):
    pt = np.array(pt)
    return pt * (self.radius / np.linalg.norm(pt))
  
  def __contains__(self, pt):
    pt = np.array(pt)
    return pt.size == self.d and abs(np.linalg.norm(pt) - self.radius) < 1E-7
