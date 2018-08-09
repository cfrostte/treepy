#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class SubgraphProperties(object):

    def __init__(self):
        # mena and std for area
        self.mean_area = {}
        self.std_area = {}
        # mena and std for distance
        self.mean_dist = {}
        self.std_dist = {}
        # mena and std for angle
        self.mean_angle = {}
        self.std_angle = {}
        # mena and std for angle
        self.mean_angle_two = {}
        self.std_angle_two = {}
        # quality of subgraph
        self.quality = {}
        # List of curve aprox
        self.coef_curve = {}
        self.error_curve = {}


    def setProps(self):
        self.mean_area = {}
        self.std_area = {}
        self.mean_dist = {}
        self.std_dist = {}
        self.mean_angle = {}
        self.std_angle = {}
        self.mean_angle_two = {}
        self.std_angle_two = {}
        self.quality = {}
        self.coef_curve = {}
        self.error_curve = {}


    def getMeanAngleTwo(self):
        return self.mean_angle_two

    def getStdAngleTwo(self):
        return self.std_angle_two

    def getMeanAngle(self):
        return self.mean_angle

    def getCurves(self):
        return self.coef_curve
    def getQualityCurve(self):
        return self.error_curve

