import tsp
import random
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
    
    # Retrieve best vertices from best edges
    bestVerticesA = getBestEdgeVertices(A, cities)
    bestVerticesB = getBestEdgeVertices(B, cities)
    
    # Marking vertices that aren't in best edges as -1
    bestVerticesA = [-1 if x not in bestVerticesA else x for x in A]
    bestVerticesB = [-1 if x not in bestVerticesB else x for x in B]
    
    # Making offspring
    offSpringA = makePermBestEdges(bestVerticesA, B)
    offSpringB = makePermBestEdges(bestVerticesB, A)
    
    assert tsp.is_good_perm(offSpringA)
    assert tsp.is_good_perm(offSpringB)
    
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
        
# Make complete permuations from other parent 
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
    
# Unoptimized bestEdges GA
def bestEdges(fname, max_iter, pop_size):
    city_locs = tsp.load_city_locs(fname)
    n = len(city_locs)
    # generate permutations for a specific population size
    curr_gen = [tsp.rand_perm(n) for i in range(pop_size)]
    # per population calculate total distance
    curr_gen = [(tsp.total_dist(p, city_locs), p) for p in curr_gen]
    curr_gen.sort()
    assert len(curr_gen) == pop_size
    
    
    print(f'bestEdges("{fname}", max_iter={max_iter}, pop_size={pop_size}) ...')
    for i in range(max_iter):
        print("iteration: ", i)
        # copy the top 50% of the population to the next generation, and for the rest randomly 
        # cross-breed pairs
        top_half = [p[1] for p in curr_gen[:int(pop_size/2)]]
        next_gen = top_half[:]
        while len(next_gen) < pop_size:
            parentA = random.choice(top_half)
            parentB = random.choice(top_half)
            while parentA == parentB:
                parentA = random.choice(top_half)
                parentB = random.choice(top_half)
            first, second = bestEdgesSearch(parentA, parentB, city_locs)
            tsp.do_rand_swap(first)
            tsp.do_rand_swap(second)
            
            next_gen.append(first)
            next_gen.append(second)

        next_gen = next_gen[:pop_size]

        # create the next generation of (score, permutations) pairs
        assert len(next_gen) == pop_size 
        curr_gen = [(tsp.total_dist(p, city_locs), p) for p in next_gen]
        curr_gen.sort()

    print(f'... bestEdges("{fname}", max_iter={max_iter}, pop_size={pop_size})')
    print()
    print(f'After {max_iter} generations of {pop_size} permutations, the best is:')
    print(f'score = {curr_gen[0][0]}')
    # print(curr_gen[0][1])
    assert tsp.is_good_perm(curr_gen[0][1])
    
def optimizedBestSearch(fname, max_iter=100, pop_size=50, percentToSwitch=5):
    city_locs = tsp.load_city_locs(fname)
    n = len(city_locs)
    curr_gen = [tsp.rand_perm(n) for i in range(pop_size)]
    curr_gen = [(tsp.total_dist(p, city_locs), p) for p in curr_gen]
    curr_gen.sort()
    
    bestScore = curr_gen[0][0]
    bestPermuation = curr_gen[0][1]
    useMutateSearch = False
    
    print(f'Optimized bestEdges("{fname}", max_iter={max_iter}, pop_size={pop_size}) ...')
    for i in range(max_iter):
        print("iteration: ", i)
        top_half = [p[1] for p in curr_gen[:int(pop_size/2)]]
        next_gen = top_half[:]
        while len(next_gen) < pop_size:
            parentA = random.choice(top_half)
            parentB = random.choice(top_half)
            while parentA == parentB:
                parentA = random.choice(top_half)
                parentB = random.choice(top_half)
            if(useMutateSearch):
                first = parentA[:]
                second = parentB[:]  
            else:   
                first, second = bestEdgesSearch(parentA, parentB, city_locs)
                
            tsp.do_rand_swap(first)
            tsp.do_rand_swap(second)
            next_gen.append(first)
            next_gen.append(second)

        next_gen = next_gen[:pop_size]
        assert len(next_gen) == pop_size 
        curr_gen = [(tsp.total_dist(p, city_locs), p) for p in next_gen]
        curr_gen.sort()
        
        useMutateSearch = ifSwitchToMutate(bestScore, curr_gen[0][0], percentToSwitch)
        
        if(curr_gen[0][0] < bestScore):
            bestScore = curr_gen[0][0]
            bestPermuation = curr_gen[0][1]
        
        
    print(f'... Optimized bestEdges("{fname}", max_iter={max_iter}, pop_size={pop_size})')
    print()
    print(f'After {max_iter} generations of {pop_size} permutations, the best is:')
    print(f'score = {bestScore}')
    print(bestPermuation)
    assert tsp.is_good_perm(bestPermuation)

def calculateImprovement(oldScore, newScore):
    percent = float((newScore/oldScore) * 100)
    return 100 - percent 

def ifSwitchToMutate(oldScore, newScore, percentToSwitch):
    improvement = calculateImprovement(oldScore, newScore)
    print("Improvement: ", improvement)
    if(improvement <= percentToSwitch and improvement != 0):
        return True
    else:
        return False
    
def compareCrossovers():
    cities = tsp.load_city_locs("cities1000.txt")
    permutationA = tsp.rand_perm(1000)   
    permutationB = tsp.rand_perm(1000)
    
    print("Original A: ", tsp.total_dist(permutationA, cities))
    print("Original B: ", tsp.total_dist(permutationB, cities))
    
    # Order Crossover
    offSpringA, offSpringB = crossovers.orderCrossover(permutationA, permutationB)
    print("OffspringB Order: ", tsp.total_dist(offSpringA, cities))
    print("OffspringB Order: ", tsp.total_dist(offSpringB, cities))
    
    # Partially Mapped Crossover
    offSpringA, offSpringB = crossovers.partiallyMappedCrossover(permutationA, permutationB)
    print("OffspringB Partially Mapped: ", tsp.total_dist(offSpringA, cities))
    print("OffspringB Partially Mapped: ", tsp.total_dist(offSpringB, cities))
    
    # Best Edges Crossover
    offSpringA, offSpringB = bestEdgesSearch(permutationA, permutationB, cities)
    print("OffspringB Best Edges: ", tsp.total_dist(offSpringA, cities))
    print("OffspringB Best Edges: ", tsp.total_dist(offSpringB, cities))
