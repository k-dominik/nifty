"""
Edge Contraction Graph
====================================


Contract the edges of an arbitrary graph
and call callbacks when edges and nodes
are merged
"""
from __future__ import print_function
import nifty
import nifty.graph
import pylab

def generateGrid(gridSize):
    def nid(x, y):
        return x*gridSize[1] + y
    G = nifty.graph.UndirectedGraph
    g =  G(gridSize[0] * gridSize[1])
    for x in range(gridSize[0]):
        for y in range(gridSize[1]):  

            u = nid(x,y)

            if x + 1 < gridSize[0]:

                v = nid(x+1, y)
                g.insertEdge(u, v)

            if y + 1 < gridSize[1]:

                v = nid(x, y+1)
                g.insertEdge(u, v)
    return g


class MyCallback(nifty.graph.EdgeContractionGraphCallback):
    def __init__(self):
        super(MyCallback, self).__init__()

    def contractEdge(self, edgeToContract):
        print("     contract edge",edgeToContract)

    def mergeEdges(self, aliveEdge, deadEdge):
        print("     merge edges",aliveEdge, deadEdge)

    def mergeNodes(self, aliveNode, deadNode):
        print("     merge nodes", aliveNode, deadNode)

    def contractEdgeDone(self, contractedEdge):
        print("     contract edge done", contractedEdge)


# generate grid graph
g   = generateGrid((3,2))

# the callback 
callback = MyCallback()

# the edge contraction graph
cg = nifty.graph.edgeContractionGraph(g,callback)



# plot the graph
pylab.figure()
pylab.title('graph')
nifty.graph.drawGraph(g)
pylab.show()

# - here we just contract all edges of the original graph
counter = 0
for e in g.edges():
        

    # get the endpoints of e in the original    
    u,v = g.uv(e)

    # get the nodes in the merged graph
    cu = cg.findRepresentativeNode(u)
    cv = cg.findRepresentativeNode(v)

    print("contraction graph:", cv)
    print("e",e,)   
    print("      u",u, "cv",v)
    print("     cu",cu," v",cv)

    if(cu != cv):
        # the edge is still alive 
        # since the endpoints are still in 
        # different clusters
        ce = cg.findRepresentativeEdge(e)

        # lets contract that edge
        cg.contractEdge(ce)

        # plot the graph
        pylab.figure()
        pylab.title('after contracting %d -- %d'%(cu, cv))
        nifty.graph.drawGraph(cg)
        counter += 1
        pylab.show()


    else:
        # the edge is not alive any more
        tmp = cg.nodeOfDeadEdge(e)
        assert tmp == cv