import tsp
import crossovers



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
 
    
# Best edges search:
# - A crossover based breeding in which finds the top ~50 edges in both parents
# - and makes offspring by getting the best from one parent and filling it with the other
def bestEdgesSearch(parentA, parentB, cities):
    
    n = len(parentA)
    A = parentA[:]
    B = parentB[:]
    
    bestVerticesA = getBestEdgeVertices(A, cities)
    bestVerticesB = getBestEdgeVertices(B, cities)
    
    bestVerticesA = [-1 if x not in bestVerticesA else x for x in A]
    bestVerticesB = [-1 if x not in bestVerticesB else x for x in B]
    
    offSpringA = makePermBestEdges(bestVerticesA, B)
    offSpringB = makePermBestEdges(bestVerticesB, A)
    
    
    return offSpringA, offSpringB 
    
def getBestEdgeVertices(parent, cities):
    # 1. Get all edges
    edges = []
    permuationLength = len(parent)
    for i in range(0, permuationLength - 1):
        
        cityA = parent[i]
        cityB = parent[i + 1]
        distance = tsp.city_dist(cityA, cityB, cities)
        edges.append(Edge(cityA, cityB, distance))
    
    # 2. Get the top 50% edges            
    edges.sort()
    numEdges = len(edges)
    edges = edges[:int(numEdges/2) - 1]
    
    # 3. Get all involving vertices
    vertices = []
    for edge in edges:
        edgeVertices = edge.getVertices()
        vertices.append(edgeVertices[0])
        vertices.append(edgeVertices[1])
        
    bestVertices = []
    [bestVertices.append(x) for x in vertices if x not in bestVertices]
    return bestVertices
        
    
def makePermBestEdges(bestVertices, otherPermuation):
    otherPermNoConflicts = [item for item in otherPermuation if item not in bestVertices]
    newPerm = bestVertices[:]
    i = 0
    n = len(newPerm)
    for j in range(n):
        if newPerm[j] == -1:
            newPerm[j] = otherPermNoConflicts[i]
            i += 1
    return newPerm
    


def test2():
    cities = tsp.load_city_locs("cities1000.txt")
    permutationA = tsp.rand_perm(1000)
    permutationB = tsp.rand_perm(1000)
    print("permutationA Distance: ", tsp.total_dist(permutationA, cities))
    print("permutationB Distance: ", tsp.total_dist(permutationB, cities))
    offSpringA, offSpringB = bestEdgesSearch(permutationA, permutationB, cities)
    print("offSpringA bestEdge Distance: ", tsp.total_dist(offSpringA, cities))
    print("offSpringB bestEdge Distance: ", tsp.total_dist(offSpringB, cities))
    
    offSpringA, offSpringB = crossovers.partiallyMappedCrossover(permutationA, permutationB)
    print("offSpringA partiallyMapped Distance: ", tsp.total_dist(offSpringA, cities))
    print("offSpringB partiallyMapped Distance: ", tsp.total_dist(offSpringB, cities))
    
    offSpringA, offSpringB = crossovers.orderCrossover(permutationA, permutationB)
    print("offSpringA order Distance: ", tsp.total_dist(offSpringA, cities))
    print("offSpringB order Distance: ", tsp.total_dist(offSpringB, cities))
    
    

test2()