import random
import logging

# Configuration
startingColonists = 100
startingFood = 1000
maxGenerations = 100

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

class Colonist:
    def __init__(self, isNewborn=False):
        if isNewborn:
            self.age = 0
        else:
            self.age = random.randint(1, 9)
        self.maxAge = random.randint(10, 14)
        self.foodProductionAttr = random.uniform(0.9, 1.5)

class Population:
    def __init__(self, startingColonists):
        self.colonists = [Colonist() for _ in range(startingColonists)]
        self.colonistsBorn = 0
        self.colonistsDiedOldAge = 0
        self.colonistsDiedStarvation = 0

    def getSize(self):
        return len(self.colonists)

    def handleAging(self):
        for colonist in self.colonists[:]:
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
        if self.getSize() > foodNeeded:
            starvingCount = int(self.getSize() - foodNeeded)
            self.colonists = self.colonists[:-starvingCount]
            self.colonistsDiedStarvation += starvingCount

    def removeColonistsDyingOfOldAge(self):
        self.colonists = [c for c in self.colonists if c.age < c.maxAge]

    def getEffectiveColonists(self):
        return [c for c in self.colonists if c.age > 1]

    def getAverageFoodProductionAttr(self):
        effectiveColonists = self.getEffectiveColonists()
        if not effectiveColonists:
            return 0
        return sum(c.foodProductionAttr for c in effectiveColonists) / len(effectiveColonists)

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
            f'Starting Colonists This Gen: {startingColonistsThisGen}\n'
            f'Starting Food This Gen: {int(startingFoodThisGen)}\n'
            f'Food Gathered This Gen: {int(environment.foodGathered)}\n'
            f'Food Consumed This Gen: {int(consumedFood)}\n'
            f'Colonists Born This Gen: {population.colonistsBorn}\n'
            f'Colonists Starved This Gen: {population.colonistsDiedStarvation}\n'
            f'Colonists Died of Old Age This Gen: {population.colonistsDiedOldAge}\n'
            f'Final Colonist Count This Gen: {population.getSize()}\n'
            f'Final Food Count This Gen: {int(environment.food)}\n'
        )

        if population.getSize() == 0:
            logging.info('All colonists are dead.')
            break

# Run simulation
colonySim()
