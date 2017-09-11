import networkx as nx
import math, sys, random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
from math import *

class Node(object):
    def __init__(self, point, parent):
        super(Node, self).__init__()
        self.point = point
        self.parent = parent

class Vertice(object):
	def __init__(self,alpha,ap,position):
		self.alpha = alpha
		self.ap = ap
		self.position = position

def accept(transitions,initial,accepting,s):
	state = initial
	for c in s:
		state = transitions[state][c]
	return state in accepting

def transit(transitions,primary,p):
	state = primary
	c =frozenset([p])
	state = transitions[state][c]
	return state


def decomposition(X,Y,dfa): #decompose the graph into rectangles of 10 pixel.
	
	G = nx.Graph()
	h = [] #high_level_plan
	z = 0
	p_east = 'N'
	p_west = 'N'
	p_north = 'N'
	p_south = 'N'

	a = 100

	for i in range(X/a):
		for j in range(Y/a):
			d = (i*a,j*a)
			p = check_proposition(d)

			if (i != X/a): 
				p_east = check_proposition(((i+1)*a,j*a))
			if (i != 0): 
				p_west = check_proposition(((i-1)*a,j*a))
			if (j != Y/a): 
				p_north = check_proposition((i*a,(j+1)*a))
			if (j != 0): 
				p_south = check_proposition((i*a,(j-1)*a))

			if (z != transit(dfa,z,p)):
				z = transit(dfa,z,p)
			if (z != transit(dfa,z,p_east)):
				z = transit(dfa,z,p_east)
			if (z != transit(dfa,z,p_west)):
				z = transit(dfa,z,p_west)
			if (z != transit(dfa,z,p_north)):
				z = transit(dfa,z,p_north)
			if (z != transit(dfa,z,p_south)):
				z = transit(dfa,z,p_south)

			G.add_node((z,d))
			b1 = G.nodes()

			for m in range(3):
					#if ((m,(d[0]+a,d[1])) in b1):
					G.add_edge((z,d),(m,(d[0]+a,d[1])))
					#if ((m,(d[0]-a,d[1])) in b1):
					G.add_edge((z,d),(m,(d[0]-a,d[1])))
					#if ((m,(d[0],d[1]+a)) in b1):
					G.add_edge((z,d),(m,(d[0],d[1]+a)))
					#if ((m,(d[0],d[1]-a)) in b1):
					G.add_edge((z,d),(m,(d[0],d[1]-a)))

		b2 = G.edges()
	return G

def high_level_plan(G): 

	segment_1 = nx.shortest_path(G,source = (0,(0,0)),target = (1,(200,600)))
	segment_2 = nx.shortest_path(G,source = (1,(200,600)),target = (1,(400,200)))
	segment_3 = nx.shortest_path(G,source = (1,(400,400)),target = (1,(600,600)))
	return (segment_1 + segment_2 + segment_3)

def check_proposition(d):
	if ((200<=d[0]<=300) and (600<=d[1]<=700)):
		return '1'
	if ((400<=d[0]<=500) and (200<=d[1]<=300)):
		return '2'
	if ((600<=d[0]<=700) and (600<=d[1]<=700)):
		return '3'
	return 'N'

def random_sample(h): #h stands for high level state

	position = (random()*h[1][0],random()*h[1][1])
	return position


def dist(p1,p2):  #check distance between the two points

	return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def Nearest(G1,goalPost):
    
    a = G1.nodes()
    distance = dist(a[0],goalPost)
    temp = a[0]

    for i in a:
    	if (dist(i,goalPost)<distance):
    		distance = dist(i,goalPost)
    		temp = i
    return temp

def low_level_plan(H,G1,dfa):

	a = 100
	N = 2000
	reach_goal = False

	temp1 = 0
	temp2 = 0
	temp3 = 0

	seg_1 = []
	seg_2 = []
	seg_3 = []

	for i  in range(N):

		G1.add_node((0,0))
		goal = (650,650)
		rand_h = random.choice(H)
		v = Vertice(0,0,0)
		v.alpha = rand_h[0]
		v.ap = check_proposition(rand_h[1])
		v.position = (random.random()*a+rand_h[1][0],random.random()*a+rand_h[1][1])
		near_v = Nearest(G1,v.position)

		G1.add_node(v.position)
		G1.add_edge(near_v,v.position)

		if (temp1 == 0 and check_proposition(v.position)=='1'):
			temp1 = v
		if (temp2 == 0 and check_proposition(v.position)=='2'):
			temp2 = v
		if (temp3 == 0 and check_proposition(v.position)=='3'):
			temp3 = v

		if (temp1 != 0):
			seg_1 = nx.shortest_path(G1,source = (0,0),target = temp1.position)
		if ((temp1 != 0) and(temp2 != 0)):
			seg_2 = nx.shortest_path(G1,source = temp1.position,target = temp2.position)
		if ((temp1 != 0) and(temp2 != 0) and(temp3 != 0)):
			seg_3 = nx.shortest_path(G1,source = temp2.position,target = temp3.position)
		path = seg_1 + seg_2 + seg_3

		ap = []
		for i in path:
			ap.append(frozenset(check_proposition(i)))


		if (accept(dfa,0,{3},ap)):
			reach_goal = True
			G1.add_node(goal)
			G1.add_edge(temp3.position,goal)
			path1 = path + nx.shortest_path(G1,source = temp3.position,target = goal)
	
		if (reach_goal == True):
			print(ap)
			return path1
			break

def main():

	X = 800
	Y = 800

	p1 = '1'
	p2 = '2'
	p3 = '3'

	initPost = (0,0)   #initialize the robot position
	goalPost = (650,650) # end goal position

	dfa = {0:{frozenset(['N']):0,frozenset([1]):1,frozenset([p1,p2,p3]):3,frozenset([p1,p2]):2,frozenset([p1]):1,frozenset([p2]):0,frozenset([p3]):0},
       1:{frozenset(['N']):1,frozenset([1]):1,frozenset([p1]):1,frozenset([p2]):2,frozenset([p3]):1,frozenset([p2,p3]):3},
       2:{frozenset(['N']):2,frozenset([1]):2,frozenset([p1]):2,frozenset([p2]):2,frozenset([p3]):3},
       3:{frozenset(['N']):3, frozenset([1]):3,frozenset([p1]):3,frozenset([p2]):3,frozenset([p3]):3}}

	G = decomposition(X,Y,dfa)
	H = high_level_plan(G)

	xplot =[]
	yplot =[]
	b = G.edges()

	pre = H[0][1]
	for i in H:

		xplot.append(i[1])  #store the 1st point of line segment
		yplot.append(pre)
		pre = i[1] #store the 2nd point of line segment


	G1 = nx.Graph()

	L = low_level_plan(H,G1,dfa)


	#for i in range(80):
		#for j in range(80):
	for m in range(len(xplot)):
		xplot1, yplot1 = [xplot[m][0],yplot[m][0]], [xplot[m][1],yplot[m][1]]
		plt.plot(xplot1,yplot1) #marker = 'o'

	for n in range(len(L)-1):
		xplot2, yplot2 = [L[n][0],L[n+1][0]], [L[n][1],L[n+1][1]]  # x1,x2, y1,y2
		plt.plot(xplot2,yplot2, marker = 'o')


	ax = plt.gca()
	ax.set_xlim((0, X))
	ax.set_ylim((0, Y))

	ax.add_patch(
		patches.Rectangle(
			(200,600), 100, 100,
			hatch='/',
			facecolor = "#00ffff"
			)
		)
	ax.add_patch(
		patches.Rectangle(
			(400,200), 100, 100,
			hatch='\\'
			#fill = False
			)
		)
	ax.add_patch(
		patches.Rectangle(
			(600,600), 100, 100,
			hatch = '+',
			facecolor = "grey"
			)
		)

	plt.show()
	raw_input()

main()


