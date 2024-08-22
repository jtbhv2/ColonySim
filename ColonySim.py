import random
import logging
from collections import deque
import matplotlib.pyplot as plt

# Configuration
startingColonists = 100
startingFood = 100
maxGenerations = 100

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

class Colonist:
    def __init__(self, isNewborn=False):
        self.age = 0 if isNewborn else random.randint(1, 9)
        self.maxAge = random.randint(10, 14)
        self.foodProductionAttr = random.uniform(0.4, 2) # a range of 0.9 to 1.5 will yield exponential growth every time

    def foodProduction(self):
        return self.foodProductionAttr

class Population:
    def __init__(self, startingColonists):
        self.colonists = deque(Colonist() for _ in range(startingColonists))
        self.colonistsBorn = 0
        self.colonistsDiedOldAge = 0
        self.colonistsDiedStarvation = 0

    def getSize(self):
        return len(self.colonists)

    def handleAging(self):
        # Process aging and removal in a single pass
        for colonist in list(self.colonists):
            colonist.age += 1
            if colonist.age >= colonist.maxAge:
                self.colonists.remove(colonist)
                self.colonistsDiedOldAge += 1

    def calculateNewColonists(self):
        return int(self.getSize() * random.uniform(0.1, 0.2))

    def addColonists(self, newColonistsCount):
        for _ in range(newColonistsCount):
            colonist = Colonist(isNewborn=True)  # New colonists are born with age 0
            self.colonists.append(colonist)
        self.colonistsBorn += newColonistsCount

    def handleStarvation(self):
        foodNeeded = environment.food
        colonistsCount = self.getSize()
        if colonistsCount > foodNeeded:
            starvingCount = int(colonistsCount - foodNeeded)
            # Randomly select colonists to starve
            self.colonists = deque(random.sample(self.colonists, colonistsCount - starvingCount))
            self.colonistsDiedStarvation += starvingCount

    def removeColonistsDyingOfOldAge(self):
        self.colonists = deque(c for c in self.colonists if c.age < c.maxAge)

    def getEffectiveColonists(self):
        return [c for c in self.colonists if c.age > 1]

    def getAverageFoodProductionAttr(self):
        effectiveColonists = self.getEffectiveColonists()
        if not effectiveColonists:
            return 0
        return sum(c.foodProduction() for c in effectiveColonists) / len(effectiveColonists)

class Environment:
    def __init__(self, food):
        self.food = food
        self.foodGathered = 0
        self.foodConsumed = 0

    def handleFoodProduction(self):
        avgFoodProdAttr = population.getAverageFoodProductionAttr()
        producedFood = population.getSize() * avgFoodProdAttr
        self.foodGathered = producedFood
        self.food += producedFood

    def handleFoodConsumption(self, populationSize):
        consumedFood = min(self.food, populationSize)
        self.food -= consumedFood
        self.foodConsumed = consumedFood
        return consumedFood

    def ensureNonNegativeFood(self):
        if self.food < 0:
            self.food = 0

    def getSize(self):
        return startingColonists

def colonySim():
    global environment
    global population
    population = Population(startingColonists)
    environment = Environment(startingFood)
    generation = 0

    #i dont love these lists but they are necessary for the plotting
    generations = []
    colonistCounts = []
    foodCounts = []

    while generation < maxGenerations:
        generation += 1
        
        # Starting values for the generation
        startingColonistsThisGen = population.getSize()
        startingFoodThisGen = environment.food
        
        # 1. Age colonists
        population.handleAging()
        
        # 2. Food production
        environment.handleFoodProduction()
        
        # 3. Handle new colonists being born
        newColonistsCount = population.calculateNewColonists()
        population.addColonists(newColonistsCount)
        
        # 4. Food consumption
        consumedFood = environment.handleFoodConsumption(population.getSize())
        
        # 5. Handle negative food
        environment.ensureNonNegativeFood()
        
        # 6. Starvation
        population.handleStarvation()
        
        # 7. Remove colonists dying of old age
        population.removeColonistsDyingOfOldAge()
        
        # 8. Logging
        logging.info(
            f'Generation: {generation}\n'
            f'Starting Colonists: {startingColonistsThisGen}\n'
            f'Starting Food: {int(startingFoodThisGen)}\n'
            f'Food Gathered: {int(environment.foodGathered)}\n'
            f'Food Consumed: {int(consumedFood)}\n'
            f'Colonists Born: {population.colonistsBorn}\n'
            f'Colonists Starved: {population.colonistsDiedStarvation}\n'
            f'Colonists Died of Old Age: {population.colonistsDiedOldAge}\n'
            f'Final Colonist Count: {population.getSize()}\n'
            f'Final Food Count: {int(environment.food)}\n'
        )

        # this sucks man, idk if the plotting thing will stick around
        generations.append(generation)
        colonistCounts.append(population.getSize())
        foodCounts.append(environment.food)

        if population.getSize() == 0:
            logging.info('All colonists are dead.')
            break

    # i mean wtf is all this? i hate it and it may go bye bye
    plt.figure(figsize=(10, 6))
    plt.plot(generations, colonistCounts, label='Colonist Count', color='blue', marker='o')
    plt.plot(generations, foodCounts, label='Food Count', color='orange', marker='x')
    plt.xlabel('Generation')
    plt.ylabel('Count')
    plt.title('Colonist and Food Counts Over Generations')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Run simulation
colonySim()
