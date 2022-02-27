from itertools import permutations
import time

# ------ EXHAUSTIVE SEARCH ------
def exhaustive(nCities, cities_dis, cities, city_coords):
    # Calculate time
    start_time = time.time()
    #print(cities_dis) 
    first_permutation = False
    for newOrder in permutations(city_coords):
        possibleDistanceTravelled = 0
        
        for i in range(nCities-1):
            possibleDistanceTravelled += cities_dis[newOrder[i]][cities.index(newOrder[i+1])]
        possibleDistanceTravelled += cities_dis[newOrder[nCities-1]][cities.index(newOrder[0])]

        # First permutation is saved as possible best for the first instance
        if first_permutation == False: 
            distanceTravelled = possibleDistanceTravelled
            first_permutation = True

        # Checking the others
        if possibleDistanceTravelled < distanceTravelled:
            distanceTravelled = possibleDistanceTravelled
            cityOrder = newOrder
    print("--- %s seconds of runtime ---" % (time.time() - start_time))

    return cityOrder, distanceTravelled


