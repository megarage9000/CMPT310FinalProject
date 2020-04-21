import tsp
import sys


 # Vertex Class
 # - Has a unique ID
 # - Has a list of vertex ID's it is adjacent to
class Vertex():
    
    def __init__(self, key):
        self.adjacent = []
        self.numAdjacent = 0
        self.key = key
        
    def addAdjacent(self, neighbor):
        self.adjacent.append(neighbor)
        self.numAdjacent += 1
        
    def removeAdjacent(self, neighbor):
        self.adjacent.remove(neighbor)
        self.numAdjacent -= 1
        
    def hasAdjacentVertices(self):
        return (self.numAdjacent > 0)
    
    def hasAdjacentNeighbor(self, neighbor):
        return (neighbor in self.adjacent)

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
        
    def buildGraphFromCities(self, cities):
        cities = tsp.load_city_locs(cities)
        edges = []
        numCities = len(cities)
        for cityA in range(1, numCities + 1):
            self.addVertex(Vertex(cityA))
            for cityB in range(cityA + 1, numCities + 1):
                distance = tsp.city_dist(cityA, cityB, cities)
                edge = Edge(cityA, cityB, distance)
                edges.append(edge)
                
        edges.sort()
        numEdges = len(edges)
        currentEdgeIndex = 0
        
        while not self.hasEnoughEdges() and currentEdgeIndex < numEdges:
            self.addEdge(edges[currentEdgeIndex])
            currentEdgeIndex += 1
            
        self.numEdges = currentEdgeIndex
        
    def makePermuations(self, numPermuations, lowerBound=10, upperBound=50):
        permutations = []
        
        while len(permutations) < numPermuations:
            permutation = tsp.rand_perm(self.numVertices)
            score = self.measurePermToGraph(permutation)
            if score >= lowerBound and score <= upperBound:
                print("Added a permuation")
                permutations.append(permutation)
        
        return permutations
            
    def measurePermToGraph(self, permutation):
        score = 0
        permLength = len(permutation)
        for i in range(1, permLength + 1):
            for j in range(i + 1, permLength + 1):
                if(self.getVertex(i).hasAdjacentNeighbor(j)):
                    score += 1
                    
        score = int(score / self.numEdges) * 100
        return score
                
        
        
        
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
            
    def removeEdge(self, vertexA_ID, vertexB_ID):
        self.getVertex(vertexA_ID).removeAdjacent(vertexB_ID)
        self.getVertex(vertexB_ID).removeAdjacent(vertexA_ID)
          
    
    # - Used to build a kruskal tree
    #
    # def isCycleOnEdge(self, startingVertexID):
    #     visited = [[False] * 2 for i in range(self.numVertices)] 
    #     queue = [startingVertexID]
    #     visited[startingVertexID - 1][0] = True
        
    #     while(len(queue) > 0):
            
    #         vertexID = queue.pop(0)
    #         vertex = self.getVertex(vertexID)
            
    #         for childID in vertex.getAllAdjacent():
    #             if(visited[childID - 1][0] == True and visited[childID - 1][1] == True):
    #                 return True
    #             elif(visited[childID - 1][0] == True):
    #                 visited[childID - 1][1] = True
    #             else:
    #                 queue.append(childID)
    #                 visited[childID - 1][0] = True
        
    #     return False
    
    def hasEnoughEdges(self):
        for vertex in self.getAllVertices():
            if(vertex.hasAdjacentVertices() == False):
                return False
        return True
     
    def getAllVertices(self):
        return self.verticesDictionary.values()
    
    def printAllVertices(self):
        for vertex in self.getAllVertices():
            print(vertex.toString())

            
    
    
def test():    
    # bulding a kruskal tree
    graph = Graph()
    graph.buildGraphFromCities("cities1000.txt")
    print("Built graph! Generating permuations")
    permutations = graph.makePermuations(20)
    print("Done!")
    print(permutations)
test()