
import tsp

def helloWorld():
    print("hello World")
    print("Help me!")
    result = tsp.load_city_locs("cities1000.txt")
    for city in result:
        print(city)
    
helloWorld()
