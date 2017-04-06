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

X = 800
Y = 800
N = 10

windowSize = [X, Y]

robot_radius = 5
vicinity = 10

min_dist = 2.0
Maxnode = 10000

count = 0
cirObs = []

def dist(p1,p2):

	return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def extend(p1,p2):

	check = False
	if (dist(p1,p2)< 5):
		a1 = p2[0]
		a2 = p2[1]
	else: 
		angle = atan2(p2[1]-p1[1],p2[0]-p1[0])
		a1 = p1[0] + vicinity*cos(angle)
		a2 = p1[1] + vicinity*sin(angle)

	x1 = np.linspace(p1[0], a1, N)
	x2 = np.linspace(p1[1], a2, N)

	for x in x1:
		for y in x2:
			if (collides((x,y))==True):
				check = True
			else: check = False
		
	if (check == True):
		return (a1, a2)
	return p1

def local_connector(p1,p2):
	if (dist(p1,p2)<min_dist):
		return True
	return False

#def pc_collision_check(p1,p2,radius):

	#distance = dist(p1,p2)
	#if (distance >= radius):
		#return True
	#return False

def ce_collision_check(p1,p2,r_radius,ob_radius):

	distance = dist(p1,p2)
	if (distance >= (r_radius + ob_radius)):
		return True
	return False

def generate_random_point():
	while True:
		p = random.random()*X,random.random()*Y
		p_no_collision_env = collides(p)
		if (p_no_collision_env == True):
			return p

def collides(p):

	#for cir in cirObs:
		#if (ce_collision_check(p,(cir[0],cir[1]),robot_radius,cir[2])==True):
			#return True
		#return False

	if (ce_collision_check(p,(cirObs[0][0],cirObs[0][1]),robot_radius,cirObs[0][2])==True):
			if (ce_collision_check(p,(cirObs[1][0],cirObs[1][1]),robot_radius,cirObs[1][2])==True):
					if (ce_collision_check(p,(cirObs[2][0],cirObs[2][1]),robot_radius,cirObs[2][2])==True):
						return True
	return False


def initializing_obstacles(configuration):

	 global cirObs
	 cirObs = []
	 if (configuration == 0):
	 	cirObs.append((X/4,Y/4,80))
	 	cirObs.append((X/2,Y/2,80))
	 	cirObs.append((X/1.5,Y/1.5,30))


def main():

	global count
	count = 0
	initPost = Node((1,1), None)
	goalPost = Node((300,300), None)
	temp = Node(None,None)

	reach_goal = False
	initializing_obstacles(0)
	node = []
	node.append(initPost)

	while count < 3000: #count<Maxnode:
		if (local_connector(node[count].point, goalPost.point) == True):
			reach_goal = True
			break
		else: 
			rand = generate_random_point()
			temp.point = extend(node[count].point,rand)
			temp.parent = node[count]
			node.append(temp)
			print(temp.point)
			temp = Node(None,None)
			count = count + 1

	print(reach_goal)
	#plot the graph
	circle1 = plt.Circle((cirObs[0][0], cirObs[0][1]), cirObs[0][2], color='r')
	circle2 = plt.Circle((cirObs[1][0], cirObs[1][1]), cirObs[1][2], color='blue')
	circle3 = plt.Circle((cirObs[2][0], cirObs[2][1]), cirObs[2][2], color='g', clip_on=False)

	for n in node:
		plt.plot(n.point[0],n.point[1],"ro")
		#print(n.point[0],n.point[1])
	#fig, ax = plt.subplots()

	plt.plot(initPost.point[0],initPost.point[1], "bo")
	plt.plot(goalPost.point[0],goalPost.point[1], "bo")

	ax = plt.gca()
	ax.set_xlim((0, X))
	ax.set_ylim((0, Y))

	ax.add_artist(circle1)
	ax.add_artist(circle2)
	ax.add_artist(circle3)

# here must be something like circle.plot() or not?

	plt.show()
	raw_input()

if __name__ == '__main__':
	main()

