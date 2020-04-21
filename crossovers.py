import tsp
import random

#TODO implement crossover methods
#TODO implement boruvka/kruskal tree for initial population

# NOTE:
# - ALL CROSSOVER METHOD IDEAS CAME FROM THE CROSSOVERS OPERATORS FOR TSP PDF

def partiallyMappedTest(fname, max_iter, pop_size):
    city_locs = tsp.load_city_locs(fname)
    n = len(city_locs)
    # generate permutations for a specific population size
    curr_gen = [tsp.rand_perm(n) for i in range(pop_size)]
    # per population calculate total distance
    curr_gen = [(tsp.total_dist(p, city_locs), p) for p in curr_gen]
    curr_gen.sort()
    assert len(curr_gen) == pop_size
    
    
    print(f'partiallyMappedCrossover("{fname}", max_iter={max_iter}, pop_size={pop_size}) ...')
    for i in range(max_iter):
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
            first, second = partiallyMappedCrossover(parentA, parentB)
            tsp.do_rand_swap(first)
            tsp.do_rand_swap(second)
            next_gen.append(first)
            next_gen.append(second)

        next_gen = next_gen[:pop_size]

        # create the next generation of (score, permutations) pairs
        assert len(next_gen) == pop_size 
        curr_gen = [(tsp.total_dist(p, city_locs), p) for p in next_gen]
        curr_gen.sort()

    print(f'... partiallyMappedCrossover("{fname}", max_iter={max_iter}, pop_size={pop_size})')
    print()
    print(f'After {max_iter} generations of {pop_size} permutations, the best is:')
    print(f'score = {curr_gen[0][0]}')
    # print(curr_gen[0][1])
    assert tsp.is_good_perm(curr_gen[0][1])


# ---- partiallyMappedCrossover ---- 

def generateCrosspoints(size):
    cutPoints = [random.randrange(1, size - 1), random.randrange(1, size - 1)]
    cutPoints = list(set(cutPoints))
    while len(cutPoints) == 1: 
        cutPoints = [random.randrange(1, size - 1), random.randrange(1, size - 1)]
        cutPoints = list(set(cutPoints))   
    cutPoints.sort()
    return cutPoints[0], cutPoints[1]
 
def partiallyMappedCrossover(parentA ,parentB):
    assert tsp.is_good_perm(parentA)
    assert tsp.is_good_perm(parentB)
    assert len(parentA) == len(parentB)
    n = len(parentA)
    
    # Generate cut points for partitoning
    firstCutPoint, secondCutPoint = generateCrosspoints(n)
    
    # Split the parents up to sublists 
    # - parent 1
    leftParentA, middleParentA, rightParentA = splitParent(parentA, firstCutPoint, secondCutPoint)
    
    # - parent 2
    leftParentB, middleParentB, rightParentB = splitParent(parentB, firstCutPoint, secondCutPoint)
    # Make offspring
    offspringA = makeOffspringPartialMap(leftParentA, rightParentA, middleParentA, middleParentB)
    offspringB = makeOffspringPartialMap(leftParentB, rightParentB, middleParentB, middleParentA)
    
    return offspringA, offspringB

def splitParent(parent, firstCutPoint, secondCutPoint):
    leftParition = parent[:firstCutPoint]
    middleParition = parent[firstCutPoint:secondCutPoint + 1]
    rightParition = parent[secondCutPoint + 1:]
    return leftParition, middleParition, rightParition

def getConflictsPartialMap(leftParition, rightPartition, middlePartition):
    leftConflicts = list(set(leftParition) & set(middlePartition))
    rightConflicts = list(set(rightPartition) & set(middlePartition))
    conflicts = leftConflicts + rightConflicts  
    return conflicts  

def makeOffspringPartialMap(leftParentX, rightParentX, middleParentX, middleParentY):
    
    conflicts = getConflictsPartialMap(leftParentX, rightParentX, middleParentY)   
    for i in range(len(conflicts)):
        replacement = resolveConflictPartial(conflicts[i], middleParentY, middleParentX) 
        if(conflicts[i] not in leftParentX):
            index = rightParentX.index(conflicts[i])
            rightParentX[index] = replacement
        else:
            index = leftParentX.index(conflicts[i])
            leftParentX[index] = replacement
            
    offspring = leftParentX + middleParentY + rightParentX
    return offspring
 
def resolveConflictPartial(conflict, partitionA, partionB):
    isResolved = False
    possibleReplacement = conflict
    while not isResolved:
        possibleReplacement = partionB[partitionA.index(possibleReplacement)]
        isResolved = (possibleReplacement not in partitionA)
    return possibleReplacement
     
# ---- partiallyMappedCrossover End ----     

# ---- orderCrossover ----

def orderCrossoverTest(fname, max_iter, pop_size):
    city_locs = tsp.load_city_locs(fname)
    n = len(city_locs)
    # generate permutations for a specific population size
    curr_gen = [tsp.rand_perm(n) for i in range(pop_size)]
    # per population calculate total distance
    curr_gen = [(tsp.total_dist(p, city_locs), p) for p in curr_gen]
    curr_gen.sort()
    assert len(curr_gen) == pop_size
    
    print(f'orderCrossover("{fname}", max_iter={max_iter}, pop_size={pop_size}) ...')
    for i in range(max_iter):
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
            first, second = orderCrossover(parentA, parentB)
            tsp.do_rand_swap(first)
            tsp.do_rand_swap(second)
            
            next_gen.append(first)
            next_gen.append(second)

        next_gen = next_gen[:pop_size]

        # create the next generation of (score, permutations) pairs
        assert len(next_gen) == pop_size 
        curr_gen = [(tsp.total_dist(p, city_locs), p) for p in next_gen]
        curr_gen.sort()

    print(f'... orderCrossover("{fname}", max_iter={max_iter}, pop_size={pop_size})')
    print()
    print(f'After {max_iter} generations of {pop_size} permutations, the best is:')
    print(f'score = {curr_gen[0][0]}')
    # print(curr_gen[0][1])
    assert tsp.is_good_perm(curr_gen[0][1])

def orderCrossover(parentA, parentB):
    assert tsp.is_good_perm(parentA)
    assert tsp.is_good_perm(parentB)
    assert len(parentA) == len(parentB)
    n = len(parentA)
    
    firstCutPoint, secondCutPoint = generateCrosspoints(n)
    
    # Split the parents up to sublists 
    # - parent 1
    leftParentA, middleParentA, rightParentA = splitParent(parentA, firstCutPoint, secondCutPoint)
    # - parent 2
    leftParentB, middleParentB, rightParentB = splitParent(parentB, firstCutPoint, secondCutPoint)
    
    offspringA = makeOffSpringOrder(middleParentA, rightParentB + leftParentB + middleParentB, firstCutPoint)
    offspringB = makeOffSpringOrder(middleParentB, rightParentA + leftParentA + middleParentA, firstCutPoint)
    return offspringA, offspringB
    
def makeOffSpringOrder(middleParentA, sequenceBAfterCutPoint, firstCutPoint):
    conflicts = getConflictsOrder(middleParentA, sequenceBAfterCutPoint)
    for conflict in conflicts:
        sequenceBAfterCutPoint.remove(conflict)
        
    leftPartition = sequenceBAfterCutPoint[:firstCutPoint]
    rightPartition = sequenceBAfterCutPoint[firstCutPoint:]
    return leftPartition + middleParentA + rightPartition
    
    
def getConflictsOrder(middlePartition, otherPartition):
    return list(set(middlePartition) & set(otherPartition))

# ---- orderCrossover End ---- 

# def test():
#     partiallyMappedTest("cities1000.txt", 100, 50)
#     orderCrossoverTest("cities1000.txt", 100, 50)
#     tsp.crossover_search("cities1000.txt", 100, 50)
#     tsp.mutate_search("cities1000.txt", 100, 50)
#     tsp.rand_best("cities1000.txt", 100)
    
        
# test()
    
    