import networkx as nx
import math, sys, random
from math import *
#import pygame
#from pygame import *
import matplotlib.pyplot as plt
import numpy as np
import time

X = 800
Y = 800
N = 10

robot_radius = 2
vicinity = 5
radius = 50

min_dist = 2.0
Maxnode = 200

N1 = 100

count = 0
cirObs = []

class Node(object):
    def __init__(self, point, distance):
        super(Node, self).__init__()
        self.point = point
        self.distance = distance

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

def local_connector(p1,p2):  #attempt to connect to the end_goal
    
    check1 = False

    if (dist(p1,p2)<min_dist):
        return True

    else: 
        b1 = np.linspace(p1[0], p2[0], 100)
        b2 = np.linspace(p1[1], p2[1], 100)

        for xb, yb in zip(b1,b2):

            if (collides((xb,yb))==True):
                check1 = True
            else: 
                return False  
                break

        if (check1 == True):
            for xb, yb in zip(b1,b2):
                plt.plot(xb, yb,"ro")

        return check1    

def Near(G,rand,radius):
    
    a = G.nodes()
    u = []
    for i in range(len(a)):
        if (dist(a[i],rand)<radius):
            u.append(a[i])
    return u

def Nearest(G1,goalPost,k):
    
    a = G1.nodes()
    u = []
    v = []

    for i in range(len(a)):
        if (dist(a[i],goalPost)<50):
            u.append(Node(a[i],dist(a[i],goalPost)))
            #print(a[i])

    sorted(u,key =lambda u: u.distance)

    for j in range(k):
        if (len(u)<=j): 
            break
        else:
            v.append(u[j].point)

    #print(v)
    return v

def initializing_obstacles(configuration): #initializing the circular obstacles
    
     global cirObs
     cirObs = []
     if (configuration == 0):
        cirObs.append((X/4,Y/4,120))
        cirObs.append((X/2,Y/2,200))
        cirObs.append((X/1.5,Y/1.5,60))

def oracle(G,q_closest_goal,rand): #qnear is a list of near configuration with the random point

    a = G.nodes()
    min_angle = math.fabs(atan2(q_closest_goal[1]-rand[1],q_closest_goal[0]-rand[0]))
    q_new = a[0]

    for i in range(len(a)):
        angle = math.fabs(atan2(a[i][1]-rand[1],a[i][0]-rand[0]))
        if (angle<min_angle):
            q_new = a[i]
            min_angle = angle
    
    return q_new

def main():

    start_time = time.time()
    #start_time = time.time()
    initPost = (1,1)   #initialize the robot position
    goalPost = (700,700) # end goal position
    count = 0
    initializing_obstacles(0)
    reach_goal = False

    G = nx.Graph()
    G.add_node(initPost)
    G.add_node(goalPost)

    for l in range(Maxnode):
        rand1 = generate_random_point()
        G.add_node(rand1)
   
    a1 = G.nodes()


    for ux in range(len(a1)):
        U_collection = Near(G,a1[ux],radius)
        U_collection.remove(a1[ux])

        for j in range(len(U_collection)):
            if (edge_check(a1[ux],U_collection[j])==True):
                G.add_edge(a1[ux],U_collection[j])
                G.add_edge(U_collection[j],a1[ux])
  ## above is to create the graph by PRM

    G1 = nx.Graph()
    G1.add_node(initPost)
    #G1.add_node(goalPost)

    b1 = G1.nodes()
    q_closest_goal = b1[0]

    xplot =[]
    yplot =[]
    count1 = 0

    while reach_goal == False:

        for i in range(N1):
            if (i==0 or i ==1): 
                k =  3
            else: 
                k = int(math.log(i))

            rand = generate_random_point()
            b1 = G1.nodes()

            for n in range(len(b1)):
                if (dist(b1[n],goalPost)<dist(q_closest_goal,goalPost)):
                    q_closest_goal = b1[n]

            q_new = oracle(G,q_closest_goal,rand) 

            if(edge_check(q_closest_goal, q_new)==True):
                G1.add_node(q_new)
                G1.add_edge(q_closest_goal,q_new)
                G1.add_edge(q_new,q_closest_goal)
                xplot.append(q_closest_goal)
                yplot.append(q_new)
            
            #count1 = count1 +1 
            #if (count1 >1000):
                #reach_goal = True

            q_nearset = Nearest(G1,goalPost,k)
   
            for m in range(len(q_nearset)):
               if(local_connector(q_nearset[m],goalPost)==True):
                   reach_goal = True
                   break
            if (reach_goal == True):
                break

        print(reach_goal)
        
    #print(G1.edges())
    #nx.draw(G1,pos=nx.spring_layout(G1))
    #plt.show()    
    
    print("--- %s seconds ---" % (time.time() - start_time))
    #plot the graph
    circle1 = plt.Circle((cirObs[0][0], cirObs[0][1]), cirObs[0][2], color='r')
    circle2 = plt.Circle((cirObs[1][0], cirObs[1][1]), cirObs[1][2], color='blue')
    circle3 = plt.Circle((cirObs[2][0], cirObs[2][1]), cirObs[2][2], color='g', clip_on=False)

    plt.plot(initPost[0],initPost[1], "bo")
    plt.plot(goalPost[0],goalPost[1], "bo")


    for m in range(len(xplot)):
        xplot1, yplot1 = [xplot[m][0],yplot[m][0]], [xplot[m][1],yplot[m][1]]
        plt.plot(xplot1,yplot1, marker = 'o')

    ax = plt.gca()
    ax.set_xlim((0, X))
    ax.set_ylim((0, Y))

    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.add_artist(circle3)

    shortest = nx.shortest_path(G1,source = initPost,target = goalPost)
    for k in range(len(shortest)):
        plt.plot(shortest[k][0],shortest[k][1], "bo")

    print(shortest)
    # here must be something like circle.plot() or not?

    plt.show()
    raw_input()

if __name__ == '__main__':
    main()
 




