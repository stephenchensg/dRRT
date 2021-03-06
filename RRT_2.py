import math, sys, random
from math import *
#import pygame
#from pygame import *
import matplotlib.pyplot as plt
import numpy as np
import time

class Node(object):
    def __init__(self, point, parent):
        super(Node, self).__init__()
        self.point = point
        self.parent = parent

X = 800
Y = 800
N = 10

robot_radius = 2
vicinity = 5

min_dist = 2.0
Maxnode = 5000

count = 0
cirObs = []

def dist(p1,p2):  #check distance between the two points

    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def extend(p1,p2):  #extend the tree to q_new

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

    for x, y in zip(x1,x2):

            if (collides((x,y))==True):
                check = True
            else: 
                return p1
                break
        
    if (check == True):
        return (a1, a2)

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

def ce_collision_check(p1,p2,r_radius,ob_radius): #collision check

    distance = dist(p1,p2)
    if (distance >= (r_radius + ob_radius)):
        return True
    return False

def generate_random_point(): # generate random points
    while True:
        p = random.random()*X,random.random()*Y
        p_no_collision_env = collides(p)
        if (p_no_collision_env == True):
            return p

def collides(p): # check collision with environment

    collision_free = False
    for cir in range(len(cirObs)):
        if (ce_collision_check(p,(cirObs[cir][0],cirObs[cir][1]),robot_radius,cirObs[cir][2])==True):
            collision_free = True
        else: 
            return False
    return collision_free

    #if (ce_collision_check(p,(cirObs[0][0],cirObs[0][1]),robot_radius,cirObs[0][2])==True):
        #if (ce_collision_check(p,(cirObs[1][0],cirObs[1][1]),robot_radius,cirObs[1][2])==True):
           # if (ce_collision_check(p,(cirObs[2][0],cirObs[2][1]),robot_radius,cirObs[2][2])==True):
               # return True
    #return False


def initializing_obstacles(configuration): #initializing the circular obstacles

     global cirObs
     cirObs = []
     if (configuration == 0):
        cirObs.append((X/4,Y/4,120))
        cirObs.append((X/2,Y/2,200))
        cirObs.append((X/1.5,Y/1.5,60))


def main():

    start_time = time.time()

    global count
    count = 0
    initPost = Node((1,1), None)   #initialize the robot position
    goalPost = Node((700,700), None) # end goal position
    temp = Node(None,None)
    counter = 0

    reach_goal = False
    initializing_obstacles(0)
    node = []
    node.append(initPost)

    q_near = node[0].point
    q_closest_goal = node[0].point

    #print(q_near)  #check the points

    while count < Maxnode: 

        #import ipdb; ipdb.set_trace()
        if (reach_goal == False):
            for n in range(1,len(node)-1):
                if (dist(node[n].point,goalPost.point)<dist(q_closest_goal,goalPost.point)):
                    q_closest_goal = node[n].point
            
            #print(q_closest_goal)    
            if (local_connector(q_closest_goal, goalPost.point) == True):
                reach_goal = True
                break
        if (reach_goal == True):
            break

        else: 
            rand = generate_random_point()
            #print(rand)
            plt.plot(rand[0],rand[1],"green")

            #Find the qnear
            for n in range(1,len(node)-1):
                if (dist(node[n].point,rand)<dist(q_near,rand)):
                    q_near = node[n].point
                    counter = n

            temp.point = extend(q_near,rand)
            temp.parent = node[counter].parent
            node.append(temp)
            temp = Node(None,None)
            count = count + 1

    print(reach_goal) 
    print("--- %s seconds ---" % (time.time() - start_time)) #check if reach goal
    
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



