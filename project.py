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
    plt.show()

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
            print node.GetId()

    ### Clustring coefficients
    print "clustering coeff",  snap.GetClustCf(network)


def GenRandomNet(reference):
    NNodes = reference.GetNodes()
    NEdge  = reference.GetEdges()

    Graph = snap.GenRndGnm(snap.PNGraph, NNodes, NEdge)
    return Graph

            
GetNetWorkStat(network, "Mexican Bank Network")
randnet = GenRandomNet(network)
GetNetWorkStat(randnet, "Reference Erdos-Renyi Network")
