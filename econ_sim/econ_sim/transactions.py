'''
Created on Jan 22, 2014

@author: Peter Norvig, Cliff Clive
'''

import random


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


def edgeworth_trade(X, Y):
    # Useful constants for the following calculations
    alphaX = X.pref1 / (X.pref1 + X.pref2)
    betaX  = X.pref2 / (X.pref1 + X.pref2)
    alphaY = Y.pref1 / (Y.pref1 + Y.pref2)
    betaY  = Y.pref2 / (Y.pref1 + Y.pref2)
    total_1 = X.good1 + Y.good1
    total_2 = X.good2 + Y.good2
    
    # Equilibrium price of good 1 relative to good 2
    price = (X.good2 * alphaX + Y.good2 * alphaY) / (X.good1 * betaX + Y.good1 * betaY)

    # Allocation of good 1, following from demand function and market clearing conditions
    allocation_x1 = alphaX * (price * X.good1 + X.good2) / price 
    allocation_x1 = min(total_1 - 0.0001, max(0.0001, allocation_x1)) 
    allocation_y1 = total_1 - allocation_x1
    
    # Allocation of good 2, following from budget constraint and market clearing conditions
    allocation_x2 = price * allocation_x1 * X.pref2 / X.pref1 
    allocation_x2 = min(total_2 - 0.0001, max(0.0001, allocation_x2)) 
    allocation_y2 = total_2 - allocation_x2
    
    return (allocation_x1, allocation_x2), (allocation_y1, allocation_y2)
                       
    