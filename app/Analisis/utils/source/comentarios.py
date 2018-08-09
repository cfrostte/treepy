


graph_props_2 = graph_props
tuplas_nodes = []

# Generate lista of nodes degree == 1 (candidate of edges)
for s in graph_props.subgraphs:
    H = graph_props.subgraphs[s]
    tuplas_nodes.append([n for n in H.nodes() if H.degree(n) == 1])

for t1 in range(len(tuplas_nodes)-1):
    print('t1:',t1)
    for t2 in range(t1 + 1,len(tuplas_nodes)):
        print('\tt2:',t2)
        for n1 in range(len(tuplas_nodes[t1])):
            print('\t\tn1:',n1)
            if len(tuplas_nodes[t2]) != 0:
                for n2 in range(len(tuplas_nodes[t2])):
                    print('\t\t\tn2:',n2)
                    dist = calculateDistance(graph_props.getCoordCentroids(tuplas_nodes[t1][n1]),graph_props.getCoordCentroids(tuplas_nodes[t2][n2]))
                    angle_edge_1 = graph_props.getAngleOfEdge(list(graph_props.G.edges(tuplas_nodes[t1][n1]))[0])
                    angle_edge_2 = graph_props.getAngleOfEdge(list(graph_props.G.edges(tuplas_nodes[t2][n2]))[0])
                    angle_edge_n = calculateAngle(graph_props.getCoordCentroids(tuplas_nodes[t1][n1]),graph_props.getCoordCentroids(tuplas_nodes[t2][n2]))
                    rest_1 = np.abs(angle_edge_1 - angle_edge_n)
                    rest_2 = np.abs(angle_edge_2 - angle_edge_n)

                    if (np.mean((rest_1,rest_2)) < graph_props.getMeanTwoAngles(t1)+ 3*graph_props.getStdTwoAngles(t1) or np.mean((rest_1,rest_2)) < graph_props.getMeanTwoAngles(t2) + 3*graph_props.getStdTwoAngles(t2)) and (dist < 4*graph_props.getMeanDistance(t2)):
                        # if (angle_edge_n > (graph_props.getMeanAngle(t1)-3.5*graph_props.getStdAngle(t1)) and angle_edge_n < (graph_props.getMeanAngle(t1)+3.5*graph_props.getStdAngle(t1))) or (angle_edge_n > (graph_props.getMeanAngle(t2)-3.5*graph_props.getStdAngle(t2)) and angle_edge_n < (graph_props.getMeanAngle(t2)+3.5*graph_props.getStdAngle(t2))):
                            graph_props_2.subgraphs_edge_candidates.append((tuplas_nodes[t1][n1], tuplas_nodes[t2][n2]))
                    # if ((angle_edge_n <= (graph_props.getMeanTwoAngles(t1) + 3*graph_props.getStdTwoAngles(t1)) and angle_edge_n <= (graph_props.getMeanTwoAngles(t2)+3*graph_props.getStdTwoAngles(t2))) and dist < 3*graph_props.getMeanDistance(t2) ):
                    #     graph_props_2.subgraphs_edge_candidates.append((tuplas_nodes[t1][n1], tuplas_nodes[t2][n2]))
                    #     print(tuplas_nodes[t1][n1],tuplas_nodes[t2][n2])
