import tsp
import random

#TODO implement crossover methods

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
        top_half = [p[1] for p in curr_gen[:int(n/2)]]
        next_gen = top_half[:]
        while len(next_gen) < pop_size:
            parentA = random.choice(top_half)
            parentB = random.choice(top_half)
            while parentA == parentB:
                parentA = random.choice(top_half)
                parentB = random.choice(top_half)
            first, second = partiallyMappedCrossover(parentA, parentB)
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
    print(curr_gen[0][1])
    assert tsp.is_good_perm(curr_gen[0][1])


# ---- partiallyMappedCrossover ---- 
 
def partiallyMappedCrossover(parentA ,parentB):
    assert tsp.is_good_perm(parentA)
    assert tsp.is_good_perm(parentB)
    assert len(parentA) == len(parentB)
    n = len(parentA)
    
    # Generate cut points for partitoning
    cutPoints = [random.randrange(1, n-1), random.randrange(1, n-1)]
    cutPoints = list(set(cutPoints))
    while len(cutPoints) == 1: 
        cutPoints = [random.randrange(1, n-1), random.randrange(1, n-1)]
        cutPoints = list(set(cutPoints))   
    cutPoints.sort()
    firstCutPoint = cutPoints[0]
    secondCutPoint = cutPoints[1]
    
    # Split the parents up to sublists 
    # - parent 1
    leftParentA, middleParentA, rightParentA = splitParent(parentA, firstCutPoint, secondCutPoint)
    
    # - parent 2
    leftParentB, middleParentB, rightParentB = splitParent(parentB, firstCutPoint, secondCutPoint)
    
    offspringA = makeOffspring(leftParentA, rightParentA, middleParentA, middleParentB)
    offspringB = makeOffspring(leftParentB, rightParentB, middleParentB, middleParentA)
    
    return offspringA, offspringB

def splitParent(parent, firstCutPoint, secondCutPoint):
    leftParition = parent[:firstCutPoint]
    middleParition = parent[firstCutPoint:secondCutPoint + 1]
    rightParition = parent[secondCutPoint + 1:]
    return leftParition, middleParition, rightParition

def getConflicts(leftParition, rightPartition, middlePartition):
    leftConflicts = list(set(leftParition) & set(middlePartition))
    rightConflicts = list(set(rightPartition) & set(middlePartition))
    conflicts = leftConflicts + rightConflicts  
    return conflicts  

def makeOffspring(leftParentX, rightParentX, middleParentX, middleParentY):
    
    conflicts = getConflicts(leftParentX, rightParentX, middleParentY)   
    for i in range(len(conflicts)):
        replacement = resolveConflict(conflicts[i], middleParentY, middleParentX) 
        if(conflicts[i] not in leftParentX):
            index = rightParentX.index(conflicts[i])
            rightParentX[index] = replacement
        else:
            index = leftParentX.index(conflicts[i])
            leftParentX[index] = replacement
            
    offspring = leftParentX + middleParentY + rightParentX
    return offspring
 
def resolveConflict(conflict, partitionA, partionB):
    isResolved = False
    possibleReplacement = conflict
    while not isResolved:
        possibleReplacement = partionB[partitionA.index(possibleReplacement)]
        isResolved = (possibleReplacement not in partitionA)
    return possibleReplacement
     
# ---- partiallyMappedCrossoverEnd ----     
def test():
    partiallyMappedTest("cities1000.txt", 100, 500)
    tsp.crossover_search("cities1000.txt", 100, 500)
        
test()
    
    