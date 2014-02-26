'''
Created on Jan 22, 2014

@author: Peter Norvig, Cliff Clive
'''

import random
import math


def random_split(X, Y):
    "Take all the money in the pot and divide it randomly between X and Y."
    pot = X + Y
    m = random.uniform(0, pot)
    return m, pot - m


def winner_take_most(X, Y, most=3/4.): 
    "Give most of the money in the pot to one of the parties."
    pot = X + Y
    m = random.choice((most * pot, (1 - most) * pot))
    return m, pot - m


def winner_take_all(X, Y): 
    "Give all the money in the pot to one of the actors."
    return winner_take_most(X, Y, 1.0)


def redistribute(X, Y): 
    "Give 55% of the pot to the winner; 45% to the loser."
    return winner_take_most(X, Y, 0.55)


def split_half_min(X, Y):
    """The poorer actor only wants to risk half his wealth; 
    the other actor matches this; then we randomly split the pot."""
    pot = min(X, Y)
    m = random.uniform(0, pot)
    return X - pot/2. + m, Y + pot/2. - m


def cobb_douglas_competitive_eqbm(X, Y):
    # Useful constants for the following calculations
    alphaX = X.pref1 / (X.pref1 + X.pref2)
    betaX  = X.pref2 / (X.pref1 + X.pref2)
    alphaY = Y.pref1 / (Y.pref1 + Y.pref2)
    betaY  = Y.pref2 / (Y.pref1 + Y.pref2)
    total_1 = X.good1 + Y.good1
    total_2 = X.good2 + Y.good2
    
    # Equilibrium price of good 1 relative to good 2
    price = (X.good2 * alphaX + Y.good2 * alphaY) / (X.good1 * betaX + Y.good1 * betaY)

    allocation_x = X.demand(price)
    allocation_y = (total_1 - allocation_x[0], total_2 - allocation_x[1])

    return (allocation_x, allocation_y, price)


def cobb_douglas_negotiation(agentX, agentY):
    # Find the total amounts of each good:
    total_1 = agentX.good1 + agentY.good1
    total_2 = agentX.good2 + agentY.good2

    # Each agent will accept no less of good1 than the amount
    # where the contract curve intersects their starting
    # indifference curve
    min_good1_x = math.sqrt(agentX.good1 * agentX.good2 * total_1 / total_2)
    min_good1_y = math.sqrt(agentY.good1 * agentY.good2 * total_1 / total_2)
    max_good1_x = total_1 - min_good1_y

    # Bargaining power of an agent is that agent's share of the
    # sum of the two agents' charisma scores.
    bargaining_power_x = agentX.charisma / (agentX.charisma + agentY.charisma)

    # The amount of good1 up for negotiation is max_good1_x - min_good1_x.
    # Each agent's bargaining power determines what share they will get.
    allocation_x1 = min_good1_x + bargaining_power_x * (max_good1_x - min_good1_x)
    allocation_y1 = total_1 - allocation_x1
    allocation_x2 = (total_2 / total_1) * allocation_x1
    allocation_y2 = total_2 - allocation_x2

    return (allocation_x1, allocation_x2), (allocation_y1, allocation_y2)


