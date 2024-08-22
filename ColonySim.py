#right now, let's just get something going. literally anything idc

import random



def main():
    colonists = 100
    food = 1000
    generation = 0
    while generation <=100:
        generation += 1
        food += colonists * 1.1
        colonists = colonists*random.randint(1,3)
        food -= colonists
        if food < colonists:
            colonists = food
        if food <= 0:
            food = 0
        if colonists <= 0:
            print('All colonists are dead.')
            generation = 101
        print(f'Generation {generation}: Food: {food}, Colonists: {colonists}')


main()
