
import tsp

def helloWorld():
    print("random permutations: ")
    tsp.rand_best("cities1000.txt", 100)
    print("mutate search: ")
    tsp.mutate_search("cities1000.txt", 100, 500)
    print("crossover search: ")
    tsp.crossover_search("cities1000.txt", 100, 500)

helloWorld()
