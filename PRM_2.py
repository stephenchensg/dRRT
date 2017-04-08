import networkx as nx
import math, sys, random
from math import *
import matplotlib.pyplot as plt
import numpy as np
import time

X = 800
Y = 800
N = 10

robot_radius = 2
vicinity = 5
radius = 20

min_dist = 2.0
Maxnode = 1000

count = 0
cirObs = []

def dist(p1,p2):  #check distance between the two points

    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def generate_random_point(): # generate random points
    while True:
        p = random.random()*X,random.random()*Y
        p_no_collision_env = collides(p)
        if (p_no_collision_env == True):
            return p

def ce_collision_check(p1,p2,r_radius,ob_radius): #collision check

    distance = dist(p1,p2)
    if (distance >= (r_radius + ob_radius)):
        return True
    return False

def collides(p): # check collision with environment

    collision_free = False
    for cir in range(len(cirObs)):
        if (ce_collision_check(p,(cirObs[cir][0],cirObs[cir][1]),robot_radius,cirObs[cir][2])==True):
            collision_free = True
        else: 
            return False
    return collision_free

def edge_check(p1,p2):  #attempt to connect to the end_goal
    
    check1 = False

    b1 = np.linspace(p1[0], p2[0], 100)
    b2 = np.linspace(p1[1], p2[1], 100)

    for xb, yb in zip(b1,b2):

        if (collides((xb,yb))==True):
            check1 = True
        else: 
            return False  
            break

    return check1 

def Near(G,rand,radius):
    
    a = G.nodes()
    u = []
    for i in range(len(a)):
        if (dist(a[i],rand)<radius):
            u.append(a[i])
    return u

def initializing_obstacles(configuration): #initializing the circular obstacles
    
     global cirObs
     cirObs = []
     if (configuration == 0):
        cirObs.append((X/4,Y/4,120))
        cirObs.append((X/2,Y/2,200))
        cirObs.append((X/1.5,Y/1.5,60))

def main():

    start_time = time.time()
    #start_time = time.time()
    initPost = (1,1)   #initialize the robot position
    goalPost = (700,700) # end goal position
    count = 0
    initializing_obstacles(0)
    
    G = nx.Graph()
    G.add_node(initPost)
    #G.add_node(goalPost)

    for i in range(Maxnode):
        rand = generate_random_point()
        G.add_node(rand)

    a1 = G.nodes()

    for ux in range(len(a1)):
        U_collection = Near(G,a1[ux],radius)
        U_collection.remove(a1[ux])

        for j in range(len(U_collection)):
            if (edge_check(a1[ux],U_collection[j])==True):
                G.add_edge(a1[ux],U_collection[j])
                G.add_edge(U_collection[j],a1[ux])

    print("--- %s seconds ---" % (time.time() - start_time)) #check if reach goal

    #plot the graph
    circle1 = plt.Circle((cirObs[0][0], cirObs[0][1]), cirObs[0][2], color='r')
    circle2 = plt.Circle((cirObs[1][0], cirObs[1][1]), cirObs[1][2], color='blue')
    circle3 = plt.Circle((cirObs[2][0], cirObs[2][1]), cirObs[2][2], color='g', clip_on=False)

    for j in range(len(a1)):
        plt.plot(a1[j][0],a1[j][1],"ro")


    plt.plot(initPost[0],initPost[1], "bo")
    plt.plot(goalPost[0],goalPost[1], "bo")


    ax = plt.gca()
    ax.set_xlim((0, X))
    ax.set_ylim((0, Y))

    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.add_artist(circle3)

# here must be something like circle.plot() or not?

    plt.show()

    #checkf for the shortest path
    shortest = nx.shortest_path(G,source = initPost,target = goalPost)
    print(shortest)

    raw_input()

if __name__ == '__main__':
    main()
 

