#!/usr/bin/env python2.7
# oogenerateParticles.py
# Thomas Boser

"""
Note to self: particle printing format
particle barcode, [ vertex x,y,z], [ momentum p, theta, phi ], charge
4509578221846528, [-0.0224014, -0.00570905, -51.0684], [1450.18, 2.06558, -2.19591], 1
"""

from __future__ import print_function, division

import random
import math
import oogenerateHits as gh
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Particle:
    """ particle constructor """
    def __init__(self, barcode, hitbcs, gen = False, vertices=[]):
        self.barcode = barcode
        self.vertices = vertices
        self.mangle = []
        self.charge = None

        self.hits = []
        self.hitbcs = hitbcs

        ### FOR GENERATED PARTICLES ###
        self.p_radius = 0
        self.centpt = []
        self.p_circ = None
        self.m_ray = None

        if(gen): self.genParticle()

    def genParticle(self):
        """ generate values for particle """
        self.vertices = [round(random.uniform(.03, -.03),7), round(random.uniform(.03, -.03),7)\
                         ,0] #Leaving z at 0, only considering 2d space for now
        self.mangle = [round(random.uniform(15000, 4000),2), round(random.uniform(4, 0),5),\
                       round(random.uniform(4, -4),5)]
        self.charge = random.randint(-1, 1)

        #particle trajectory estimations
        magfield = 1 # we will assume the magnetic field is uniform
        if self.charge != 0: 
            self.p_radius = self.mangle[0] / (self.charge * magfield)
            self.centpt = [self.vertices[0] + (self.p_radius*math.sin(self.mangle[2])),
                           self.vertices[1] + (self.p_radius*math.cos(self.mangle[2]))]

    def addHit(self, hit):
        """ add a hit to self.hits """
        if hit not in self.hits: self.hits.append(hit)

    def getHits(self, detectors, override = False):
        """ produces all hits with the detectors specified, appends them
            to self.hits, assumes particles travel in circular motion so
            this is an approximation """
        if len(self.hits) == 0 or override == True: #if hits are not yet computed
            for detpos, det in enumerate(detectors):
                poss_hits = self.getIntersects(det)
                if poss_hits is not None:
                    self.hits.append(gh.Hit(self.hitbcs[detpos], 
                                     self.barcode, poss_hits, detpos+1))

    def getIntersects(self, detector):
        """ returns intersection pts of two cirles (or a line and a circle).
            does so using custom methods. """
        m_intersect = [detector.radius*math.cos(self.mangle[0])+self.vertices[0],
                       detector.radius*math.sin(self.mangle[0])+self.vertices[1]]
        if self.charge == 0: #if charge is 0 particle travels in straight line
            return m_intersect
        else: #circle circle intersection if particle is charged
            intersects = self.circ_intersect(detector.center, self.centpt, 
                                             detector.radius, self.p_radius)
            if not intersects: return None
            flag = 0
            if self.pt_dist(intersects[1], m_intersect) < self.pt_dist(intersects[0], m_intersect):
                flag = 1
            return intersects[flag]


    def plotOrigin(self):
        """ plot the origin point for the particle """
        plt.scatter(self.vertices[0], self.vertices[1], c='r')


    def plotJoins(self):
        """ plot all hits joined by a line """
        col = random.choice('bgrcmyk') #chose random color
        #self.hits.sort(key=lambda x: x.detpos)
        origin = self.vertices
        for hit in self.hits:
            plt.plot((origin[0], hit.lhit[0]),
                     (origin[1], hit.lhit[1]),
                      color = col)
            origin = hit.lhit

    def plotHits(self):
        """ plot all hits in self.hits """
        for hit in self.hits:
            hit.plotHit()

    def printParticle(self):
        """ print particle to stdout """
        print(self.barcode,',',self.vertices,',',self.mangle,',',self.charge, sep='')

    def printHits(self):
        """ print hits to stdout """
        for hit in self.hits:
            hit.printHit()

    ### HELPER METHODS ###
    def pt_dist(self, p1, p2): #TODO add to helper methods
        """ return distance between two points """
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def circ_intersect(self, v0, v1, r0, r1):
        """ return intersection points of two circles """
        dist = self.pt_dist(v0, v1) #calculate distance between 
        if dist > (r0 + r1): return False #out of range
        if dist < abs(r0 - r1): return False #circle contained
        if dist == 0: return False #same origin

        a = (r0**2 - r1**2 + dist**2) / (2*dist)
        b = dist - a
        h = math.sqrt(r0**2 - a**2)

        v2x = v0[0] + a*(v1[0] - v0[0])/dist
        v2y = v0[1] + a*(v1[1] - v0[1])/dist
        
        x3p = v2x + h*(v1[1] - v0[1])/dist
        y3p = v2y - h*(v1[0] - v0[0])/dist
        x3n = v2x - h*(v1[1] - v0[1])/dist
        y3n = v2y + h*(v1[0] - v0[0])/dist

        return [[x3p, y3p], [x3n, y3n]]


