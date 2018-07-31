#!/usr/bin/env python

import numpy as np

class EdgeProperties(object):

    def __init__(self):
        # self.edges = []
        self.distances = {}
        self.angles = {}
        self.label = {}
        self.angle_two_edge = {}

    # diferencia de color entre nodos

    # def setEdges(self, edges_list):
    #     self.edges = edges_list
    #
    # def getEdges(self):
    #     return self.edges

    # Distance --------------------------------------------
    def setDistances(self, distances_list):
        self.distances = {}
        self.distances = distances_list

    def getDistances(self):
        return self.distances
    # Angles ----------------------------------------------
    def setAngles(self, angles_list):
        self.angles = {}
        self.angles = angles_list

    def getAngles(self):
        return self.angles
    # Label ----------------------------------------------
    def setLabel(self, label_value):
        self.label = {}
        self.distances = label_value

    def getLabel(self):
        return self.label

    # Angle two edges -------------------------------------
    def setAngleTwoEdge(self,angle_two_list):
        self.angle_two_edge = {}
        self.angle_two_edge = angle_two_list

    def getAngleTwoEdge(self):
        return self.angle_two_edge

    # Remove propiertis -----------------------------------
    def removeProp(self,edge):

        if edge in self.distances and edge in self.angles:
            self.distances.pop(edge)
            self.angles.pop(edge)
        else:
            self.distances.pop(tuple(reversed(edge)))
            self.angles.pop(tuple(reversed(edge)))
