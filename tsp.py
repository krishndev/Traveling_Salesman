from exhaustive import exhaustive
from hillClimb import hillClimbing
from genetic import genetic

from itertools import permutations
from itertools import islice
import time
import numpy as np
import matplotlib.pyplot as plt
import statistics
import csv

def main():
    # Number of cities for the Traveling Salesman Problem
    nCities = 24
    # Creating lists and dictionaries that are needed to solve the problem
    cities_dis, cities, city_coords = defineCities(nCities)

    # Run exhaustive algorithm
    #runExhaustive(nCities, cities_dis, cities, city_coords)

    # Run hill climb (returns best of twenty runs)
    #runHillClimb(nCities, cities_dis, cities, city_coords)

    # Genetic Algorithm
    runGenetic(nCities, cities_dis, cities, city_coords)


# Creating lists and dictionaries that are needed to solve the problem
def defineCities(nCities):

    #Lists of city coordinates
    city_coords_all={"Barcelona":[2.154007, 41.390205], "Belgrade": [20.46,44.79], "Berlin": [13.40,52.52], "Brussels":[4.35,50.85],"Bucharest":[26.10,44.44], "Budapest": [19.04,47.50], "Copenhagen":[12.57,55.68], "Dublin":[-6.27,53.35], "Hamburg": [9.99, 53.55], "Istanbul": [28.98, 41.02], "Kiev": [30.52,50.45], "London": [-0.12,51.51], "Madrid": [-3.70,40.42], "Milan":[9.19,45.46], "Moscow": [37.62,55.75], "Munich": [11.58,48.14], "Paris":[2.35,48.86], "Prague":[14.42,50.07], "Rome": [12.50,41.90], "Saint Petersburg": [30.31,59.94], "Sofia":[23.32,42.70], "Stockholm": [18.06,60.33],"Vienna":[16.36,48.21],"Warsaw":[21.02,52.24]}
    
    # Getting necessary information from the file that contains all inforamation
    with open("european_cities.csv", "r") as f:
        # City coordinates
        city_coords = dict(islice(city_coords_all.items(), nCities))

        data = list(csv.reader(f, delimiter=';'))
        cities = data[0][:nCities]
        cities_dis = {}

    # A dictionary with cities and their distances to use
    for data_dis in range(len(cities)):
        cities_dis[cities[data_dis]] = [float(value) for value in data[data_dis+1][:nCities]]

    return cities_dis, cities, city_coords


# Plotting
def plot_plan(city_order, plotTitle, city_coords):
    #Map of Europe for plotting
    europe_map = plt.imread('map.png')

    fig, ax = plt.subplots(figsize=(10,10))
    ax.imshow(europe_map, extent=[-14.56,38.43, 37.697 +0.3 , 64.344 +2.0], aspect = "auto")
    plt.title(plotTitle)

    # Map (long, lat) to (x, y) for plotting
    for index in range(len(city_order) -1):
        current_city_coords = city_coords[city_order[index]]
        next_city_coords = city_coords[city_order[index+1]]
        x, y = current_city_coords[0], current_city_coords[1]
        #Plotting a line to the next city
        next_x, next_y = next_city_coords[0], next_city_coords[1]
        plt.plot([x,next_x], [y,next_y])
        
        plt.plot(x, y, 'ok', markersize=5)
        plt.text(x, y, index, fontsize=12);
    #Finally, plotting from last to first city
    first_city_coords = city_coords[city_order[0]]
    first_x, first_y = first_city_coords[0], first_city_coords[1]
    plt.plot([next_x,first_x],[next_y,first_y])
    #Plotting a marker and index for the final city
    plt.plot(next_x, next_y, 'ok', markersize=5)
    plt.text(next_x, next_y, index+1, fontsize=12);

    plt.show()

# ------- Code to run Exhaustive Algorithm and plotting it -------
def runExhaustive(nCities, cities_dis, cities, city_coords):
    print("Solving the Traveling Salesman Problem using different methods")
    # Running exhaustive algorithm
    theOrder, theDistance = exhaustive(nCities, cities_dis, cities, city_coords)
 
    print(theOrder)
    print(theDistance)
    plotTitle = "Testing Exhaustive Algorithm. Number of cities: ", str(nCities)
    # Plotting the plan found by the algorithm
    plot_plan(theOrder, plotTitle, city_coords)


# ------- Code to run Hill Climb and plotting it -------
def runHillClimb(nCities, cities_dis, cities, city_coords):
    distances = []
    allOrders = []
    
    for i in range(20):
        theOrder, theDistance = hillClimbing(nCities, cities_dis, cities)
        distances.append(theDistance)
        allOrders.append(theOrder)

        # This is just to check my code
        #print("Order Number ", i, ": ", theOrder)
        print("Order Number: ", i)
    
    maxDist = max(distances)
    minDist = min(distances)
    meanDist = float(sum(distances)/len(distances))
    stanDev = statistics.pstdev(distances)

    bestOrder = allOrders[distances.index(minDist)]
    
    # Maximum (worst) distance, Minimum (best) distance, Mean distance and Standard deviation
    print("Max: ", maxDist, "Min: ", minDist, "Mean: ", meanDist, "Standard Deviation: ", stanDev)
    print("Plotting minDist: ", bestOrder)

    # Plotting
    plotTitle = "20 runs of Genetic Algorithm. Number of cities: ", str(nCities)
    plot_plan(bestOrder, plotTitle, city_coords)


# ------- Code to run Genetic Algorithm and plotting it -------
def runGenetic(nCities, cities_dis, cities, city_coords):
    # Run twenty runs with different populations
    distancesTwenty = runTwentyGenetic(nCities, cities_dis, cities, city_coords, 20)
    distancesFifty = runTwentyGenetic(nCities, cities_dis, cities, city_coords, 50)
    distancesHundred = runTwentyGenetic(nCities, cities_dis, cities, city_coords, 100)

    # Plotting the average fitness through all the runs
    plt.plot(distancesTwenty, color='red', label=f"population of 20")
    plt.plot(distancesFifty, color='blue', label=f"population of 50")
    plt.plot(distancesHundred, color='green', label=f"population of 100")
    plt.legend()
    plt.title(f"Average fitness of the best fit individual")
    plt.grid()
    plt.show()


# 20 runs of genetic
def runTwentyGenetic(nCities, cities_dis, cities, city_coords, numPopulation):
    distances = []
    allOrders = []
    fitness = np.zeros(500)
    
    for i in range(20):
        #theOrder, theDistance = hillClimbing(cities, cities_dis)
        theOrder, theDistance, listOfBestFitness = genetic(nCities, cities_dis, cities, numPopulation)
        distances.append(theDistance)
        allOrders.append(theOrder)

        # Turn fitness list into an array to make it easier to calculate average afterwards
        fitness += np.array(listOfBestFitness)

        # This is just to check my code
        #print("Order Number ", i, ": ", theOrder)
        print("Order Number: ", i)
    
    maxDist = max(distances)
    minDist = min(distances)
    meanDist = float(sum(distances)/len(distances))
    stanDev = statistics.pstdev(distances)

    bestOrder = allOrders[distances.index(minDist)]
    
    # Maximum (worst) distance, Minimum (best) distance, Mean distance and Standard deviation
    print("Max: ", maxDist, "Min: ", minDist, "Mean: ", meanDist, "Standard Deviation: ", stanDev)
    print("Plotting minDist: ", bestOrder)

    # Plotting
    plotTitle = "20 runs of Genetic Algorithm. Number of cities: ", str(nCities), " Population of: ", str(numPopulation)
    plot_plan(bestOrder, plotTitle, city_coords)

    # Calculating average fitness
    average_fitness = fitness/20

    return average_fitness


if __name__ == "__main__":
    main()
