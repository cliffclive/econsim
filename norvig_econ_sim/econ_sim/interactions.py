'''
Created on Jan 22, 2014

@author: Peter Norvig
'''

import random


def anyone(pop): 
    return random.sample(range(len(pop)), 2)


def nearby(pop, k=5): 
    i = random.randrange(len(pop))
    j = i + random.choice((1, -1)) * random.randint(1, k)
    return i, (j % len(pop))

               
def nearby1(pop): 
    return nearby(pop, 1)