# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 13:48:43 2015

@author: admin-bellei
"""

from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction

def nCk(n,k): 
  return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)) ) )