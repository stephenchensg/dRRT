import math, sys, random
from math import *
#import pygame
#from pygame import *
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import time


#nx.draw(G)
#plt.show()

G = nx.Graph()

G.add_nodes_from([1],color  ='red')
G.add_nodes_from([2],color  ='yellow')
color = nx.get_node_attributes(G,'color')
print(G)

class Config(list):
    """List with arithmatic operators.
    
    """
    def __init__(self, q, activeIndices=None):
        super(Config, self).__init__(q[:])
        if activeIndices is None:
            self.activeIndices = range(len(self))
        else:
            assert isinstance(activeIndices, list)
            self.activeIndices = activeIndices[:]
            self.activeIndices.sort()

l = [1,2,3]
print(l.Locate(1))