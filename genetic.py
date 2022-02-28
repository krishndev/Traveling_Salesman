import time
import numpy as np
    
# Calculating fitness values
def calculateFitness(nCities, cities_dis, cities, population):
    # List that saves all the distances
    distances = []

    newDistanceTravelled = 0
    for i in range(len(population)):
        newDistanceTravelled = 0
        # Calculating the distances for each order of cities
        for j in range(nCities-1):
            newDistanceTravelled += cities_dis[population[i][j]][cities.index(population[i][j+1])]
        newDistanceTravelled += cities_dis[population[i][nCities-1]][cities.index(population[i][0])]

        distances.append(newDistanceTravelled)
    
    # A list with all the fitness values for each of the orders of cities
    # Higher fitness value means it is a better result (better distance)
    fitness_values = []
    for distance in distances:
        value = 1/distance
        fitness_values.append(value)
    totalsum = sum(fitness_values)

    # Normalizing fitness values so that the sum will equal 1
    for value in range(len(fitness_values)):
        fitness_values[value] = fitness_values[value]/totalsum
    
    return distances, fitness_values

# Tournament based parent selection
def parentSelection(population, fitness_values, numPopulation):
    parents = []
    numParents = 0
    # 5 max
    maxParents = numPopulation/2

    while numParents < maxParents:
        randlist = []
        # Choosing 4 random candidates
        rand1 = np.random.randint(0, numPopulation-1)
        randlist.append(rand1)
        rand2 = np.random.randint(0, numPopulation-1)
        randlist.append(rand2)
        rand3 = np.random.randint(0, numPopulation-1)
        randlist.append(rand3)
        rand4 = np.random.randint(0, numPopulation-1)
        randlist.append(rand4)

        # Creating a list to compare fitness of the candidates
        randPopulationFitness = []
        for i in randlist:
            randPopulationFitness.append(fitness_values[i])
        
        # Finding the best candidate based on fitness, fittest candidate always wins this 'tournament'
        bestFitness = max(randPopulationFitness)

        # Finding the city order of the best candidate
        selectedParent = population[fitness_values.index(bestFitness)]

        # Adding it to the list of parents
        parents.append(selectedParent)
        
        numParents += 1
    
    return parents

# Crossover
def crossover(a, b, start, stop):
    child = [None]*len(a)
    
    # Copy a slice from first paret:
    child[start:stop] = a[start:stop]
    
    # Map the same slice in parent b to child using indices from parent a:
    for ind, x in enumerate(b[start:stop]):
        ind += start
        if x not in child:
            while child[ind] != None:
                ind = b.index(a[ind])
            child[ind] = x
    # Copy over the rest from parent b
    for ind, x in enumerate(child):
        if x == None:
            child[ind] = b[ind]
            
    return child

# Swap mutation
def mutate(offspring, nCities):
    for child in offspring:
        # Choose random cities
        city1 = np.random.randint(0, nCities)
        city2 = np.random.randint(0, nCities)
        # Swapping these cities
        get = child[city1], child[city2]
        child[city2], child[city1] = get
    return offspring

# Choose next generation
def nextGeneration(mutOffspring, population, fitness_values):
    newPop = []

    # Adding all mutated offspring to new population
    newPop = mutOffspring.copy()

    # Finding the best candidate based on fitness, fittest candidate always wins
    bestFitness = max(fitness_values)

    # Finding the city order of the best candidate
    elite = population[fitness_values.index(bestFitness)]
    newPop.append(elite)

    return newPop

# Main genetic method
def genetic(nCities, cities_dis, cities, numPopulation):
    start_time = time.time()
    globalOrder = cities.copy()

    # Our population that is composed of orders of cities
    population = []

    for i in range(numPopulation):
        # Creating a number of random city orders
        randomOrder = cities.copy()
        np.random.shuffle(randomOrder)
        population.append(randomOrder)
    #print(population)

    # A list that saves the best fitnesses for each generation
    listOfBestFitness = []

    for i in range(500):
        # -- Calculating the distances and fitness values for each of these orders
        distances, fitness_values = calculateFitness(nCities, cities_dis, cities, population)
        #print(distances)
        #print(fitness_values)
        #print(sum(fitness_values))

        # --select parents
        parents = parentSelection(population, fitness_values, numPopulation)
        #print(parents)

        # --recombining pairs of parents, creating offspring
        offspring = []
        for i in range(len(parents)-1):
            half = len(parents[i]) // 2
            start = np.random.randint(0, len(parents[i])-half)
            stop = start+half
            child1 = crossover(parents[i], parents[i+1], start, stop)
            child2 = crossover(parents[i+1], parents[i], start, stop)
            offspring.append(child1)
            offspring.append(child2)
    

        # --mutating the resulting offspring
        mutOffspring = mutate(offspring, nCities)

        # --evaluate the new candidates
        # --selecting individuals for the next generation
        newPopulation = nextGeneration(mutOffspring, population, fitness_values)

        # Saving the best fitness each generation. This is for later when plotting average fitness
        bestFitThisGen = max(fitness_values)
        bestFitThisGen = distances[fitness_values.index(bestFitThisGen)]
        listOfBestFitness.append(bestFitThisGen)
        
        # Updating next generation
        population = newPopulation.copy()
    
    #print(population)
    bestFitness = max(fitness_values)

    # Finding the city order of the best candidate
    selectedSolution = population[fitness_values.index(bestFitness)]
    bestDistance = distances[fitness_values.index(bestFitness)]

    print("--- %s seconds of runtime ---" % (time.time() - start_time))

    return selectedSolution, bestDistance, listOfBestFitness