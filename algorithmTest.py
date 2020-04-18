import tsp

#TODO implement Boruvka's algorithm?
# - Make an algorithm/class to construct a minimum spanning tree given the cities
# - Source: https://www.geeksforgeeks.org/boruvkas-algorithm-greedy-algo-9/


class BoruvkaTree():
    
    def __init__(self, fname):
        self.cities = tsp.load_city_locs(fname)
        self.tree = []
        self.buildBoruvkaTree()
        
        
    def findClosestNeigbour(self, city):
        return -1
    
    def buildBoruvkaTree(self):
        print("hello!")
        return -1
    
def test():
    tree = BoruvkaTree("cities10.txt")
    
test()