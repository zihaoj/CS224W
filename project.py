import snap
import numpy as np
import matplotlib.pyplot as plt

network = snap.LoadEdgeList(snap.PNGraph, "interbanking_Aug2017_anonimized.csv", 0, 1)

def GetNetWorkStat(network, networkname):
    print "Network Name", networkname
    print "Number of Nodes", network.GetNodes()
    print "Number of Edges", network.GetEdges()

    ### Getting Edge Distributions
    NEdges=[]
    for node in network.Nodes():
        NEdges.append( node.GetOutDeg()  )

    Y, X = np.histogram(NEdges, 50)#NEdges , np.max(NEdges)-np.min(NEdges))

    X= X[:-1]
    plt.bar(X, Y, color = 'r', label = networkname)
    plt.xlabel('Node Out Degree')
    plt.ylabel('Number of Nodes')
    plt.legend()
    plt.xlim ([0, 50])
    #plt.show()

    #### largest SCC, WCC
    MxScc = snap.GetMxScc(network)
    print "Size of largest SCC", MxScc.GetNodes()
    MxWcc = snap.GetMxWcc(network)
    print "Size of largest WCC", MxWcc.GetNodes()

    ### Find BFS Tree sizes
    bfsnodes = []
    for node in network.Nodes():
        forward = snap.GetBfsTree(network, node.GetId(), True, False)
        bfsnodes.append( forward.GetNodes()    )

        if forward.GetNodes() == 48:
            print "node high", node.GetId()
        if forward.GetNodes() == 1:
            print "node", node.GetId()
    print bfsnodes
    ### Clustring coefficients
    print "clustering coeff",  snap.GetClustCf(network)


    ### GetBetweeness
    
    betweenes =[]
    nid = []

    node_betweeness = snap.TIntFltH()
    edge_betweeness = snap.TIntPrFltH()
    snap.GetBetweennessCentr(network, node_betweeness, edge_betweeness, 1.0, True)
    for node in node_betweeness:
        nid.append(node)
        betweenes.append(node_betweeness[node])

    betweenes = np.array(betweenes)
    nid = np.array(nid)
    nid = nid[ np.argsort( betweenes)]
    betweenes = betweenes[ np.argsort( betweenes)]

    print nid
    print betweenes

    
    nid = []
    closeness = []
    
    ## GetCloseness
    for node in network.Nodes():
        nid.append(node.GetId())
        closeness.append( snap.GetClosenessCentr(network, node.GetId(), True, True))
        #print "closeness", node.GetId(), snap.GetClosenessCentr(network, node.GetId(), True, True)

    nid = np.array(nid)
    closeness = np.array(closeness)
    nid = nid[ np.argsort( closeness)]
    closeness = closeness[np.argsort(closeness)]

    print nid, closeness

    ecc = []
    nid = []
    ## Get Eccentricity
    for node in network.Nodes():

        nid.append(node.GetId())
        ecc.append(        snap.GetNodeEcc(network, node.GetId(), True))
        
    nid = np.array(nid)
    ecc = np.array(ecc)
    nid = nid[ np.argsort( ecc)]
    ecc = ecc[np.argsort(ecc)]

    print nid, ecc


    snap.DrawGViz(network, snap.gvlNeato, "vis.png", "Mexican Bank Network Visualization", True) 




def GenRandomNet(reference):
    NNodes = reference.GetNodes()
    NEdge  = reference.GetEdges()

    Graph = snap.GenRndGnm(snap.PNGraph, NNodes, NEdge)
    return Graph

            
GetNetWorkStat(network, "Mexican Bank Network")
#randnet = GenRandomNet(network)
#GetNetWorkStat(randnet, "Reference Erdos-Renyi Network")



