import tsp
import sys

#TODO make vertex store IDs of vertices instead



 # Vertex Class
 # - Has a unique ID
 # - Has a list of vertex ID's it is adjacent to
class Vertex():
    
    def __init__(self, key):
        self.adjacent = []
        self.key = key
        
    def addAdjacent(self, neighbor):
        self.adjacent.append(neighbor)
        
    def removeAdjacent(self, neighbor):
        self.adjacent.remove(neighbor)

    def getID(self):
        return self.key
    
    def getAllAdjacent(self):
        return self.adjacent
    
    def toString(self):
        return "Vertex: " + str(self.key) + ", adjacent to " + str(self.adjacent)

    
class Edge():
    
    def __init__(self, vertexA_ID, vertexB_ID, weight):
        self.vertices = (vertexA_ID, vertexB_ID)
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
        
    def addEdge(self, Edge):
        verticesID = Edge.getVertices()
        vertexA_ID = verticesID[0]
        vertexB_ID = verticesID[1]
        self.getVertex(vertexA_ID).addAdjacent(vertexB_ID)
        self.getVertex(vertexB_ID).addAdjacent(vertexA_ID)
        if(self.isCycleOnEdge(vertexA_ID)):
            self.removeEdge(vertexA_ID, vertexB_ID)
            
    def removeEdge(self, vertexA_ID, vertexB_ID):
        self.getVertex(vertexA_ID).removeAdjacent(vertexB_ID)
        self.getVertex(vertexB_ID).removeAdjacent(vertexA_ID)
          
    # Using BFS to search for cycle
    # https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
    def isCycleOnEdge(self, startingVertexID):
        
        visited = [False] * len(self.getAllVertices())    
        queue = [startingVertexID]
        visited[startingVertexID] = True
        
        while len(queue) > 0:       
            vertexID = queue.pop()
            vertex = self.getVertex(vertexID)
            
            for childID in vertex.getAllAdjacent():
                if visited[childID] == False:
                    queue.append(childID)
                    visited[childID] == True
            
                             
        
            
    def getAllVertices(self):
        return self.verticesDictionary.values()
    
    def printAllVertices(self):
        for vertex in self.getAllVertices():
            print(vertex.toString())

            
    
    
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
    
             
    for edge in edges:
       graph.addEdge(edge)
       # print(edge.toString())
       
    for vertex in graph.getAllVertices():
        print(vertex.toString())

    
  
test()