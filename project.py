
import tsp

def helloWorld():
    print("random permutations: ")
    tsp.rand_best("cities10.txt", 100)
    print("mutate search: ")
    tsp.mutate_search("cities10.txt", 100, 4)
    print("crossover search: ")
    tsp.crossover_search("cities10.txt", 100, 4)

helloWorld()
