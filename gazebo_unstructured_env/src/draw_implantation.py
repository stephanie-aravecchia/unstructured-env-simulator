#!/usr/bin/env python3
from pointpats import PoissonClusterPointProcess
from pointpats.window import as_window
from libpysal.cg import Polygon
import matplotlib.pyplot as plt
import cv2
import random
from math import pi

#draw an implantation and scale to create later a scene in blender
class SimuWorld:
    def __init__(self, x, y):
        self.size_x = x
        self.size_y = y
        self.fig = plt.figure()
        self.fig.set_figheight(11)
        self.fig.set_figwidth(11)
        self.ax = self.fig.add_axes((.1,.1,.8,.8))
        self.elements = []

    def get_spatial_distribution(self, n_trees):
        x = float(self.size_x)/2
        y = float(self.size_y)/2
        p = Polygon(((-x,-y),(-x,y),(x,y),(x,-y)), None)
        w = as_window(p)
        n_parents = int(n_trees/20) + 1
        samples = PoissonClusterPointProcess(w, n_trees, n_parents , 3*x/(n_parents), 1)
        self.ax.plot(samples.realizations[0][:,0],samples.realizations[0][:,1],"+")
        return samples.realizations[0]  
    
    def add_element_to_world(self, elem, num, x, y, z, roll, pitch, yaw, vscale, hscale):
        if elem == "bush":
            hscale = 1.5*hscale
            vscale = 1.5*vscale
        if elem == "cyl_thin":
            hscale = .1*hscale
            vscale = 1
        if elem == "rect_thin":
            hscale = .1*hscale
            vscale = 1

        self.elements.append((elem, num, x, y, z, roll, pitch, yaw, vscale, hscale))
    
    def save_distribution(self,xp):
        f = open("distribution_%s.csv"%xp,"w")
        f.write("elem,num,x,y,z,roll,pitch,yaw,vscale,hscale\n")
        for l in self.elements:
            f.write(",".join(str(e) for e in l) +"\n")    
        f.close()
        self.elements = []

    def calc_values(self,p):
        x = p[0]
        y = p[1]
        z =  0
        roll, pitch = 0, 0
        yaw = (2*pi/100)*random.randint(0,100) 
        vscale = 0.01*random.randint(70,130)
        hscale = 0.01*random.randint(70,130)
        return x,y,z,roll,pitch,yaw,hscale,vscale

    def populate_world(self,n_trees, elem):
        points = self.get_spatial_distribution(n_trees) 
        for i, p in enumerate(points):
            x,y,z,roll,pitch,yaw,hscale,vscale = self.calc_values(p)
            self.add_element_to_world(elem, i, x, y, z, roll, pitch, yaw, vscale, hscale)

    def populate_world_with_known_distribution(self,n_trees, elem, points):
        for i, p in enumerate(points):
            x,y,z,roll,pitch,yaw,hscale,vscale = self.calc_values(p)
            self.add_element_to_world(elem, i, x, y, z, roll, pitch, yaw, vscale, hscale)
    
    #implant assets in the world with a provided point process
    def create_world_with_known_distribution(self, n_trees, xp, n_models, points):
        if xp == "cyl":
            elem = xp
            self.populate_world_with_known_distribution(n_trees, elem, points)
        elif xp == "cyl_thin":
            elem = xp
            self.populate_world_with_known_distribution(n_trees, elem, points)
        elif xp == "rect":
            elem = xp
            self.populate_world_with_known_distribution(n_trees, elem, points)
        elif xp == "rect_thin":
            elem = xp
            self.populate_world_with_known_distribution(n_trees, elem, points)
        elif xp == "trees":
            p = len(points)/n_models
            for i in range(n_models):
                elem = "tree_%02d"%i
                rmin = int(i*p)
                rmax = int(min((1+i)*p,len(points)))
                print(len(points), rmin, rmax)
                self.populate_world_with_known_distribution(int(n_trees/float(n_models)), elem, points[rmin:rmax])
        elif xp == "various":
            print(len(points))
            p = len(points)/(n_models+4)
            elem = "rect"
            n_prev = 0
            n = int(n_trees/10.)
            self.populate_world_with_known_distribution(n-n_prev, elem, points[n_prev:n])
            elem = "cyl_thin"
            n_prev = n
            n = n + int(n_trees/5.)
            self.populate_world_with_known_distribution(n-n_prev, elem, points[n_prev:n])
            n_prev = n
            n = n + int(n_trees/5.)
            elem = "rect_thin"
            self.populate_world_with_known_distribution(n-n_prev, elem, points[n_prev:n])
            n_prev = n
            n = n + int(n_trees/10.)
            elem = "rect"
            self.populate_world_with_known_distribution(n-n_prev, elem, points[n_prev:n])
            n_prev = n
            elem = "trees"
            p = (len(points)-n_prev)/n_models
            for i in range(n_models):
                elem = "tree_%02d"%i
                rmin = int(i*p+n_prev)
                rmax = int(min((1+i)*p+n_prev,len(points)))
                print(rmin, rmax)
                self.populate_world_with_known_distribution(p, elem, points[rmin:rmax])
        else:
            print("Make a choice")
            exit(0)
    
    
    #implant assets in the world without a provided point process, for each asset, a point process will be drawn (with n_trees each)
    def create_world(self, n_trees, xp, n_models):
        if xp == "cyl":
            elem = xp
            self.populate_world(n_trees, elem)
        elif xp == "cyl_thin":
            elem = xp
            self.populate_world(n_trees, elem)
        elif xp == "rect":
            elem = xp
            self.populate_world(n_trees, elem)
        elif xp == "rect_thin":
            elem = xp
            self.populate_world(n_trees, elem)
        elif xp == "trees":
            elem = xp
            self.populate_world(n_trees, elem)
        elif xp == "various":
            elem = "rect"
            self.populate_world(int(n_trees/10.), elem)
            elem = "cyl_thin"
            self.populate_world(int(n_trees/5.), elem)
            elem = "rect_thin"
            self.populate_world(int(n_trees/5.), elem)
            elem = "rect"
            self.populate_world(int(n_trees/10.), elem)
            elem = "trees"
            self.populate_world(int(2*n_trees/5.), elem)
        else:
            for i in range(n_models):
                elem = "tree_%02d"%i
                self.populate_world(int(n_trees/float(n_models)), elem)

        plt.show()
        

if __name__ == "__main__":

    #This code is implemented for the following xps: rect, cyl, trees, rect_thin, cyl_thin, various
    list_xp = ["rect", "trees"]
    size = 60
    n_elements=50
    n_trees_in_library=15 
    #size of the world (x,y) 
    world = SimuWorld(size, size)
    points = world.get_spatial_distribution(n_elements)
    for xp in list_xp:
        world.create_world_with_known_distribution(n_elements, xp, n_trees_in_library, points)
        world.save_distribution("new_env_"+xp)