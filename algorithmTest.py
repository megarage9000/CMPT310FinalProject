import tsp

#TODO implement Boruvka's algorithm?
# - Make an algorithm/class to construct a minimum spanning tree given the cities
# - Source: https://www.geeksforgeeks.org/boruvkas-algorithm-greedy-algo-9/


    
class Vertex():
    
    def __init__(self, key):
        self.adjacent = {}
        self.key = key
        
    def addAdjacent(self, neighbor, weight):
        self.adjacent[neighbor] = weight
        
    def removeAdjacent(self, neighbor):
        try:
            del self.adjacent[neighbor]
        except KeyError:
            pass
        
    def getWeightToNeighbor(self, neighbor):
        value = self.adjacent.get(neighbor)
        assert value != None
        return value
    
    def getID(self):
        return self.key
    
    def getAllAdjacent(self):
        return self.adjacent.values()
    
    def toString(self):
        return "Vertex: " + str(self.key) + ", adjacent to " + str(self.adjacent.values())
    
class Edge():
    
    def __init__(self, vertexA_ID, vertexB_ID, weight):
        self.vertices = [vertexA_ID, vertexB_ID]
        self.vertices.sort()
        self.weight = weight
        
    def getVertices(self):
        return self.vertices
            
    def getWeight(self):
        return self.weight
    
    def toString(self):
        return "Vertices in this edge: " + str(self.vertices) + ", weight: " + str(self.weight)
    
    # From this stack overflow: https://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes
    def __lt__(self, other):
        return self.weight < other.weight
    def __le__(self, other):
        return self.weight <= other.weight
    def __eq__(self, other):
        return sorted(self.vertices) == sorted(other.vertices)
    def __ne__(self, other):
        return sorted(self.vertices) != sorted(other.vertices)
    def __gt__(self, other):
        return self.weight > other.weight
    def __ge__(self, other):
        return self.weight >= other.weight
    
class Graph():
    
    def __init__(self):
        self.verticesDictionary = {}
        self.numVertices = 0
        self.numEdges = 0
        
    def getVertex(self, key):
        vertex = self.verticesDictionary.get(key)
        assert vertex != None
        return vertex
    
    def addVertex(self, vertex):
        key = vertex.getID()
        if(self.verticesDictionary.get(key) == None): 
            self.verticesDictionary[key] = vertex
            self.numVertices += 1
        
    def addEdge(self, vertexA, vertexB, weight):
        self.getVertex(vertexA.getID()).addAdjacent(vertexB, weight)
        self.getVertex(vertexB.getID()).addAdjacent(vertexA, weight)   
        if self.isCycleOnEdgeAdd(vertexA.getID()):
            self.deleteEdge(vertexA, vertexB)
        
    def deleteEdge(self, vertexA, vertexB):
        self.getVertex(vertexA.getID()).removeAdjacent(vertexB)
        self.getVertex(vertexB.getID()).removeAdjacent(vertexB)
        
    def addEdgeFromEdge(self, Edge):
        vertices = Edge.getVertices()
        weight = Edge.getWeight()
        vertexA = self.getVertex(vertices[0])
        vertexB = self.getVertex(vertices[1])
        self.addEdge(vertexA, vertexB, weight)
        
        
    def getAllVertices(self):
        return self.verticesDictionary.values()


    # Cycles here are ones consisting with > 3 edges    
    def isCycle(self, parent, parentOfParent):
        for child in parent.getAllAdjacent:
            if(child != parent):
                if(child == parentOfParent or self.isCycle(child, parent)):
                    return True
        return False

    def isCycleOnEdgeAdd(self, vertexID):
        startingVertex = self.getVertex(vertexID)
        children = startingVertex.getAllAdjacent()
        for child in children:
            if(self.isCycle(child, startingVertex)):
                return True
        return False

def test():    
    # bulding a kruskal tree
    cities = tsp.load_city_locs("cities10.txt")
    graph = Graph()
    edges = []
    for cityA in range(1, len(cities) + 1):
        vertex = Vertex(cityA)
        graph.addVertex(vertex)
        for cityB in range(cityA + 1, len(cities) + 1):
            distance = tsp.city_dist(cityA, cityB, cities)
            edge = Edge(cityA, cityB, distance)
            edges.append(edge)
            
    edges.sort()
    for vertex in graph.getAllVertices():
        print(vertex.toString())
             
    for edge in edges:
        # graph.addEdgeFromEdge(edge)
        print(edge.toString())
        
    
    
    print("hello")      
  
test()