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
import settings as config
from graph_properties import GraphProperties
from shapely.geometry import LineString, Polygon, Point
from segmentation import Segmentation
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
def automaticSegmentation(self):
    segm = Segmentation()

    # use_global_otsu = True
    methods = ['manual', 'auto_grayscale', 'global_otsu', 'local_otsu']
    algo = config.algorithm
    img = []

    start_time = datetime.datetime.now()
    print("\tauto segm Started at: " + str(start_time))


    # VARI descriptor
    if config.compute_VARI:
        print('* VARI Descriptor')
        # self.img_VARI = segm.computeVARI(self)
        if config.multiprocess_VARI:
            print('* Multiprocessing')
            self.img_VARI = segm.computeMultiprocessVARI(self)
        else:
            self.img_VARI = segm.computeVARI(self)

        end_time = datetime.datetime.now()
        tot_time = end_time - start_time
        print("\tdescriptor multi: " + str(tot_time)[5:])
        start_time = end_time
        img = self.img_VARI

    else:
        print('* Grayscale image')
        import numpy
        img = numpy.array(self.img_Grayscale.convert("L"))




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

    end_time = datetime.datetime.now()
    tot_time = end_time - start_time
    print("\talgo: " + str(tot_time)[5:])
    start_time = end_time

    img_fname = self.getFileName()
    dest_fname = config.getConfigFilename()
    segm.writeProbabilityConfig(img_fname, dest_fname)

    return img_binary

def createGraph(graph_props):
    # convert lists into arrays
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

                if (centroids_arr[i][0][0] > centroids_arr[j][0][0]):
                    graph_props.G.add_node(i)
                    graph_props.G.add_node(j)
                    graph_props.G.add_edge(j,i,quality = 0)
                    angles_list[(j,i)] = angle
                    distances_list[(j,i)] = dist

                else:
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
    '''
        CALCULATE ANGLE
        of the segment defined by ab If b(x)<a(x): the segment ba is used
        Else: the segment ab is used

        :param a: node coord tuple (x, y)
        :param b: node coord tuple (x, y)
        :return: angle of the ab segment

    '''
    if (a[0] > b[0]):
        angle = np.abs(computeAngle(b, a))
    else:
        angle = np.abs(computeAngle(a, b))
    return angle

# -------------------------------------------------------------------------------
def computeAngle(a,b):
    '''
    Compute the angle of the segment defined by a and b
    :param a: node coord tuple (x, y)
    :param b: node coord tuple (x, y)
    :return: angle of the segment
    '''
    x = (b[0] - a[0])
    y = np.abs(b[1] - a[1])
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
def drawGraph(graph_props):
    '''
        DRAW LISTSUBGRAPH
        this function draws the subgraphs in the image
    '''

    pos_miss = graph_props.node_props.getCoordMissing()
    pos = graph_props.node_props.getCoordCentroids()
    rand_color = randomcolor.RandomColor()

    cont = 0

    for s in graph_props.subgraphs.values():
        color = rand_color.generate()
        nx.draw_networkx(s, pos=pos, with_labels = True, edgelist = s.edges(data = True),node_color = color, edgecolor = 'w',font_color='black',font_size = 10, node_size = 220)
        x = [int(i) for i in s.node()]
        pos_x = pos[x[len(x) - 1]][0] - 20
        pos_y = pos[x[len(x) - 1]][1]
        plt.text(pos_x, pos_y, str(cont), bbox={'facecolor':'w', 'alpha':0.5, 'pad':9})
        cont += 1

    for p in range(len(pos_miss)):
        # plt.text(pos_miss[p][0], pos_miss[p][1], str(-1), bbox={'facecolor':'r', 'alpha':0.7, 'pad':8})
        plt.plot(pos_miss[p][0],pos_miss[p][1],'maroon', marker="o",  markersize=25)

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
                plt.plot(xp,graph_props.subgraph_props.coef_curve[s](xp),'r-',linewidth=3.5)
                plt.text(x[0],y[0],str(graph_props.subgraph_props.error_curve[s]), bbox=dict(facecolor='white', alpha=0.5))
            else:
                plt.plot(xp,graph_props.subgraph_props.coef_curve[s](xp),color ="white",linestyle = '-',linewidth=3.5)
                plt.text(x[0],y[0],str(graph_props.subgraph_props.error_curve[s]), bbox=dict(facecolor='red', alpha=0.5))


# -------------------------------------------------------------------------------
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
            else:
                removeEdges(s[1],graph_props_2)

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

    for s in list(graph_props.subgraphs):
        H = graph_props.subgraphs[s]
        for e in list(H.edges()):
            if graph_props.getDistanceOfEdge(e) > 75:
                removeEdges(e,graph_props_2)

    return graph_props_2

# -------------------------------------------------------------------------------
def filterNodeExcentricty(graph_props):

    graph_props_2 = copy.deepcopy(graph_props)

    mean_ex = np.mean(list(graph_props.node_props.getExcentriciy().values()))
    std_ex = np.std(list(graph_props.node_props.getExcentriciy().values()))
    for s in list(graph_props.subgraphs):
        H = graph_props.subgraphs[s]
        for n in list(H.nodes()):
            if graph_props.getExcentriciy(n) < (mean_ex-2*std_ex):
                removeNodes(n,graph_props_2)

    return graph_props_2

# -------------------------------------------------------------------------------
def filterNodeDegree(graph_props):
    graph_props_2 = copy.deepcopy(graph_props)
    for n in list(graph_props.G.nodes()):
        if graph_props.G.degree(n) == 0:
            removeNodes(n,graph_props_2)
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
def filterSubgraph(graph_props):


    graph_props_0 = filterEdgesDistance(graph_props)
    graph_props_0.findSubgraphs()
    graph_props_1 = filterEdgesAngles(graph_props_0)
    graph_props_1.findSubgraphs()
    graph_props_2 = filterNodeExcentricty(graph_props_1)
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

def dividirSurco(grf,degree,error_max):

    grf2 = copy.deepcopy(grf)
    for s in grf.subgraphs:
        if grf.subgraph_props.error_curve[s] > error_max:
            H = grf.subgraphs[s]
            node_0 = []
            node_cons = []
            N = 4
            umb_err = 20
            for n in H.nodes():
                if H.degree(n) == 1:
                    node_0.append(n)

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
                x = [grf.getCoordCentroids(node_cons[n])[0] for n in range(N)]
                y = [grf.getCoordCentroids(node_cons[n])[1] for n in range(N)]
                z = np.polyfit(x,y, degree) # genera parametros de la curva
                p = np.poly1d(z) # función curva
                e = np.abs(np.polyval(z, x) - y)
                error = np.sum(e)/len(x)
                N += 1

            x2 = [grf.getCoordCentroids(n)[0] for n in H.nodes()]
            y2 = [grf.getCoordCentroids(n)[1] for n in H.nodes()]

        #     plt.figure()
        #     plt.axis('equal')
        #     plt.ylim(max(y),0)
        #     xp = np.linspace(min(x), max(x), len(x)+100)
        #     plt.plot(x2,y2,'.',xp,p(xp),'r-')
            removeNodes(node_cons[N],grf2)

        # plt.show()
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
def processImage():
    obj = Detection()
    obj.process()
    config.printObjInfoToLog(obj)
    return obj

# loops on the given folder (from settings)
def processFolder():
    # variables initialization
    obj_list = []
    index = 0

    source_dir = config.getSourceFolderName()
    listing = os.listdir(source_dir)
    for file in listing:
        for search_str in config.getSupportedFormats():
            if search_str in file or str.upper(search_str) in file:
                config.setImageFilename(file)
                obj_list.append(processImage())
                index = index + 1

    return obj_list

# runs the detection on the given file/folder
def run(file):
    if (os.path.isdir(file)):
        # if directory
        config.setSourceFolderName(file)
        proc_list = processFolder()
        config.printListInfoToLog(proc_list)
    else:
        # if file
        dir, filename = os.path.split(file)
        config.setSourceFolderName(dir)
        config.setImageFilename(filename)
        proc_img = processImage()

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

    def saveFigure(self,graph_props,nombre):
        fig, ax = plt.subplots(figsize=config.subplot_size)
        ax.imshow(config.arr_overlay)

        ax = self.drawRegions(graph_props, ax)
        drawGraph(graph_props)
        ax.set_axis_off()
        plt.tight_layout()
        plt.savefig(config.getLabelingPath(nombre))

    def filterRegionsByArea(self, arr_labeled, node_props, poly=None):
        centroids_arr = {}
        areas_arr = {}
        bboxes_arr = {}
        eccentricity = {}
        error_area = {}
        intensity = {}
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
                # draw rectangle around segmented areas
                rect = mpatches.Rectangle((bbox[i][0], bbox[i][1]), bbox[i][2]-bbox[i][0], bbox[i][3]-bbox[i][1],
                                       fill=False, edgecolor='w', linewidth=1)
                ax.add_patch(rect)

                # draw centroid over segmented areas
                centroid = mpatches.Circle( ((bbox[i][2]+bbox[i][0])/2, ((bbox[i][3]+bbox[i][1])/2)), 0.5, fill=False, edgecolor='yellow', linewidth=1)
                ax.add_patch(centroid)

        return ax


    # applies threshold, detects regions, calculates score

    def process(self):

        # SEGMENTATION #------------------------------

        start_time = datetime.datetime.now()

        print('\nProcessing:', config.getImageFilename())
        print("\tStarted at: " + str(start_time))

        # PHASE 2
        # # calculate distance min between trees
        # # # TODO: set area min
        # plt.imshow(self.img_RGB)
        # p = plt.ginput(-1)
        # # # # dist = calculateDistance(p[0],p[1])
        config.setDistanceThreshold(200)
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

        end_time = datetime.datetime.now()
        tot_time = end_time - start_time
        print("\tSegmentation: " + str(tot_time)[5:])
        start_time = end_time


        # POSTPROCESSING #------------------------------
        # PHASE 3
        # Binary closing
        arr_closed = closing(arr_binary, square(3))

        # configure size of subplots
        config.subplot_size = (arr_closed.shape[1]/100, arr_closed.shape[0]/100)

        if config.getDebugMode() == 2:
            # save closed binary image
            cls_binary = Image.fromarray(arr_closed)
            cls_binary.save(config.getClosingPath(self.img_file))
            # print(np.min(cls_binary))
            # print(np.max(cls_binary))

        end_time = datetime.datetime.now()
        tot_time = end_time - start_time
        print("\tPostprocessing: " + str(tot_time)[5:])
        start_time = end_time


        # PHASE 4
        # Labeling
        #arr_labeled = label(arr_cleared)graph_props.edge_props.edges
        # def axplot(arr_closed,arr_RGB):

        # convert image into array
        arr_RGB = array(self.img_RGB)
        plt.close('all')
        arr_labeled = label(arr_closed)
        config.arr_overlay = label2rgb(arr_labeled, image=arr_RGB, alpha=0.2)

        end_time = datetime.datetime.now()
        tot_time = end_time - start_time
        print("\tLabeling: " + str(tot_time)[5:])
        start_time = end_time

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

        end_time = datetime.datetime.now()
        tot_time = end_time - start_time
        print("\tCreation of initial graph/find subgraphs: " + str(tot_time)[5:])
        start_time = end_time

        #self.saveFigure(graph_props_v0,config.getImageFilename())

        # self.saveFigure(graph_props_v0,'prueba_00.jpg')
        # 2 - 1° filtered to the subgraph
        #   - Filter for distance
        #   - Filter for angles
        #   - Filter for nodes
        # ---------------------------------------------------------
        graph_props_v1 = filterSubgraph(graph_props_v0)
        graph_props_v1.findSubgraphs()
        # self.saveFigure(graph_props_v1, 'arboles_01.jpg')

        end_time = datetime.datetime.now()
        tot_time = end_time - start_time
        print("\tSubgraph filtering: distance, angle, eccentricity " + str(tot_time)[5:])
        start_time = end_time

        # graph_props_v2 = filterSubgraph(graph_props_v1)
        # graph_props_v2.findSubgraphs()
        # self.saveFigure(graph_props_v2, 'arboles_02.jpg')

        # # 3 - Set to the candidates of edges
        # #   - Search of candidates
        # #   - Add of setCandidatesOfEdges
        # #   - Draw of candidates
        # # ---------------------------------------------------------
        graph_props_v3 = setCandidatesOfEdges(graph_props_v1)
        graph_props_v3.addEdgesCandidates()
        graph_props_v3.findSubgraphs()

        end_time = datetime.datetime.now()
        tot_time = end_time - start_time
        print("\tEdge candidates " + str(tot_time)[5:])
        start_time = end_time

        # self.saveFigure(graph_props_v3,'arboles_03.jpg')

        # # 4 - Filter the nodes of degree == 0
        # # ---------------------------------------------------------
        graph_props_v4 = filterNodeDegree(graph_props_v3)
        graph_props_v4.findSubgraphs()
        # self.saveFigure(graph_props_v4,'arboles_04.jpg')

        end_time = datetime.datetime.now()
        tot_time = end_time - start_time
        print("\tNode filtering: degree " + str(tot_time)[5:])
        start_time = end_time

        # # 5 - Last filter of edges
        # # ---------------------------------------------------------
        for i in range(3):
            graph_props_vf = filterUltimasEdges(graph_props_v4)
        graph_props_vf = filterNodeDegree(graph_props_vf)
        graph_props_vf.findSubgraphs()

        end_time = datetime.datetime.now()
        tot_time = end_time - start_time
        print("\tUltimas edges " + str(tot_time)[5:])
        start_time = end_time

        AddNodes(graph_props_vf)

        grf2 = dividirSurco(graph_props_vf,2,20)
        grf2.findSubgraphs()


        # Compute curve of subgraphs
        if config.use_polynomial_regression:
            plotPolynomial(graph_props_vf)
            plotPolynomial(grf2)
            end_time = datetime.datetime.now()
            tot_time = end_time - start_time
            print("\tPolynomial regression: " + str(tot_time)[5:])
            start_time = end_time

        self.saveFigure(grf2,config.getImageFilename())



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
