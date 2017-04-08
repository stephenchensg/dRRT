import math, sys, random
from math import *
#import pygame
#from pygame import *
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import time

G = nx.Graph()

G.add_node((1,1))
G.add_node((3,3))

G.add_edge((1,1),(4,4))
G.add_edge((1,1),(3,3))
G.add_edge((4,4),(2,2))
G.add_edge((2,2),(3,3))

a = []
a = G.nodes()

for ai in range(len(a)):
	print(a[ai])


a.remove((1,1))

print(a)

print(G.nodes())
print(len(G))
print(G.edges())

print(nx.shortest_path(G,source = (1,1), target= (3,3)))
