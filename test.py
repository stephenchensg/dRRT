import math, sys, random
from math import *
#import pygame
#from pygame import *
import matplotlib.pyplot as plt
import numpy as np


class Node(object):
	def __init__(self, point, parent):
		super(Node, self).__init__()
		self.point = point
		self.parent = parent


x = Node((1,1),None)
y = Node((2,2),x)

obs = [x, y]


print(obs[0].point)
print(x)
print(len(obs))