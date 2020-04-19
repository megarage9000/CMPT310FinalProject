import tsp
import random

#TODO implement crossover methods

def partiallMappedTest(fname, max_itr, pop_size):
    city_locs = tsp.load_city_locs(fname)
    n = len(city_locs)
    # generate permutations for a specific population size
    curr_gen = [tsp.rand_perm(n) for i in range(pop_size)]
    # per population calculate total distance
    curr_gen = [(tsp.total_dist(p, city_locs), p) for p in curr_gen]
    curr_gen.sort()
    assert len(curr_gen) == pop_size

 
 
def partiallyMappedCrossover(parent1 ,parent2):
    assert tsp.is_good_perm(parent1)
    assert tsp.is_good_perm(parent2)
    assert len(parent1) == len(parent2)
    n = len(parent1)
    
    print("Parent 1 before partitioning: ", parent1)
    print("Parent 2 before partitioning: ", parent2)
    # Generate cut points for partitoning
    cutPoints = [random.randrange(1, n-1), random.randrange(1, n-1)]
    cutPoints.sort()
    print("Indexes of cut points: ", cutPoints)
    firstCutPoint = cutPoints[0]
    secondCutPoint = cutPoints[1]
    
    # Split the parents up to sublists
    
    # - parent 1
    leftParent1 = parent1[:firstCutPoint]
    middleParent1 = parent1[firstCutPoint:secondCutPoint + 1]
    rightParent1 = parent1[secondCutPoint + 1: ]
    print("Parent 1 after parition: {",leftParent1, "}, {",middleParent1,"}, {",rightParent1,"}")
    
    # - parent 2
    leftParent2 = parent2[:firstCutPoint]
    middleParent2 = parent2[firstCutPoint:secondCutPoint + 1]
    rightParent2 = parent2[secondCutPoint + 1: ]
    print("Parent 2 after parition: {",leftParent2, "}, {",middleParent2,"}, {",rightParent2,"}")
    
def test():
    cities = tsp.load_city_locs("cities10.txt")
    n = len(cities)
    perm1 = tsp.rand_perm(n)
    perm2 = tsp.rand_perm(n)
    partiallyMappedCrossover(perm1, perm2)
    
test()
    
    