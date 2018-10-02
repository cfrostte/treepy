#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
from node_properties import NodeProperties
from edge_properties import EdgeProperties
from subgraph_properties import SubgraphProperties
import settings as config
import numpy as np
import math
import detection
import sys


# calculate distance
def calculateDistance(coords1, coords2):
    x_side = coords2[0] - coords1[0]
    y_side = coords2[1] - coords1[1]
    dist = math.floor(math.sqrt((x_side) ** 2 + (y_side) ** 2))
    return dist

class GraphProperties(object):

    def __init__(self):
        self.G = nx.Graph()

        self.node_props = NodeProperties()
        self.edge_props = EdgeProperties()
        self.subgraph_props = SubgraphProperties()

        self.subgraphs = {}
        # self.subgraphs_list = []
        self.subgraphs_ends = []
        self.subgraphs_edge_candidates = []
        self.subgraphs_angles_mean = {} # subgraph_id:{angles_mean, angles_std_dev}



    def getSubgraphEnds(self):
        return self.subgraphs_ends

    def findEndsOfSubgraphs(self):
        # remove old nodes from list
        self.subgraphs_ends = []

        for s in range(len(self.subgraphs)):
            ends_list = []
            for n in self.subgraphs[s].nodes:
                if(self.G.degree(n) <= 1):
                    ends_list.append(n)
            self.subgraphs_ends.append(ends_list)


    # calculates the distance between ends of different subgraphs to find
    # candidates to edges
    def findEdgeCandidates(self):
        # first, find the end of each subgraph
        self.findEndsOfSubgraphs()

        # then, try with all the combinations of those ends
        centroids_dict = self.node_props.getCoordCentroids()

        print('Edge candidates:', len(self.subgraphs_ends))
        for s1 in range(len(self.subgraphs_ends)):
            # print('s', s1)
            for n1 in range(len(self.subgraphs_ends[s1])):
                i = self.subgraphs_ends[s1][n1]
                for s2 in range(s1+1, len(self.subgraphs_ends)):
                    # print('**s',s2)
                    for n2 in range(len(self.subgraphs_ends[s2])):
                        j = self.subgraphs_ends[s2][n2]

                        dist = calculateDistance(centroids_dict[i], centroids_dict[j])
                        if(dist <= (config.getDistanceThreshold())):
                            angle = detection.calculateAngle(centroids_dict[i], centroids_dict[j])

                            # TODO: comparar con la media de ángulos de subgrafos
                            if(angle < 15):
                                self.subgraphs_edge_candidates.append((i, j))

    # Draw candidates to edges
    def drawEndsCandidates(self):
        pos = {}
        for candidate in self.subgraphs_edge_candidates:
            pos[candidate[0]] = self.getCoordCentroids(candidate[0])
            pos[candidate[1]] = self.getCoordCentroids(candidate[1])

        nx.draw_networkx_edges(self.G, pos=pos, with_labels=True, edgelist=self.subgraphs_edge_candidates, edge_color='b', width=1.5, font_size=9)

    # EDGES ====================================================================

    # returns distance for the given edge
    def getDistanceOfEdge(self, edge):
        distances = self.edge_props.distances

        if edge in distances:
            # look for the tuple (node1, node2)
            dist = self.edge_props.distances[edge]
        else:
            # reverse search (node2, node1)
            dist = self.edge_props.distances[tuple(reversed(edge))]
        return dist

        # edge_index = self.getIndexOfEdge(edge)
        # return self.edge_props.distances[edge]

    # returns angle for the given edge
    def getAngleOfEdge(self, edge):
        angles = self.edge_props.angles

        if edge in angles:
            # look for the tuple (node1, node2)
            ang = self.edge_props.angles[edge]
        else:
            # reverse search (node2, node1)
            edge_rev = tuple(reversed(edge))
            ang = self.edge_props.angles[edge_rev]
        return ang

    # returns the list of distances for the given list of edges
    def getDistancesOfEdges(self, edges_list):
        dist_list = {}
        for e in edges_list:
            dist_list[e] = self.getDistanceOfEdge(e)
        return dist_list

    # returns the list of angles for the given list of edges
    def getAnglesOfEdges(self, edges_list):
        angles_list = {}
        for e in edges_list:
            angles_list[e] = self.getAngleOfEdge(e)
        return angles_list

    # returns the index
    def getIndexOfEdge(self, edge):
        edges_list = list(self.G.edges)
        try:
            # try to find the tuple (node1, node2)
            index = edges_list.index(edge)
        except ValueError:
            # reverse search (node2, node1)
            index = edges_list.index(tuple(reversed(edge)))
        return index

    def addEdgesCandidates(self):
        '''
        Iterates over the list of edges candidates, adds the new edges to the graph, computes and stores it's properties
        '''
        # print('candidatos', len(self.subgraphs_edge_candidates))
        # adds the new edges and computes it's properties
        for e in self.subgraphs_edge_candidates:
            #print('agregado', '(',e[0], e[1],')')
            # adds the edge to the graph
            self.G.add_edge(e[0], e[1])
            self.computeEdgeProperties(e)

        self.subgraphs_edge_candidates = [] # clean the list of candidates

    def computeEdgeProperties(self, e):
        '''
        Computes and stores all the properties for the given edge

        :param edge: the edge to compute angle (tuple). E.g: (node1, node2)

        :return:
        '''
        # set the angle
        self.edge_props.angles[e] = self.calculateAngleOfEdge(e)
        # set the distance
        coords_n1 = self.getCoordCentroids(e[0])
        coords_n2 = self.getCoordCentroids(e[1])
        self.edge_props.distances[e] = detection.calculateDistance(coords_n1, coords_n2)

    def calculateAngleOfEdge(self, edge):
        '''
        Computes the angle for the given edge. Determines the coords of the two nodes and returns the angle defined by them.

        :param edge: the edge to compute angle (tuple). E.g: (node1, node2)

        :return: angle of the given edge (float)
        '''
        n1_coords = self.getCoordCentroids(edge[0])
        n2_coords = self.getCoordCentroids(edge[1])
        angle = detection.calculateAngle(n1_coords, n2_coords)
        return angle


    # NODES ====================================================================

    # returns the area for the given node
    def getAreaOfNode(self, node):
        return self.node_props.areas[node]

    # returns the list of areas for the given list of nodes
    def getAreasOfNodes(self, nodes_list):
        areas_list = {}

        for n in nodes_list:
            areas_list[n] = self.getAreaOfNode(n)
        return areas_list

    def getExcentricity(self, node):
        return self.node_props.excentricity[node]

    def getExcentriciys(self, nodes_list):
        excentriciy_list = {}

        for n in nodes_list:
            excentriciy_list[n] = self.getShaftRatio(n)
        return excentriciy_list

    def getErrorArea(self,node):
        return self.node_props.error_area[node]

    def getErrorAreas(self,node_list):
        error_areas = {}
        for n in node_list:
            error_areas[n] = self.getErrorArea(n)
        return error_areas

    def getCoordCentroids(self,node):
        return self.node_props.coordCentroids[node]


    # SUBGRAPH =================================================================
   
    def calculatePropsSubgraph(self,idx,s):

        try:
            subgraph_angles = self.getAnglesOfEdges(s.edges())
            mean_angle = float(sum(subgraph_angles.values())) / len(subgraph_angles)
            std_angles = np.std(list(subgraph_angles.values()))
        except ZeroDivisionError:
            mean_angle = None
            std_angles = None
        self.subgraph_props.mean_angle[idx] = mean_angle
        self.subgraph_props.std_angle[idx] = std_angles

        try:
            subgraph_distances = self.getDistancesOfEdges(s.edges())
            mean_distances = float(sum(subgraph_distances.values())) / len(subgraph_distances)
            std_distances = np.std(list(subgraph_distances.values()))
        except ZeroDivisionError:
            mean_distances = None
            std_distances = None
        self.subgraph_props.mean_dist[idx] = mean_distances
        self.subgraph_props.std_dist[idx] = std_distances

        try:
            subgraph_area = self.getAreasOfNodes(s.nodes())
            mean_area = float(sum(subgraph_area.values())) / len(subgraph_area)
            std_area = np.std(list(subgraph_area.values()))
        except ZeroDivisionError:
            mean_area = None
            std_area = None

        self.subgraph_props.mean_area[idx] = mean_area
        self.subgraph_props.std_area[idx] = std_area

    #--------------------------------------------------------------------------------
    # find non-connected subgraphs in main graph
    # @profile
    def findSubgraphs(self):

        self.subgraphs = {}
        self.subgraph_props.setProps()
       
        listSubgraph = sorted(nx.connected_components(self.G), key = len, reverse=True)

        for i in range(len(listSubgraph)):
            s = self.G.subgraph(listSubgraph[i])
            self.generateAnglesTwoEdges(s,i)
            self.subgraphs[i] = s
            self.calculatePropsSubgraph(i,s)
            self.polynomialRegression(s,i,2)

    #--------------------------------------------------------------------------------
    def generateAnglesTwoEdges(self,H,i):
        for n in H.nodes():
            if H.degree(n) > 1:
                edges = list(H.edges(n))
                angles = self.getAnglesOfEdges(edges)
                for a in angles:
                    for b in angles:
                        if a != b:
                            r = angles[a] - angles[b]
                            self.edge_props.angle_two_edge[i,a,b] = r

        mean_angle_two = np.mean(np.abs(list(self.edge_props.angle_two_edge.values())))
        std_angle_two = np.std(np.abs(list(self.edge_props.angle_two_edge.values())))
        self.subgraph_props.mean_angle_two[i] = mean_angle_two
        self.subgraph_props.std_angle_two[i] = std_angle_two

    #--------------------------------------------------------------------------------
    def polynomialRegression(self,H,idx,degree):
        '''
            POLYNOMIAL REGRESSION
            this function generates a curve adjustment to the subgraphs
        '''
        x = []
        y = []
        curve = {}
        if (H.number_of_nodes() > 3):
            for n in H.nodes():
                x.append(self.node_props.centroids[n][0][0]) #Cargo coord x del centroide
                y.append(self.node_props.centroids[n][0][1]) #Cargo coord y del centroide
            z = np.polyfit(x,y, degree) # genera parametros de la curva
            p = np.poly1d(z) # función curva
            e = np.abs(np.polyval(z, x) - y)
            error = np.sum(e)/len(x)
            self.subgraph_props.coef_curve[idx] = p
            self.subgraph_props.error_curve[idx] = round(error,1)
        else:
            self.subgraph_props.error_curve[idx] = round(0,1)

    #---------------------------------------------------------------------------------
    def getCantNodesSub(self,id_subgraph):
        sub = self.subgraphs[id_subgraph]
        can = sub.number_of_nodes()
        return can

    # returns the mean area
    def getMeanArea(self,id_subgraph):
        return self.subgraph_props.mean_area[id_subgraph]
    # returns the std area
    def getStdArea(self, id_subgraph):
        return self.subgraph_props.std_area[id_subgraph]

    # returns the mean distances
    def getMeanDistance(self, id_subgraph):
        return self.subgraph_props.mean_dist[id_subgraph]
    # returns the std distances
    def getStdDistance(self, id_subgraph):
        return self.subgraph_props.std_dist[id_subgraph]

    # returns the mean angles
    def getMeanAngle(self, id_subgraph):
        return self.subgraph_props.mean_angle[id_subgraph]
    # returns the std angles
    def getStdAngle(self, id_subgraph):
        return self.subgraph_props.std_angle[id_subgraph]

    def getMeanTwoAngles(self,id_subgraph):
        return self.subgraph_props.mean_angle_two[id_subgraph]

    def getStdTwoAngles(self,id_subgraph):
        return self.subgraph_props.std_angle_two[id_subgraph]

    # returns the quality of subgraph
    def getQualitySubgraph(self,id_subgraph):
        return self.subgraph_props.quality[id_subgraph]

    def getEdgesUnion(self):
        return self.subgraphs_edge_candidates
