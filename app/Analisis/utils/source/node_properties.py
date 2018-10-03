#!/usr/bin/env python
# -*- coding: utf-8 -*-

class NodeProperties(object):

    def __init__(self):
        # list of areas (in pixels)
        self.areas = {}
        # list of centroids coords
        self.centroids = {}
        # list of centroids coords
        self.coordCentroids = {}
        # list of bounding boxes of each region
        self.bboxes = {}
        # list of axis region
        self.excentricity = {}
        # error relative: area region vs area bbox
        self.error_area = {}
        # quality of node
        self.quality = {}
        # ----------------------------------------------
        # Node faltantes
        self.coord_missing = []

        # color
        # perimetro

    def getCoordMissing(self):
        return self.coord_missing

    def setCoordMissing(self,list_c):
        self.coord_missing = []
        self.coord_missing = list_c

    # sets and get area --------------------------------------------------------
    def setAreas(self, areas_arr):
        self.areas = {}
        self.areas = areas_arr

    # lists all the areas
    def getAreas(self):
        return self.areas

    # returns the area for the given Node ID
    def getArea(self, node_id):
        return self.areas[node_id]

    # sets and get centroid ----------------------------------------------------
    def setCentroids(self, centroids_arr):
        self.centroids = {}
        self.centroids = centroids_arr

    # lists all the centroids
    def getCentroids(self):
        return self.centroids

    # sets and get coord centroid ----------------------------------------------
    def setCoordCentroids(self, centroids_dict):
        self.coordCentroids = {}
        self.coordCentroids = centroids_dict

    # lists all the centroids
    def getCoordCentroids(self):
        return self.coordCentroids

    # # returns the centroid for the given Node ID
    # def getCentroid(self, node_id):
    #     return self.centroids[node_id]

    # get and set bboxes -------------------------------------------------------
    def setBBoxes(self, bboxes_arr):
        self.bboxes = {}
        self.bboxes = bboxes_arr

    # gets the list of bboxes
    def getBBoxes(self):
        return self.bboxes

    # get and set excentriciy --------------------------------------------------
    def setExcentriciy(self,excentriciy_list):
        self.excentricity = {}
        self.excentricity = excentriciy_list

    def getExcentricity(self):
        return self.excentricity

    # get and set error of areas -----------------------------------------------
    def setErrorArea(self,error_list):
        self.error_area = {}
        self.error_area = error_list

    def getErrorArea(self):
        return self.error_area

    # get and set quality of node ----------------------------------------------
    def setQuality(self,quality_list):
        self.quality = {}
        self.quality = quality_list

    def getQuality(self):
        return self.quality


    # Remove propiertis---------------------------------------------------------
    def removeProp(self,node):
        self.areas.pop(node)
        self.bboxes.pop(node)
        self.centroids.pop(node)
        self.coordCentroids.pop(node)
        self.excentricity.pop(node)
        self.error_area.pop(node)
        # self.quality.pop(node)
