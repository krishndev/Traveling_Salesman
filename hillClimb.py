import time
import numpy as np

# ------ HILL CLIMBING ------
def hillClimbing(nCities, cities_dis, cities):
    start_time = time.time()

    new_cityOrder = cities.copy()
    np.random.shuffle(new_cityOrder)

    first = False 
    for i in range(1000):
        newDistanceTravelled = 0

        # Save first instance as possible best
        if first == False:
            for j in range(nCities-1):
                newDistanceTravelled += cities_dis[new_cityOrder[j]][cities.index(new_cityOrder[j+1])]
            newDistanceTravelled += cities_dis[new_cityOrder[nCities-1]][cities.index(new_cityOrder[0])]
            distanceTravelled = newDistanceTravelled
            cities = new_cityOrder
            first = True

        # Two random cities
        city1 = np.random.randint(0, nCities)
        city2 = np.random.randint(0, nCities)

        if city1 != city2:
            # Reorder the set of cities
            possibleCityOrder = new_cityOrder.copy() 
            #print(possibleCityOrder)

            # Swap cities
            get = possibleCityOrder[city1], possibleCityOrder[city2]
            possibleCityOrder[city2], possibleCityOrder[city1] = get
            #print(possibleCityOrder)

            #print(possibleCityOrder)
            # Work out the new distances
            newDistanceTravelled = 0
            for j in range(nCities-1):
                newDistanceTravelled += cities_dis[possibleCityOrder[j]][cities.index(possibleCityOrder[j+1])]
            newDistanceTravelled += cities_dis[possibleCityOrder[nCities-1]][cities.index(possibleCityOrder[0])]
            if newDistanceTravelled < distanceTravelled:
                distanceTravelled = newDistanceTravelled
                cities = possibleCityOrder.copy()

    print("--- %s seconds of runtime ---" % (time.time() - start_time))

    return cities, distanceTravelled