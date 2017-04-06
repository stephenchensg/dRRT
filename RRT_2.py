import math, sys, random
from math import *
#import pygame
#from pygame import *
import matplotlib.pyplot as plt


class Node(object):
	def __init__(self,point,parent):
		super(Node,self).__init__()
		self.point = point
		self.parent = parent


X = 800
Y = 800
windowSize = [X, Y]

robot_radius = 5
obstacle_radius = 30

goal_radius = 10
min_dist = 1.0
Maxnode = 10000

count = 0
cirObs = []

def dist(p1,p2):
	return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def point_circle_collision_check(p1,p2,radius):
	distance = dist(p1,p2)
	if (distance <= radius):
		return True
	return False

def circle_circle_collision_check(p1,p2,robot_radius,obstacle_radius):
	distance = dist(p1,p2)
	if (distance <= (robot_radius + obstacle_radius)):
		return True
	return False

def collides(p):
	for cir in cirObs:

def initializing_obstacles(configuration):

	 global cirObs
	 cirObs = []
	 if (configuration == 0):
	 	cirObs.append((X/4,Y/4,30),X/4,Y/4,30))

def main():
    global count

    startpoint = Node((1,1),None)
    goalpoint = Node()


plt.plot([1,2,3,4])
plt.show()

raw_input()
