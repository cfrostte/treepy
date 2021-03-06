#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.patches as mpatches
# from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb
from PIL import Image, ImageOps, ImageDraw
from numpy import array
import numpy as np
import os
import math
import Analisis.utils.source.settings as config
from Analisis.utils.source.graph_properties import GraphProperties
from shapely.geometry import LineString, Polygon, Point
from Analisis.utils.source.segmentation import Segmentation
import randomcolor
import copy


# #-------------------------------------------------------------------------------
def copyTheClass(object):
    '''
        This function, makes the copy of a class and its sub class
        Parametrs:

        object: type <__main__.MyClass object>
    '''
    object_new = GraphProperties() #create new object type GraphProperties()

    object_new.G = copy(object.G)



# #-------------------------------------------------------------------------------
def cutRemains(img_RGB):
    plt.imshow(img_RGB)
    coords = plt.ginput(-1)
    poly = Polygon(coords)
    return poly

# set threshold grayscale
# @profile
def automaticSegmentation(self):
    segm = Segmentation()

    # use_global_otsu = True
    methods = ['manual', 'auto_grayscale', 'global_otsu', 'local_otsu']
    algo = config.algorithm
    img = []

    start_time = datetime.datetime.now()

    # VARI descriptor
    if config.compute_VARI:
        print('* VARI Descriptor')
        # self.img_VARI = segm.computeVARI(self)
        if config.multiprocess_VARI:
            print('* Multiprocessing')
            self.img_VARI = segm.computeMultiprocessVARI(self)
        else:
            self.img_VARI = segm.computeVARI(self)

        start_time = printElapsedTime(start_time, 'Descriptor multiproc.')
        img = self.img_VARI
    else:
        print('* Grayscale image')
        import numpy
        img = numpy.array(self.img_Grayscale.convert("L"))
    start_time = printElapsedTime(start_time, 'Automat. segm.')

    # segmentation algorithms
    if algo == 2:
        print('* Global Otsu')
        img_binary = segm.globalOtsu(self, img)
        # print('con Otsu', np.min(img_binary), np.max(img_binary))
    elif algo == 3:
        print('* Local Otsu')
        img_binary = segm.computeLocalOtsu(self, img)
        # print('con Otsu', np.min(img_binary), np.max(img_binary))
    else:
        # initialize probability config (from file or from GUI)
        segm.initProbabilityConfig(self)

        # generate histogram with both datasets
        if config.getDebugMode() == 2:
            segm.generateHistogram()

        print('* Automatic grayscale segmentation')
        img_binary = segm.automaticGrayscaleSegmentation(self)

    start_time = printElapsedTime(start_time, 'Segment. alg.')
    img_fname = self.getFileName()
    dest_fname = config.getConfigFilename()
    segm.writeProbabilityConfig(img_fname, dest_fname)

    return img_binary

# @profile
def createGraph(graph_props):
    thr_dist = config.getDistanceThreshold()
    centroids_arr = list(graph_props.node_props.getCentroids().values())
    rang_centr = len(centroids_arr)

    distances_list = {}
    angles_list = {}
    centroides_cen = {}

    for i in range(rang_centr):
        for j in range(i+1, rang_centr):
            angle = 0
            dist = calculateDistance(centroids_arr[i][0],centroids_arr[j][0])

            if(dist <= thr_dist):
                angle = calculateAngle(centroids_arr[i][0],centroids_arr[j][0])

                # if (centroids_arr[i][0][0] > centroids_arr[j][0][0]):
                # graph_props.G.add_node(i)
                # graph_props.G.add_node(j)
                # graph_props.G.add_edge(j,i,quality = 0)
                # angles_list[(j,i)] = angle
                # distances_list[(j,i)] = dist
                # else:
                graph_props.G.add_node(j)
                graph_props.G.add_node(i)
                graph_props.G.add_edge(i,j,quality = 0)
                angles_list[(i,j)] = angle
                distances_list[(i,j)] = dist

            centroides_cen[i] = centroids_arr[i][0]
            centroides_cen[j] = centroids_arr[j][0]

    #graph_props.edge_props.setEdges(graph_props.G.edges)
    graph_props.edge_props.setDistances(distances_list)
    graph_props.edge_props.setAngles(angles_list)
    graph_props.node_props.setCoordCentroids(centroides_cen)


    return graph_props

# -------------------------------------------------------------------------------
def removeEdges(edge,graph_props):
    '''
        REMOVE EDGES
        this function remove edges and their properties.

    '''
    if edge in graph_props.G.edges():
        graph_props.edge_props.removeProp(edge)
        graph_props.G.remove_edge(edge[0],edge[1])
    return graph_props

# -------------------------------------------------------------------------------
def removeNodes(node,graph_props):
    '''
        REMOVE NODE
        this function remove nodes and their properties.

    '''
    if node in graph_props.G.node():
        graph_props.node_props.removeProp(node)
        graph_props.G.remove_node(node)
    return graph_props

# -------------------------------------------------------------------------------
def calculateDistance(coords1, coords2):
    '''
        CALCULATE DISTANCE
        this function calculates the distance between two nodes

    '''
    x_side = np.abs(coords2[0]-coords1[0])
    y_side = np.abs(coords2[1]-coords1[1])
    dist = math.floor(math.sqrt((x_side)**2+(y_side)**2))
    return dist
# -------------------------------------------------------------------------------
def calculateAngle(a, b):
    """
    :param a: node coord tuple (x, y)
    :param b: node coord tuple (x, y)
    :return: angle of the ab segment (float)
    Calculates the angle of the segment defined by ab If b(x)<a(x): the segment ba is used
    Else: the segment ab is used
    """
    if (a[0] > b[0]):
        angle = computeAngle(b, a)
    else:
        angle = computeAngle(a, b)
    return angle

# -------------------------------------------------------------------------------
def computeAngle(a,b):
    """
    :param a: node coord tuple (x, y)
    :param b: node coord tuple (x, y)
    :return: angle of the segment (float)
    Compute the angle of the segment defined by a and b
    """
    x = (b[0] - a[0])
    y = (b[1] - a[1])
    angle = math.atan2(y,x) * (180.0 / math.pi)
    return angle

# -------------------------------------------------------------------------------
# calculate angle 3 points
def _angle(p0,p1,p2):
    a = (p1[0]-p0[0])**2 + (p1[1]-p0[1])**2
    b = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2
    c = (p2[0]-p0[0])**2 + (p2[1]-p0[1])**2

    return math.acos( (a+b-c) / math.sqrt(4*a*b) ) * 180/math.pi
# -------------------------------------------------------------------------------
def drawGraph(graph_props, plot_curves=True):
    """
    :param graph_props: GraphProperties object
    :return: None
    Draws the subgraphs over the image
    """
    pos_miss = graph_props.node_props.getCoordMissing()
    pos = graph_props.node_props.getCoordCentroids()

    # generate colormap
    l = len(graph_props.subgraphs.values())
    subgraphs_n = 15
    if l>subgraphs_n:
        subgraphs_n = l
    c = plt.cm.get_cmap('hsv', subgraphs_n+1)
    cont = 0
    margin = 30

    # subgraph's curves
    if plot_curves:
        for s in graph_props.subgraphs:
            x = []
            y = []
            H = graph_props.subgraphs[s]
            if (H.number_of_nodes() > 3):
                for n in H.nodes():
                    x.append(graph_props.node_props.centroids[n][0][0])
                    y.append(graph_props.node_props.centroids[n][0][1])
                xp = np.linspace(min(x)-100, max(x)+100, len(x)+100)
                # plt.ylim(max(y),0)
                if (graph_props.subgraph_props.error_curve[s] > 20):
                    plt.plot(xp,graph_props.subgraph_props.coef_curve[s](xp),'m--',linewidth=1.5)
                    plt.text(x[0],y[0]+margin, str(graph_props.subgraph_props.error_curve[s]), bbox=dict(facecolor='red', alpha=0.5))
                else:
                    plt.plot(xp,graph_props.subgraph_props.coef_curve[s](xp),'b--',linewidth=1.5)
                    plt.text(x[0],y[0]+margin, str(graph_props.subgraph_props.error_curve[s]), bbox=dict(facecolor='grey', alpha=0.5))

    # nodes and edges
    for s in graph_props.subgraphs.values():
        # nx.draw_networkx(s, pos=pos, with_labels = True, edgelist = s.edges(data = True),node_color = c(cont+1), edgecolor = 'w',font_color='black',font_size = 10, node_size = 220)
        nx.draw_networkx(s, pos=pos, with_labels = True, edgelist = s.edges(data = True),node_color = 'green', edgecolor = 'grey',font_color='white',font_size = 10, node_size = 220)
        x = [int(i) for i in s.node()]
        pos_x = pos[x[len(x) - 1]][0] - 20
        pos_y = pos[x[len(x) - 1]][1]
        plt.text(pos_x+margin, pos_y+margin, str(cont), bbox={'facecolor':'w', 'alpha':0.5, 'pad':6})
        cont += 1

    # missing nodes
    for p in range(len(pos_miss)):
        # plt.text(pos_miss[p][0], pos_miss[p][1], str(-1), bbox={'facecolor':'r', 'alpha':0.7, 'pad':8})
        plt.plot(pos_miss[p][0],pos_miss[p][1],'maroon', marker="o",  markersize=15)

# -------------------------------------------------------------------------------
# @profile
def filterUltimasEdges(graph_props):

    graph_props_2 = copy.deepcopy(graph_props)

    for n in list(graph_props.G.nodes()):
        if graph_props.G.degree(n) > 2:
            edge = list(graph_props.G.edges(n))
            m = maxInDictionari(graph_props.getDistancesOfEdges(edge))
            removeEdges(m,graph_props_2)

    return graph_props_2

# -------------------------------------------------------------------------------
def filterEdgesAngles(graph_props):

    graph_props_2 = copy.deepcopy(graph_props)
    list_angle = graph_props.edge_props.getAngleTwoEdge()

    for s in list(list_angle):
        if np.abs(list_angle[s]) > (graph_props.getStdTwoAngles(list(s)[0]) + 1.2*graph_props.getMeanTwoAngles(list(s)[0])):
            if list_angle[s] < 0:
                removeEdges(s[2],graph_props_2)
                # print('\tremoving edge (ang A)', s[2], list_angle[s])
            else:
                removeEdges(s[1],graph_props_2)
                # print('\tremoving edge (ang B)', s[1], list_angle[s])

    return graph_props_2

# -------------------------------------------------------------------------------
def contar_veces(elemento, lista):
    veces = 0
    for i in lista:
        if elemento == i:
            veces += 1
    return veces

# -------------------------------------------------------------------------------
def maxInDictionari(dict_d):
    valores = dict_d.values()
    val_max = max(valores)
    for n in dict_d:
        if dict_d[n] == val_max:
            return n

# -------------------------------------------------------------------------------
def filterEdgesDistance(graph_props):
    graph_props_2 = copy.deepcopy(graph_props)

    if config.use_auto_distance_thresh:
        thresh = config.getDistanceThreshold()
        min = thresh[0]
        max = thresh[1]
    else:
        thresh = 75

    # print('USING dist thres =', thresh)
    # print('edges n', len(list(graph_props.subgraphs)))

    for s in list(graph_props.subgraphs):
        H = graph_props.subgraphs[s]
        for e in list(H.edges()):
            if config.use_auto_distance_thresh:
                if not (min < graph_props.getDistanceOfEdge(e) < max):
                    removeEdges(e,graph_props_2)
                # if min > graph_props.getDistanceOfEdge(e):
                #     print('\tremoving edge (dist)', e, graph_props.getDistanceOfEdge(e))
            else:
                if graph_props.getDistanceOfEdge(e) > thresh:
                    removeEdges(e,graph_props_2)
                # print('\tremoving edge (dist)', e, graph_props.getDistanceOfEdge(e))

    return graph_props_2

# -------------------------------------------------------------------------------
def filterNodeExcentricity(graph_props):

    graph_props_2 = copy.deepcopy(graph_props)

    mean_ex = np.mean(list(graph_props.node_props.getExcentricity().values()))
    std_ex = np.std(list(graph_props.node_props.getExcentricity().values()))
    for s in list(graph_props.subgraphs):
        H = graph_props.subgraphs[s]
        for n in list(H.nodes()):
            if graph_props.getExcentricity(n) < (mean_ex - 2 * std_ex):
                removeNodes(n,graph_props_2)

    return graph_props_2

# -------------------------------------------------------------------------------
def filterNodeDegree(graph_props):
    graph_props_2 = copy.deepcopy(graph_props)
    for n in list(graph_props.G.nodes()):
        if graph_props.G.degree(n) == 0:
            removeNodes(n,graph_props_2)
            # None
    return graph_props_2


# -------------------------------------------------------------------------------
def setCandidatesOfEdges(G):
    Grf = copy.deepcopy(G)
    tuplas_nodes = []
    list_edges_union = []

    cant_nod = G.G.number_of_nodes()

    for s in G.subgraphs:
        H = G.subgraphs[s]
        tuplas_nodes.append([n for n in H.nodes() if H.degree(n) == 1])

    print(tuplas_nodes)

    cont = 0
    for t1 in range(len(tuplas_nodes)-1):
        for t2 in range(t1 + 1,len(tuplas_nodes)):
            for n1 in range(len(tuplas_nodes[t1])):
                if len(tuplas_nodes[t2]) != 0:
                    for n2 in range(len(tuplas_nodes[t2])):
                        dist = calculateDistance(G.getCoordCentroids(tuplas_nodes[t1][n1]),G.getCoordCentroids(tuplas_nodes[t2][n2]))
                        m_d1,s_d1 = G.getMeanDistance(t1), G.getStdDistance(t1)
                        m_d2,s_d2 = G.getMeanDistance(t2), G.getStdDistance(t2)

                        angle_new = calculateAngle(G.getCoordCentroids(tuplas_nodes[t1][n1]),G.getCoordCentroids(tuplas_nodes[t2][n2]))
                        angle_ed1 = Grf.getAngleOfEdge(list(G.G.edges(tuplas_nodes[t1][n1]))[0])
                        angle_ed2 = Grf.getAngleOfEdge(list(G.G.edges(tuplas_nodes[t2][n2]))[0])

                        ma_t1, sa_t1 = G.getMeanAngle(t1), G.getStdAngle(t1)
                        ma_t2, sa_t2 = G.getMeanAngle(t2), G.getStdAngle(t2)
                        mtw_t1, stw_t1 = G.getMeanTwoAngles(t1), G.getStdTwoAngles(t1)
                        mtw_t2, stw_t2 = G.getMeanTwoAngles(t2), G.getStdTwoAngles(t2)

                        rest_ang1 = np.abs(angle_new - angle_ed1)
                        rest_ang2 = np.abs(angle_new - angle_ed2)

                        if (dist <= 3*(m_d1+3*s_d1) or dist <= 3*(m_d2+3*s_d2)):
                            # if (G.getCantNodesSub(t1) >= G.getCantNodesSub(t2)):
                            if (rest_ang1 < mtw_t1+ 4*stw_t1) and (rest_ang2 < mtw_t2+ 4*stw_t2):
                                if (angle_new >= (ma_t1 - 4*sa_t1) and angle_new <= (ma_t1 + 5*sa_t1)) or  (angle_new >= (ma_t2 - 4*sa_t2) and angle_new <= (ma_t2 + 5*sa_t2)):
                                    Grf.subgraphs_edge_candidates.append((tuplas_nodes[t1][n1], tuplas_nodes[t2][n2]))
                            #
                            # if (np.mean((rest_ang1,rest_ang2)) < mtw_t1+ 4*stw_t1):
                            #     if (angle_new >= (ma_t1 - 4*sa_t1) and angle_new <= (ma_t1 + 4*sa_t1)):
                            #         Grf.subgraphs_edge_candidates.append((tuplas_nodes[t1][n1], tuplas_nodes[t2][n2]))
                            #         list_edges_union.append((tuplas_nodes[t1][n1], tuplas_nodes[t2][n2]))
                            #
                            # # else:
                            # if (np.mean((rest_ang1,rest_ang2)) < mtw_t2+ 4*stw_t2):
                            #     if (angle_new >= (ma_t2 - 4*sa_t2) and angle_new <= (ma_t2 + 4*sa_t2)):
                            #         Grf.subgraphs_edge_candidates.append((tuplas_nodes[t1][n1], tuplas_nodes[t2][n2]))
                            #         list_edges_union.append((tuplas_nodes[t1][n1], tuplas_nodes[t2][n2]))
    return Grf

# def findEdges(graph):
#     """
#     :param graph: object to find edge candidates (Graph Properties)
#     :return: Graph Properties object with added candidates
#     Looks for edge candidates between subgraphs and single nodes
#     """
#     Grf = copy.deepcopy(graph)
#     max_loops = 3
#     loop = 0
#
#     while loop < max_loops:
#         tuplas_nodes = []
#         single_nodes = []
#         for s in Grf.subgraphs:
#             H = Grf.subgraphs[s]
#             nodes_deg_0 = [n for n in H.nodes() if H.degree(n) == 0]
#             if len(nodes_deg_0) == 1:
#                 single_nodes.append(nodes_deg_0[0])
#             nodes_deg_1 = [n for n in H.nodes() if H.degree(n) == 1]
#             if 0 < len(nodes_deg_1) <= 2:  # to exclude cases when subgraph has more than 2 nodes with degree == 1
#                 tuplas_nodes.append(nodes_deg_1)
#
#         # print('\n', tuplas_nodes)
#         # print(single_nodes)
#
#         if len(single_nodes) == 0 or len(tuplas_nodes) == 0: # there aren't nodes to evaluate
#             break
#
#         for sg in tuplas_nodes:
#             i = tuplas_nodes.index(sg)
#             sg_mean_d, sg_std_d = Grf.getMeanDistance(i), Grf.getStdDistance(i)
#             sg_std_a = Grf.getStdAngle(i)
#             # print('>', sg, sg_mean_d, sg_std_d)
#             for n1 in sg:
#                 n1_centr = Grf.getCoordCentroids(n1)
#                 n1_neighb = list(Grf.G.neighbors(n1))[0]
#                 n1_neighb_centr = Grf.getCoordCentroids(n1_neighb)
#                 # print(n1, n1_neighb)
#                 # print(n1, 'neigh', Grf.G[n1][0])
#                 for n0 in single_nodes:
#                     n0_centr = Grf.getCoordCentroids(n0)
#                     dist = calculateDistance(n0_centr, n1_centr)
#
#                     if 1*(sg_mean_d-2*sg_std_d) < dist < 2*(sg_mean_d+2*sg_std_d):
#                         # if sg_std_d == 0:
#                         new_edge_angle = calculateAngle(n0_centr, n1_centr)
#                         n1_neighb_angle = calculateAngle(n1_centr, n1_neighb_centr)
#
#                         # print(n1, n0, 'dist=', dist, 'ang=', sg_angle)
#                         # print('\t', n1, n1_neighb, 'ang neighb=', n1_neighb_angle)
#
#                         if n1_neighb_angle - 2*sg_std_a < new_edge_angle < n1_neighb_angle + 2*sg_std_a:
#                             # print('nuevo edge:', n1, n0, 'loop:', loop)
#                             Grf.subgraphs_edge_candidates.append((n1, n0))
#
#         if len(Grf.subgraphs_edge_candidates) == 0:
#             # print('break on loop', loop, ', no candidates')
#             break
#         Grf.addEdgesCandidates()
#         Grf.findSubgraphs()
#         loop += 1
#
#     return Grf

def findEdges(graph):
    """
    :param graph: object to find edge candidates (Graph Properties)
    :return: Graph Properties object with new edges
    Looks for edge candidates between subgraphs
    """
    Grf = copy.deepcopy(graph)
    max_loops = 2
    loop = 0
    connected_subgr = []
    distances = []
    tuples = []

    while loop < max_loops:
        tuplas_nodes = []
        single_nodes = []
        for s in Grf.subgraphs:
            H = Grf.subgraphs[s]
            nodes_deg_0 = [n for n in H.nodes() if H.degree(n) == 0]
            if len(nodes_deg_0) != 0:
                single_nodes.append(nodes_deg_0[0])

            nodes_deg_1 = [n for n in H.nodes() if H.degree(n) == 1]
            if 0 < len(nodes_deg_1):  # to exclude cases when subgraph has more than 2 nodes with degree == 1
                tuplas_nodes.append(nodes_deg_1)

        # print('\ngrado=1', tuplas_nodes)
        # print(single_nodes)

        if len(single_nodes) == 0 or len(tuplas_nodes) == 0:  # there aren't nodes to evaluate
            break

        for sg1 in tuplas_nodes:
            i1 = tuplas_nodes.index(sg1)
            sg1_mean_d, sg1_std_d = Grf.getMeanDistance(i1), Grf.getStdDistance(i1)
            sg1_mean_a, sg1_std_a = Grf.getMeanAngle(i1), Grf.getStdAngle(i1)

            if sg1_std_d == 0:
                sg1_std_d = sg1_mean_d * 0.2
                # print('cero std dist', sg1, sg1_std_d)

            mult_std_dist = 2
            mult_mean_dist = 3
            min_d1 = sg1_mean_d - (mult_std_dist * sg1_std_d)
            max_d1 = (mult_mean_dist * sg1_mean_d) + (mult_std_dist * sg1_std_d)

            # TODO: mejorar este valor por defecto
            if sg1_std_a == 0:
                sg1_std_a = np.abs(sg1_mean_a) * 0.2
                # print('cero std ang', sg1, sg1_std_a)
            # print('>>>', sg1, sg1_mean_d, sg1_std_d)
            # print('>', sg, sg_mean_d, sg_std_d)
            mult_std_ang = 3
            ang_thres_1 = mult_std_ang * sg1_std_a
            max_thres_ang = 30
            if ang_thres_1 > max_thres_ang:
                # print('ang thres sg1 > 30:', ang_thres_1)
                ang_thres_1 = max_thres_ang

            for n1 in sg1:
                n1_centr = Grf.getCoordCentroids(n1)
                n1_neighb = list(Grf.G.neighbors(n1))[0]
                n1_neighb_centr = Grf.getCoordCentroids(n1_neighb)
                # print(n1, n1_neighb)
                # print(n1, 'neigh', Grf.G[n1][0])

                distances = []
                tuples = []

                for n2 in single_nodes:
                    if (sg1, n2) not in connected_subgr:
                        i2 = single_nodes.index(n2)
                        # sg2_mean_d, sg2_std_d = Grf.getMeanDistance(i2), Grf.getStdDistance(i2)
                        # sg2_mean_a, sg2_std_a = Grf.getMeanAngle(i2), Grf.getStdAngle(i2)
                        # if sg2_std_d == 0:
                        #     sg2_std_d = sg2_mean_d * 0.2
                        #     # print('cero dist', sg2, sg2_std_d)
                        # if sg2_std_a == 0:
                        #     sg2_std_a = np.abs(sg2_mean_a) * 0.2
                        #     # print('cero std ang', sg2, sg2_std_a)

                            # for n2 in sg2:
                        n2_centr = Grf.getCoordCentroids(n2)
                        # n2_neighb = list(Grf.G.neighbors(n2))[0]
                        # n2_neighb_centr = Grf.getCoordCentroids(n2_neighb)

                        dist = calculateDistance(n2_centr, n1_centr)
                        # print('\t', n1, n2)
                        # distance min/max values of sg1 and sg2
                        # min_d2 = sg2_mean_d - (mult_std_dist * sg2_std_d)
                        # max_d2 = (mult_mean_dist * sg2_mean_d) + (mult_std_dist * sg2_std_d)

                        # ang_thres_2 = mult_std_ang * sg2_std_a
                        # if ang_thres_2 > max_thres_ang:
                        #     # print('ang thres sg2 > 30:', ang_thres_2)
                        #     ang_thres_2 = max_thres_ang

                        if (min_d1 < dist < max_d1):
                            # if sg_std_d == 0:
                            new_edge_angle = calculateAngle(n2_centr, n1_centr)
                            n1_neighb_angle = calculateAngle(n1_centr, n1_neighb_centr)
                            # n2_neighb_angle = calculateAngle(n2_centr, n2_neighb_centr)
                            min_a1 = n1_neighb_angle - ang_thres_1
                            max_a1 = n1_neighb_angle + ang_thres_1
                            # min_a2 = n2_neighb_angle - ang_thres_2
                            # max_a2 = n2_neighb_angle + ang_thres_2

                            # print(n1, n0, 'dist=', dist, 'ang=', sg_angle)
                            # print('\t', n1, n1_neighb, 'ang neighb=', n1_neighb_angle)

                            if (min_a1 < new_edge_angle < max_a1):
                                # print('nuevo edge (subgr):', n1, n2, 'loop:', loop)
                                # print(n1_neighb_angle, new_edge_angle, n2_neighb_angle)
                                # print(sg1_mean_a, sg1_std_a)
                                # print(sg2_mean_a, sg2_std_a)
                                #
                                # print(min_d1, '<', dist, '<', max_d1)
                                # print(sg1_mean_d, sg1_std_d)
                                #
                                # print(min_d2, '<', dist, '<', max_d2)
                                # print(sg2_mean_d, sg2_std_d)

                                # Grf.subgraphs_edge_candidates.append((n1, n2))
                                # connected_subgr.append((sg1, sg2))
                                tuples.append((n1, n2))
                                distances.append(dist)
                                # print('possible edge', (n1, n2))
                                # print('\t', min_d1, '<', dist ,'<', max_d1, 'and', min_d2 ,'<', dist, '<', max_d2)
                                # print('\t', min_a1, '<', new_edge_angle ,'<', max_a1, 'and', min_a2 ,'<', new_edge_angle, '<', max_a2)

                                # Grf.addEdgesCandidates()
                                # Grf.findSubgraphs()
                                # loop += 1

                                # print('break, loop', loop)
                                # break
                            # else:
                            #     print('\tno ang', n1, n2)
                            # print('\t', min_a1, '<', new_edge_angle, '<', max_a1)
                            # print('\t', n1_neighb_angle, sg1_mean_a, sg1_std_a)
                            # print('\t', min_a2, '<', new_edge_angle, '<', max_a2)
                            # print('\t', n2_neighb_angle, sg2_mean_a, sg2_std_a)

                        # else:
                        #     print('\tno dist', n1, n2)
                    # else:
                    #     print('omitido: ', (sg1, sg2))

                if len(distances) != 0:
                    # add the edge with min distance
                    i = distances.index(np.min(distances))
                    # print('tuples/dists', tuples[i][0], tuples[i][1], distances[i])
                    # print('nuevo edge (single):', tuples[i][0], tuples[i][1])
                    Grf.subgraphs_edge_candidates.append((tuples[i][0], tuples[i][1]))

        if len(Grf.subgraphs_edge_candidates) == 0:
            # print('break on loop', loop, ', no candidates')
            break

        Grf.addEdgesCandidates()
        Grf.findSubgraphs()
        loop += 1
        # print('loop +1')

    return Grf

def findEdgesBetweenSubgraphs(graph):
    """
    :param graph: object to find edge candidates (Graph Properties)
    :return: Graph Properties object with new edges
    Looks for edge candidates between subgraphs
    """
    Grf = copy.deepcopy(graph)
    max_loops = 2
    loop = 0
    connected_subgr = []
    distances = []
    tuples = []

    while loop < max_loops:
        tuplas_nodes = []
        single_nodes = []
        for s in Grf.subgraphs:
            H = Grf.subgraphs[s]
            # nodes_deg_0 = [n for n in H.nodes() if H.degree(n) == 0]
            # if len(nodes_deg_0) != 0:
            #     single_nodes.append(nodes_deg_0[0])

            nodes_deg_1 = [n for n in H.nodes() if H.degree(n) == 1]
            if 0 < len(nodes_deg_1):  # to exclude cases when subgraph has more than 2 nodes with degree == 1
                tuplas_nodes.append(nodes_deg_1)

        # print('\ngrado=1', tuplas_nodes)
        # print(single_nodes)

        if len(tuplas_nodes) == 0:  # there aren't nodes to evaluate
            break

        for sg1 in tuplas_nodes[:-1]:
            i1 = tuplas_nodes.index(sg1)
            sg1_mean_d, sg1_std_d = Grf.getMeanDistance(i1), Grf.getStdDistance(i1)
            sg1_mean_a, sg1_std_a = Grf.getMeanAngle(i1), Grf.getStdAngle(i1)

            if sg1_std_d == 0:
                sg1_std_d = sg1_mean_d * 0.2
                # print('cero std dist', sg1, sg1_std_d)

            mult_std_dist = 2
            mult_mean_dist = 3
            min_d1 = sg1_mean_d - (mult_std_dist * sg1_std_d)
            max_d1 = (mult_mean_dist * sg1_mean_d) + (mult_std_dist * sg1_std_d)

            if sg1_std_a == 0:
                sg1_std_a = np.abs(sg1_mean_a) * 0.2
                # print('cero std ang', sg1, sg1_std_a)
            # print('>>>', sg1, sg1_mean_d, sg1_std_d)
            # print('>', sg, sg_mean_d, sg_std_d)
            mult_std_ang = 3
            ang_thres_1 = mult_std_ang * sg1_std_a
            min_thres_ang = 10
            max_thres_ang = 30
            if ang_thres_1 > max_thres_ang:
                # print('ang thres sg1 > 30:', ang_thres_1)
                ang_thres_1 = max_thres_ang
            if ang_thres_1 < min_thres_ang:
                # print('ang thres sg1 < 10:', ang_thres_1)
                ang_thres_1 = min_thres_ang

            for n1 in sg1:
                n1_centr = Grf.getCoordCentroids(n1)
                n1_neighb = list(Grf.G.neighbors(n1))[0]
                n1_neighb_centr = Grf.getCoordCentroids(n1_neighb)
                # print(n1, n1_neighb)
                # print(n1, 'neigh', Grf.G[n1][0])

                for sg2 in tuplas_nodes[i1+1:]:
                    distances = []
                    tuples = []
                    if (sg1, sg2) not in connected_subgr:
                        i2 = tuplas_nodes.index(sg2)
                        sg2_mean_d, sg2_std_d = Grf.getMeanDistance(i2), Grf.getStdDistance(i2)
                        sg2_mean_a, sg2_std_a = Grf.getMeanAngle(i2), Grf.getStdAngle(i2)
                        if sg2_std_d == 0:
                            sg2_std_d = sg2_mean_d * 0.2
                            # print('cero dist', sg2, sg2_std_d)
                        if sg2_std_a == 0:
                            # sg2_std_a = np.abs(sg2_mean_a) * 0.2
                            sg2_std_a = max_thres_ang
                            # print('cero std ang', sg2, sg2_std_a)

                        for n2 in sg2:
                            n2_centr = Grf.getCoordCentroids(n2)
                            n2_neighb = list(Grf.G.neighbors(n2))[0]
                            n2_neighb_centr = Grf.getCoordCentroids(n2_neighb)

                            dist = calculateDistance(n2_centr, n1_centr)
                            # print('\t', n1, n2)
                            # distance min/max values of sg1 and sg2
                            min_d2 = sg2_mean_d - (mult_std_dist * sg2_std_d)
                            max_d2 = (mult_mean_dist * sg2_mean_d) + (mult_std_dist * sg2_std_d)

                            if min_d1 > max_d1:
                                aux = min_d1
                                min_d1 = max_d1
                                max_d1 = aux

                            if min_d2 > max_d2:
                                aux = min_d2
                                min_d2 = max_d2
                                max_d2 = aux

                            if (min_d1 < dist < max_d1) and (min_d2 < dist < max_d2):
                                # if sg_std_d == 0:
                                ang_thres_2 = mult_std_ang * sg2_std_a
                                if ang_thres_2 > max_thres_ang:
                                    # print('ang thres sg2 > 30:', ang_thres_2)
                                    ang_thres_2 = max_thres_ang
                                if ang_thres_2 < min_thres_ang:
                                    # print('ang thres sg2 > 30:', ang_thres_2)
                                    ang_thres_2 = min_thres_ang

                                new_edge_angle = calculateAngle(n2_centr, n1_centr)
                                n1_neighb_angle = calculateAngle(n1_centr, n1_neighb_centr)
                                n2_neighb_angle = calculateAngle(n2_centr, n2_neighb_centr)
                                min_a1 = n1_neighb_angle - ang_thres_1
                                max_a1 = n1_neighb_angle + ang_thres_1
                                min_a2 = n2_neighb_angle - ang_thres_2
                                max_a2 = n2_neighb_angle + ang_thres_2

                                # TODO: verificar si es necesario invertir el orden del min/max
                                # print(n1, n0, 'dist=', dist, 'ang=', sg_angle)
                                # print('\t', n1, n1_neighb, 'ang neighb=', n1_neighb_angle)

                                if (min_a1 < new_edge_angle < max_a1) and (min_a2 < new_edge_angle < max_a2):
                                    # print('nuevo edge (subgr):', n1, n2, 'loop:', loop)
                                    # print(n1_neighb_angle, new_edge_angle, n2_neighb_angle)
                                    # print(sg1_mean_a, sg1_std_a)
                                    # print(sg2_mean_a, sg2_std_a)
                                    #
                                    # print(min_d1, '<', dist, '<', max_d1)
                                    # print(sg1_mean_d, sg1_std_d)
                                    #
                                    # print(min_d2, '<', dist, '<', max_d2)
                                    # print(sg2_mean_d, sg2_std_d)

                                    # Grf.subgraphs_edge_candidates.append((n1, n2))
                                    # connected_subgr.append((sg1, sg2))
                                    tuples.append((n1, n2))
                                    distances.append(dist)
                                    # print('possible edge', (n1, n2))
                                    # print('\t', min_d1, '<', dist ,'<', max_d1, 'and', min_d2 ,'<', dist, '<', max_d2)
                                    # print('\t', min_a1, '<', new_edge_angle ,'<', max_a1, 'and', min_a2 ,'<', new_edge_angle, '<', max_a2)

                                    # Grf.addEdgesCandidates()
                                    # Grf.findSubgraphs()
                                    # loop += 1

                                    # print('break, loop', loop)
                                    # break
                            #     else:
                            #         print('\tno ang', n1, n2)
                            #         print('\t', min_a1, '<', new_edge_angle, '<', max_a1)
                            #         print('\t\t', n1_neighb_angle, sg1_mean_a, sg1_std_a)
                            #         print('\t', min_a2, '<', new_edge_angle, '<', max_a2)
                            #         print('\t\t', n2_neighb_angle, sg2_mean_a, sg2_std_a)
                            #
                            # else:
                            #     print('\tno dist', n1, n2)
                    # else:
                    #     print('omitido: ', (sg1, sg2))

                    if len(distances) != 0:
                        # add the edge with min distance
                        i = distances.index(np.min(distances))
                        # print('tuples/dists', tuples[i][0], tuples[i][1], distances[i])
                        # print('\tnuevo edge (subgr):', tuples[i][0], tuples[i][1])
                        Grf.subgraphs_edge_candidates.append((tuples[i][0], tuples[i][1]))

        if len(Grf.subgraphs_edge_candidates) == 0:
            # print('break on loop', loop, ', no candidates')
            break

        Grf.addEdgesCandidates()
        Grf.findSubgraphs()
        loop += 1
        # print('loop +1')

    return Grf



#-------------------------------------------------------------------------------
# Generate list of nodes missing

def AddNodes(grf):
    coord = []
    for s in grf.subgraphs:
        H = grf.subgraphs[s]
        for e in H.edges():
            dist = grf.getDistanceOfEdge(e)
            if (dist > grf.getMeanDistance(s)+2.3*grf.getStdDistance(s)):
                p1 = grf.getCoordCentroids(e[0])
                p2 = grf.getCoordCentroids(e[1])
                if (dist/2 < grf.getMeanDistance(s)):
                    d_x0 = np.abs(p1[0]-p2[0])/2
                    d_y0 = np.abs(p1[1]-p2[1])/2
                    if (p1[0] < p2[0] and p1[1] < p2[1]):
                        coord.append((p1[0] + d_x0,p1[1] + d_y0))
                    elif (p1[0] < p2[0] and p1[1] > p2[1]):
                        coord.append((p1[0] + d_x0,p2[1] + d_y0))
                    elif (p1[0] > p2[0] and p1[1] < p2[1]):
                        coord.append((p2[0] + d_x0,p1[1] + d_y0))
                    else:
                        coord.append((p2[0] + d_x0,p2[1] + d_y0))
                else:
                    d_x0 = np.abs(p1[0]-p2[0])/3
                    d_y0 = np.abs(p1[1]-p2[1])/3
                    if (p1[0] < p2[0] and p1[1] < p2[1]):
                        coord.append((p1[0] + d_x0,p1[1] + d_y0))
                        coord.append((p1[0] + 2*d_x0,p1[1] + 2*d_y0))
                    elif (p1[0] < p2[0] and p1[1] > p2[1]):
                        coord.append((p1[0] + d_x0,p2[1] + d_y0))
                        coord.append((p1[0] + 2*d_x0,p2[1] + 2*d_y0))
                    elif (p1[0] > p2[0] and p1[1] < p2[1]):
                        coord.append((p2[0] + d_x0,p1[1] + d_y0))
                        coord.append((p2[0] + 2*d_x0,p1[1] + 2*d_y0))
                    else:
                        coord.append((p2[0] + d_x0,p2[1] + d_y0))
                        coord.append((p2[0] + 2*d_x0,p2[1] + 2*d_y0))
    grf.node_props.setCoordMissing(coord)

# -------------------------------------------------------------------------------
# Filter subgraph
# @profile
def filterSubgraph(graph_props):
    start_time = datetime.datetime.now()

    graph_props_0 = filterEdgesDistance(graph_props)
    graph_props_0.findSubgraphs()
    start_time = printElapsedTime(start_time, '\tEdges dist')

    # graph_props_1 = filterEdgesAngles(graph_props_0)
    # graph_props_1.findSubgraphs()
    # start_time = printElapsedTime(start_time, '\tEdges ang')

    graph_props_2 = filterNodeExcentricity(graph_props_0)
    graph_props_2.findSubgraphs()
    start_time = printElapsedTime(start_time, '\tNodes exc')

    return graph_props_2

#-------------------------------------------------------------------------------
def cutRemains(img_RGB):
    plt.imshow(img_RGB)
    coords = plt.ginput(-1)
    poly = Polygon(coords)
    return poly
# -------------------------------------------------------------------------------
# Print attributes of subgraph
def printSubgraph(graph_props):
    f = open(config.getReportPath(),'w')

    f.write('\nLIST WITH SUBGRAPH PROPERTIES\n')
    f.write('===================================================================\n')

    f.write('\nSUBGRAPH: \n')
    f.write('Number of subgraph = ' + str(len(graph_props.subgraphs)) + '\n')
    f.write('...................................................................\n')

    for s in range(len(graph_props.subgraphs)):
        subg = graph_props.subgraphs[s]

        f.write('\nSubgraph ID: ' + str(s) + '\n')
        f.write('\tNumber of nodes = ' + str(subg.number_of_nodes()) + '\n')
        f.write('\tNumber of edges = ' + str(subg.number_of_edges()) + '\n')
        f.write('\tMean of dist = ' + str(graph_props.getMeanDistance(s)) + '\n')
        # f.write('\tMean of area = ' + str(mean_areas) + '\n')
        f.write('\tMean of angle = ' + str(graph_props.getMeanAngle(s))
                                        + '\tStd = ' + str(graph_props.getStdAngle(s)) + '\n')

        f.write('\t\tList of Nodes: \n\t\t------------------------------------------------------------------\n')
        for n in subg:
            f.write('\t\t\tNode ID: ' + str(n) + '\n')
            f.write('\t\t\t\tGrado: ' + str(subg.degree(n))
                                                        + '\tCentroid coords: '
                                                        + str(np.asarray(graph_props.node_props.centroids[n]))
                                                        + '\tRegion area: ' + str(graph_props.getAreaOfNode(n))
                                                        + '\n')

        f.write('\t\tList of Edges: \n\t\t------------------------------------------------------------------\n')
        for e in subg.edges:
            f.write('\t\t\tEdge ID: ' + str(graph_props.getIndexOfEdge(e)) + '\n')
            f.write('\t\t\t\tNodes: ' + str(e) + '\tDistance: ' + str(graph_props.getDistanceOfEdge(e))+ '\n')
            f.write('\t\t\t\tAngle: ' + str(graph_props.getAngleOfEdge(e)) + '\n')

    f.close()

# -------------------------------------------------------------------------------
# set threshold color
def setThresholdcolor(self,p):
    plt.imshow(self.img_RGB)
    p = plt.ginput(12)
    r_i = 0
    g_i = 0
    b_i = 0
    for i in range(len(p)):
        r_i = self.img_RGB.getpixel((p[i][0],p[i][1]))[0] + r_i
        g_i = self.img_RGB.getpixel((p[i][0],p[i][1]))[1] + g_i
        b_i = self.img_RGB.getpixel((p[i][0],p[i][1]))[2] + b_i
    r,g,b = r_i/len(p),g_i/len(p),b_i/len(p)
    print('r:',r,'g:',g,'b:',b)
    config.setRGBThreshold([(r-25,r+25),(g-25,g+25),(b-25,g+25)])

# -------------------------------------------------------------------------------
# set threshold grayscale
def automaticGrayThreshold(self):
    segm = Segmentation()
    segm.initProbabilityConfig(self)

    # generate histogram with both datasets
    if config.getDebugMode() == 2:
        segm.generateHistogram()

    img_binary = segm.generateBinaryImage(self)

    img_fname = self.getFileName()
    dest_fname = config.getConfigFilename()
    segm.writeProbabilityConfig(img_fname, dest_fname)

    return img_binary

#--------------------------------------------------------------------------------
def distMin(P,U):
    '''
        DISTANCE MIN
        this function calculates the minimum distance from a point to a curve

        @P: Point of interest (x,y)
        @U: List of pints on the curve [(x,y)..(x,y)]
    '''
    dist = []
    for i in range(len(U)):
        dist.append(calculateDistance(P,U[i]))
    dist_min = np.min(dist)
    return dist.index(dist_min)

# @profile
def dividirSurco(grf,degree,error_max):

    grf2 = copy.deepcopy(grf)
    for s in grf.subgraphs:
        if grf.subgraph_props.error_curve[s] > error_max:
            H = grf.subgraphs[s]
            node_0 = []
            node_cons = []
            N = 4
            umb_err = 20
            # print('nodes   ', H.nodes())
            for n in H.nodes():
                if H.degree(n) == 1:
                    # print('\tappend', n)
                    node_0.append(n)

            if len(node_0) > 0:
                n_x  = node_0[0]
                n_s = node_0[0]

                for cont in range(len(list(H.nodes()))):
                    node_cons.append(n_s)
                    consect = []
                    for i in H.neighbors(n_s):
                        if i not in node_cons:
                            n_s = i
                error = 0
                while (error < umb_err):
                    # print('---> ', N, node_cons, range(N), n_s)
                    try:
                        x = [grf.getCoordCentroids(node_cons[n])[0] for n in range(N)]
                        y = [grf.getCoordCentroids(node_cons[n])[1] for n in range(N)]
                    except IndexError:
                        break
                    z = np.polyfit(x,y, degree) # genera parametros de la curva
                    p = np.poly1d(z) # función curva
                    e = np.abs(np.polyval(z, x) - y)
                    error = np.sum(e)/len(x)
                    N += 1

                if config.getDebugMode() == 1:
                    x2 = [grf.getCoordCentroids(n)[0] for n in H.nodes()]
                    y2 = [grf.getCoordCentroids(n)[1] for n in H.nodes()]

                    plt.figure()
                    plt.axis('equal')
                    plt.ylim(max(y),0)
                    xp = np.linspace(min(x), max(x), len(x)+100)
                    plt.plot(x2,y2,'.',xp,p(xp),'r-')
                # print('\n->', N-1, node_cons)
                # print('-->', node_cons[N-1])
                try:
                    grf2 = removeNodes(node_cons[N-1],grf2)
                except IndexError:
                    pass

    if config.getDebugMode() == 1:
        plt.show()

    plt.close()
    return grf2

# -------------------------------------------------------------------------------
def plotPolynomial(grf):
    '''
        POLYNOMIAL REGRESSION
        this function generates a curve adjustment to the subgraphs
    '''
    plt.figure()
    plt.axis('equal')
    for s in grf.subgraphs:
        x = []
        y = []
        H = grf.subgraphs[s]
        if (H.number_of_nodes() > 3):
            for n in H.nodes():
                x.append(grf.node_props.centroids[n][0][0])
                y.append(grf.node_props.centroids[n][0][1])
            xp = np.linspace(min(x)-100, max(x)+100, len(x)+100)
            plt.ylim(max(y),0)
            if (grf.subgraph_props.error_curve[s] > 20):
                plt.plot(x,y,'.',xp,grf.subgraph_props.coef_curve[s](xp),'r-')
                plt.text(x[0],y[0],str(grf.subgraph_props.error_curve[s]), bbox=dict(facecolor='red', alpha=0.58))
            else:
                plt.plot(x,y,'.',xp,grf.subgraph_props.coef_curve[s](xp),'g-')
                plt.text(x[0],y[0],str(grf.subgraph_props.error_curve[s]), bbox=dict(facecolor='green', alpha=0.58))

    if config.getDebugMode() == 1:
        plt.show()


# def polynomialRegression(grf,degree):
#     '''
#         POLYNOMIAL REGRESSION
#         this function generates a curve adjustment to the subgraphs
#     '''

#     curve = {}
#     for i in grf.subgraphs:
#         H = grf.subgraphs[i]
#         x = []
#         y = []
#         for n in H.nodes():
#             x.append(grf.node_props.centroids[n][0][0]) #Cargo coord x del centroide
#             y.append(grf.node_props.centroids[n][0][1]) #Cargo coord y del centroide
#         curve[i] = (x,y) #Concateno en un diccionario para cada subgr (x[],y[])

#     plt.axis('equal')
#     # plt.ylim(1200, 0)
#     for i in curve:
#         x = curve[i][0]
#         y = curve[i][1]
#         plt.ylim(max(y),0)
#         z = np.polyfit(x,y, degree)
#         p = np.poly1d(z)
#         xp = np.linspace(min(x), max(x), len(x))
#         e = np.abs(np.polyval(z, x) - y)
#         error = np.sum(e)/len(x)
#         plt.plot(x,y,'.',xp, p(xp),'-')
#         plt.text(x[len(x)-1],y[len(y)-1],str(i))
#         plt.text(x[0],y[0],str(error), bbox=dict(facecolor='green', alpha=0.58))
#         print(i,':\t',error)

#     plt.show()

#-----------------------------------------------------------------------
# runs the detection on a single image
# @profile
def processImage():
    det = Detection()
    det.process()
    config.printObjInfoToLog(det)
    del det
    # return det

# loops on the given folder (from settings)
def processFolder():
    # variables initialization
    # obj_list = []
    index = 0

    source_dir = config.getSourceFolderName()
    listing = os.listdir(source_dir)
    for file in listing:
        for search_str in config.getSupportedFormats():
            if search_str.lower() in file.lower():
                config.setImageFilename(file)
                # obj_list.append(processImage())
                processImage()
                index = index + 1

    return index

# runs the detection on the given file/folder
def run(file):
    if (os.path.isdir(file)):
        # if directory
        config.setSourceFolderName(file)
        proc_list_n = processFolder()
        config.printListInfoToLog(proc_list_n)
    else:
        # if file
        dir, filename = os.path.split(file)
        config.setSourceFolderName(dir)
        config.setImageFilename(filename)
        proc_img = processImage()

def printElapsedTime(start_time, msg):
    end_time = datetime.datetime.now()
    tot_time = end_time - start_time
    print("\t"+msg+":\t" + str(tot_time)[2:11])
    return end_time

class Detection(object):

    def __init__(self):
        # IMAGE PROPERTIES
        image_file = config.getImageFilename()

        # PHASE 1
        # original image (PIL Image object)
        if config.use_autocontrast:
            # from skimage import exposure
            # original = exposure.equalize_hist(Image.open(config.getImagePath(image_file)))
            original = ImageOps.autocontrast(Image.open(config.getImagePath(image_file)),0.5)
        else:
            original = Image.open(config.getImagePath(image_file))
        # apply resizing (from settings)
        self.img_RGB = original.resize( [int(config.getResize() * s) for s in original.size] )
        self.img_Grayscale = self.img_RGB.convert('LA')
        # self.img_Grayscale.save('gray.png')
        self.img_VARI = []
        # image filename
        self.img_file = image_file
        # width, height of the image
        self.img_width, self.img_height = self.img_RGB.size
        # margin (in pixels)
        self.margin = int(self.img_height*(config.getExclusionMargin()*0.01))
        # number of detected regions
        self.regions_n = 0
        # distance between a corner of the image and it's centroid
        self.img_dist = 0
        # image centroid coords
        self.img_centroid = [-1, -1]

        # GROUP PROPERTIES
        # bounding box of the group, including centroid = [x, y, width, height, centroid_x, centroid_y]
        self.group_bbox = [-1, -1, -1, -1, -1, -1]
        # area of regions detected and filtered
        self.regions_area = []

        # calculated distance between group centroid and image centroid
        self.final_distance = 0
        # calculated score of the detection (from 0 to 1)
        self.final_score = -1

    # returns the mask (lookup table) to apply the threshold
    def mask(self, low, high):
        return [255 if low <= x <= high else 0 for x in range(0, 256)]

    # applies RGB threshold and converts into binary
    def applyRGBThreshold(self):
        thres = config.RGB_threshold
        mask_R = self.mask(thres[0][0], thres[0][1])
        mask_G = self.mask(thres[1][0], thres[1][1])
        mask_B = self.mask(thres[2][0], thres[2][1])
        img_binary = self.img_RGB.point(mask_R+mask_G+mask_B).convert('L').point([0]*255+[255])
        return img_binary

    # @profile
    def saveFigure(self, graph_props, nombre, plot_curves=True):
        fig, ax = plt.subplots(figsize=config.subplot_size)
        # ax.imshow(config.arr_overlay)
        # ax.imshow(array(self.img_RGB))

        ax = self.drawRegions(graph_props, ax)
        drawGraph(graph_props, plot_curves)
        ax.set_axis_off()
        ax.invert_yaxis()
        plt.tight_layout()
        plt.savefig(config.getPlotPath(nombre))
        plt.close()

    def filterRegionsByArea(self, arr_labeled, node_props, poly=None):
        centroids_arr = {}
        areas_arr = {}
        bboxes_arr = {}
        eccentricity = {}
        error_area = {}
        intensity = {}
        #poly = cutRemains(self.img_RGB)
        if not poly:
            poly = cutRemains(self.img_RGB)

        # variables to get group bbox coords
        min_x_group=self.img_width
        min_y_group=self.img_height
        max_x_group=0
        max_y_group=0

        cont = 0
        for region in regionprops(arr_labeled):
            min_y_bbox, min_x_bbox, max_y_bbox, max_x_bbox = region.bbox
            p = Point((min_x_bbox+max_x_bbox)/2, (min_y_bbox+max_y_bbox)/2)
            if region.area >= config.getMinAreaSize() and p.within(poly):

                # (major_axis, minor_axis)
                eccentricity[cont] = (region.minor_axis_length/region.major_axis_length)
                # generate array of area
                areas_arr[cont] = region.convex_area
                # generate array boxes
                min_y_bbox, min_x_bbox, max_y_bbox, max_x_bbox = region.bbox
                # generate array of bbox
                bboxes_arr[cont] = [min_x_bbox, min_y_bbox, max_x_bbox, max_y_bbox]
                # area box
                error_area[cont] = np.abs((np.abs(min_y_bbox - max_y_bbox)*np.abs(min_x_bbox-max_x_bbox)) - areas_arr[cont])/(np.abs(min_y_bbox - max_y_bbox)*np.abs(min_x_bbox-max_x_bbox))
                # generate array of centroids
                centroids_arr[cont] = [((min_x_bbox+max_x_bbox)/2,(min_y_bbox+max_y_bbox)/2)]

                # print(cont,'ecc:',(region.minor_axis_length/region.major_axis_length), 'elotro:',region.eccentricity)

                cont = cont + 1

                # get coords of group bbox
                if max_y_bbox > max_y_group:
                    max_y_group = max_y_bbox
                if min_x_bbox < min_x_group:
                    min_x_group = min_x_bbox
                if min_y_bbox < min_y_group:
                    min_y_group = min_y_bbox
                if max_x_bbox > max_x_group:
                    max_x_group = max_x_bbox

                # count number of regions on image
                self.regions_n = self.regions_n + 1
                self.regions_area.append(region.area)

        # compute bounding box and centroid of the group = [x, y, width, height, centroid_x, centroid_y]
        group_width = max_x_group-min_x_group
        group_height = max_y_group-min_y_group
        self.group_bbox = [min_x_group, min_y_group, group_width, group_height, min_x_group+group_width, min_y_group+group_height]

        # set attributes to object
        node_props.setCentroids(centroids_arr)
        node_props.setAreas(areas_arr)
        node_props.setBBoxes(bboxes_arr)
        node_props.setExcentriciy(eccentricity)
        node_props.setErrorArea(error_area)

        return node_props

    def drawRegions(self, graph_props, ax):
        bbox = graph_props.node_props.getBBoxes()

        if config.getDebugMode() >= 1:
            for i in graph_props.G.nodes():
                ## draw rectangle around segmented areas
                # rect = mpatches.Rectangle((bbox[i][0], bbox[i][1]), bbox[i][2]-bbox[i][0], bbox[i][3]-bbox[i][1],
                #                        fill=False, edgecolor='w', linewidth=1)
                # ax.add_patch(rect)

                # draw centroid over segmented areas
                centroid = mpatches.Circle( ((bbox[i][2]+bbox[i][0])/2, ((bbox[i][3]+bbox[i][1])/2)), 0.5, fill=False, edgecolor='yellow', linewidth=1)
                ax.add_patch(centroid)
        return ax

    def automaticDistanceThreshold(self, graph):
        """
        :return: min threshold (int), max threshold (int)
        Computes min/max distance threshold for the given graph
        """
        print('* Automatic distance threshold')

        dist_list = []
        for s in list(graph.subgraphs):
            H = graph.subgraphs[s]
            for e in list(H.edges()):
                dist_list.append(graph.getDistanceOfEdge(e))

        # compute Gaussian Kernel Density Estimation
        from scipy import stats
        dist_list = np.array(dist_list)
        kde = stats.gaussian_kde(dist_list)
        # bins = np.linspace(dist_list.min(), dist_list.max(), 100)
        bins = np.linspace(dist_list.min(), dist_list.max(), dist_list.max() - dist_list.min())
        estimation = kde(bins)

        # find maxs, mins of estimation
        import peakutils
        maxs = peakutils.indexes(estimation)
        mins = peakutils.indexes(-estimation)
        # print('maxs', dist_list.min()+maxs)
        # print('mins', dist_list.min()+mins)

        min = dist_list.min() + mins[0]
        max = dist_list.min() + maxs[0]

        diff = np.abs(maxs[0]-mins[0])
        # diff_2 = int(diff*0.8)
        min_1 = max-diff
        min_2 = max+diff
        # print(min_1, min_2, diff)

        if config.getDebugMode() == 2 or config.getDebugMode() == 1:
            plt.plot(bins, estimation, 'c--')

            bins = np.linspace(0, np.max(dist_list), num=np.max(dist_list))
            plt.hist(dist_list, facecolor='grey', label='Dist grafo inicial', bins=bins, normed=True, alpha=0.6)
            plt.legend()

            plt.title(self.getFileName())
            plt.ylabel("Pixels")
            plt.xlabel("Distances")
            plt.plot(max, estimation[maxs[0]], '*k')
            plt.plot(min, estimation[mins[0]], '*r')
            fname = config.getPlotPath(config.getImageFilename()+'_distances')

            # plt.plot([max-diff, max-diff], [0, estimation[maxs[0]]], 'g.-', label='min_dist')
            # plt.plot([max+diff, max+diff], [0, estimation[maxs[0]]], 'm.-', label='max_dist')

            plt.plot([min_1, min_1], [0, estimation[maxs[0]]], 'g--', label='min_dist')
            plt.plot([min_2, min_2], [0, estimation[maxs[0]]], 'm--', label='max_dist')

            if config.getDebugMode() == 2:
                plt.savefig(fname)
            if config.getDebugMode() == 1:
                plt.show()

        return min_1, min_2

    # applies threshold, detects regions, calculates score

    # @profile
    def process(self):

        # SEGMENTATION #------------------------------

        start_time = datetime.datetime.now()
        start_time_process = start_time

        print('\nProcessing:', config.getImageFilename())
        print("\tStarted at: " + str(start_time)[11:23])

        # PHASE 2
        # # calculate distance min between trees
        # # # TODO: set area min
        # plt.imshow(self.img_RGB)
        # p = plt.ginput(-1)
        # # # # dist = calculateDistance(p[0],p[1])
        # setThresholdcolor(self,p)

        # Selection of segmentation threshold type
        if config.algorithm != 0:
            arr_binary = automaticSegmentation(self)
        else:
            # apply manual RGB threshold and convert into binary
            img_binary = self.applyRGBThreshold()
            arr_binary = array(img_binary)

            if config.getDebugMode() == 2:
                # save binary image
                img_binary.save(config.getBinaryPath(self.img_file))

        if config.getDebugMode() == 2:
            # create destination folder if not exists
            bin_folder = config.getBinaryFolderPath()
            if not os.path.exists(bin_folder):
                os.makedirs(bin_folder)
        start_time = printElapsedTime(start_time, 'Segmentation')

        # POSTPROCESSING #------------------------------
        # PHASE 3
        # Binary closing
        arr_closed = closing(arr_binary, square(3))
        del arr_binary

        # configure size of subplots
        config.subplot_size = (arr_closed.shape[1]/100, arr_closed.shape[0]/100)

        if config.getDebugMode() == 2:
            # save closed binary image
            cls_binary = Image.fromarray(arr_closed)
            cls_binary.save(config.getClosingPath(self.img_file))
            # print(np.min(cls_binary))
            # print(np.max(cls_binary))
        start_time = printElapsedTime(start_time, 'Postprocess.')

        # PHASE 4
        # Labeling
        #arr_labeled = label(arr_cleared)graph_props.edge_props.edges
        # def axplot(arr_closed,arr_RGB):

        # convert image into array
        arr_RGB = array(self.img_RGB)
        plt.close('all')
        arr_labeled = label(arr_closed)
        del arr_closed
        config.arr_overlay = label2rgb(arr_labeled, image=arr_RGB, alpha=0.2)
        start_time = printElapsedTime(start_time, 'Labeling')

        # return arr_labeled, ax

        # arr_labeled, ax = axplot(arr_closed,arr_RGB)
        # ###############################################################################################
        # ===============================================================================================
        # ###############################################################################################
        '''
        -------------------------------------------------------------------------------------------------
            1) Generate graph and properties
            2) Generate subgraphs and properties of subgraph
            3) Filter the subgraph
                a) Filter for edges
                b) Filter for node
            4) Draw complete graph
            5) Print properties of complete graph
        -------------------------------------------------------------------------------------------------
        '''
        graph_props_v0 = GraphProperties()

        # PHASE 5
        # filter detected regions by area
        graph_props_v0.node_props = self.filterRegionsByArea(arr_labeled, graph_props_v0.node_props)

        # PHASE 6 & 7
        # calculate dist between centroids
        # TODO: use dynamic threshold

        # 1 - Create Graph v0 and subgraph
        # ---------------------------------------------------------
        graph_props_v0 = createGraph(graph_props_v0)
        graph_props_v0.findSubgraphs()
        start_time = printElapsedTime(start_time, 'Initial graph')
        self.saveFigure(graph_props_v0, config.getImageFilename()+'_v0', False)


        #self.saveFigure(graph_props_v0,config.getImageFilename())

        # self.saveFigure(graph_props_v0,'prueba_00.jpg')
        # 2 - 1° filtered to the subgraph
        #   - Filter for distance
        #   - Filter for angles
        #   - Filter for nodes
        # ---------------------------------------------------------

        if config.use_auto_distance_thresh:
            min_dist, max_dist = self.automaticDistanceThreshold(graph_props_v0)
            config.setDistanceThreshold([min_dist, max_dist])

        graph_props_v1 = filterSubgraph(graph_props_v0)
        start_time = printElapsedTime(start_time, 'Subgraph filtering')
        self.saveFigure(graph_props_v1, config.getImageFilename()+'_v1', False)

        # graph_props_v2 = filterSubgraph(graph_props_v1)
        # graph_props_v2.findSubgraphs()
        # self.saveFigure(graph_props_v2, 'arboles_02.jpg')

        # # 3 - Set to the candidates of edges
        # #   - Search of candidates
        # #   - Add of setCandidatesOfEdges
        # #   - Draw of candidates
        # # ---------------------------------------------------------
        graph_props_v3 = findEdges(graph_props_v1)
        graph_props_v3 = findEdgesBetweenSubgraphs(graph_props_v3)
        # graph_props_v3.addEdgesCandidates()
        # graph_props_v3.findSubgraphs()
        start_time = printElapsedTime(start_time, 'Edge candidates')
        self.saveFigure(graph_props_v3, config.getImageFilename()+'_v3', False)

        # # 4 - Filter the nodes of degree == 0
        # # ---------------------------------------------------------
        graph_props_v4 = filterNodeDegree(graph_props_v3)
        graph_props_v4.findSubgraphs()
        start_time = printElapsedTime(start_time, 'Node filtering: degree')
        self.saveFigure(graph_props_v4, config.getImageFilename()+'_v4')

        # # 5 - Last filter of edges
        # # ---------------------------------------------------------
        for i in range(3):
            graph_props_vf = filterUltimasEdges(graph_props_v4)
        graph_props_vf = filterNodeDegree(graph_props_vf)
        graph_props_vf.findSubgraphs()
        start_time = printElapsedTime(start_time, 'Ultimas edges')
        self.saveFigure(graph_props_vf, config.getImageFilename()+'_vf')

        AddNodes(graph_props_vf)

        degree = 2
        error_max = 20
        grf2 = dividirSurco(graph_props_vf, degree, error_max)
        grf2.findSubgraphs()

        # Compute curve of subgraphs
        if config.use_polynomial_regression:
            if config.getDebugMode() == 1:
                plotPolynomial(graph_props_vf)
                plotPolynomial(grf2)
                start_time = printElapsedTime(start_time, 'Polynomial regression')

        self.saveFigure(grf2, config.getImageFilename()+'_grf2')

        end_time = datetime.datetime.now()
        tot_time = end_time - start_time_process
        print("Total:\t" + str(tot_time)[3:11])

    def calculateCentroid(self, x_side, y_side):
        centroid = [x_side/2, y_side/2]
        return centroid

    def calculateImageCentroid(self):
        self.img_centroid = self.calculateCentroid(self.img_width, self.img_height)

    def calculateGroupCentroid(self, x_side, y_side):
        self.group_centroid = self.calculateCentroid(x_side, y_side)

    # calculates distance between two given arrays of coords
    def calculateDistance(self, coords1, coords2):
        x_side = coords2[0]-coords1[0]
        y_side = coords2[1]-coords1[1]
        dist = math.sqrt((x_side)**2+(y_side)**2)
        return dist

    # calculates the score, based on reference distance and centroid-to-centroid distance
    def calculateScore(self):
        self.final_score = format(self.final_distance/self.img_dist, '.2f')

    # returns the image's centroid coordinates [x,y]
    def getImageCentroid(self):
        return self.img_centroid

    # returns number of detected regions on the image (integer)
    def getRegionsN(self):
        return self.regions_n

    # returns the score of the detection
    def getScore(self):
        return self.final_score

    # returns the name of the image file
    def getFileName(self):
        return self.img_file

    # returns the width of the image
    def getImageWidth(self):
        return self.img_width

    # returns the width of the image
    def getImageHeight(self):
        return self.img_height

    # returns the area of each region detected and filtered
    def getRegionsArea(self):
        return self.regions_area
