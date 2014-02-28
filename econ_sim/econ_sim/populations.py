'''
Created on Jan 22, 2014

@author: Peter Norvig, Cliff Clive
'''

import random
import numpy as np


N  = 5000 # Default size of population
mu = 100. # Default mean of population's wealth


def sample(distribution, N=N, mu=mu):
    "Sample from the distribution N times, then normalize results to have mean mu."
    return normalize([distribution() for _ in range(N)], mu * N)


def constant(mu=mu):
    return mu


def uniform(mu=mu, width=mu):
    return random.uniform(mu-width/2, mu+width/2)


def gauss(mu=mu, sigma=mu/3):
    return random.gauss(mu, sigma) 


def beta(alpha=2, beta=3):
    return random.betavariate(alpha, beta)


def pareto(alpha=4):
    return random.paretovariate(alpha)
    
    
def normalize(numbers, total):
    """ Scale the numbers so that they add up to total. """
    factor = total / float(sum(numbers))
    return [x * factor for x in numbers]


def random_agent(mu_e1=mu, mu_e2=mu, sigma_e1=mu/3, sigma_e2=mu/3, 
                 mu_p1=0.5, mu_p2=0.5, width_p1=0.5, width_p2=0.5):
    e1 = max(0, gauss(mu_e1, sigma_e1))
    e2 = max(0, gauss(mu_e2, sigma_e2))
    p1 = uniform(mu_p1, width_p1)
    p2 = uniform(mu_p2, width_p2)
    return Agent(e1, e2, p1, p2)


def random_bargaining_agent(mu_e1=mu, mu_e2=mu, sigma_e1=mu/3, sigma_e2=mu/3,
                            mu_p1=0.5, mu_p2=0.5, width_p1=0.0, width_p2=0.0,
                            mu_ch=0.5, width_ch=0.5):
    e1 = max(0, gauss(mu_e1, sigma_e1))
    e2 = max(0, gauss(mu_e2, sigma_e2))
    p1 = uniform(mu_p1, width_p1)
    p2 = uniform(mu_p2, width_p2)
    ch = uniform(mu_ch, width_ch)
    return BargainingAgent(e1, e2, p1, p2, ch)


class Agent(object):
    def __init__(self, endowment1, endowment2, preference1, preference2):
        """
        Agents are characterized by their allocations and preferences
        of goods 1 and 2. Economists usually call the starting value of
        a good an "endowment".
        The preference variables should be between 0 and 1.
        """
        self.good1 = max(0, endowment1)
        self.good2 = max(0, endowment2)
        self.pref1 = preference1
        self.pref2 = preference2
        
    @property
    def utility(self):
        """
        We'll use the Cobb-Douglas utility function for our model.
        """
        return pow(self.good1, self.pref1) * pow(self.good2, self.pref2)

    # The allocation property is just syntactic sugar that lets us assign
    # allocations using tuples a little more cleanly.
    @property
    def allocation(self): return (self.good1, self.good2)

    @allocation.setter
    def allocation(self, values): self.good1, self.good2 = values

    def demand(self, price):
        alpha = self.pref1 / (self.pref1 + self.pref2)
        quantity1 = alpha * (price * self.good1 + self.good2) / price
        quantity2 = price * quantity1 * self.pref2 / self.pref1
        return (quantity1, quantity2)

    # We need to define comparison operators in order to sort the
    # agents based on utility. I always prefer to define all of them
    # if I need to define any.
    def __gt__(self, other): return self.utility > other
    def __lt__(self, other): return self.utility < other
    def __eq__(self, other): return self.utility == other
    def __ge__(self, other): return self.utility >= other
    def __le__(self, other): return self.utility <= other
    def __ne__(self, other): return self.utility != other

    # We need to define multiplication and addition operators
    # in order to use Norvig's normalize function.
    def __mul__(self, other):
        self.good1 *= other
        self.good2 *= other
        return self
    
    def __radd__(self, other):
        return other + self.good1 + self.good2


class BargainingAgent(Agent):
    def __init__(self, endowment1, endowment2, preference1, preference2, cha):
        Agent.__init__(self, endowment1, endowment2, preference1, preference2)
        self.charisma = cha

    # We need to define comparison operators in order to sort the
    # agents based on charisma. I always prefer to define all of them
    # if I need to define any.
    def __gt__(self, other): return self.charisma > other
    def __lt__(self, other): return self.charisma < other
    def __eq__(self, other): return self.charisma == other
    def __ge__(self, other): return self.charisma >= other
    def __le__(self, other): return self.charisma <= other
    def __ne__(self, other): return self.charisma != other


def aggregate_demand(agents, max_price=10, steps=100):
    prices = (np.arange(steps) + 1) * max_price / float(steps)
    result = {}
    for price in prices:
        quantity = 0
        for a in agents:
            if a.demand(price)[0] > a.good1:
                quantity += a.demand(price)[0] - a.good1
        result[price] = quantity
    #quantities = [sum([a.demand(p)[0] - a.good1 for a in agents if a.demand(p)[0] > a.good1]) for p in prices]
    #return dict(zip(prices, quantities))
    return result


def aggregate_supply(agents, max_price=10, steps=100):
    prices = (np.arange(steps) + 1) * max_price / float(steps)
    result = {}
    for price in prices:
        quantity = 0
        for a in agents:
            if a.demand(price)[0] < a.good1:
                quantity += a.good1 - a.demand(price)[0]
        result[price] = quantity
    #quantities = [sum([a.good1 - a.demand(p)[0] for a in agents if a.demand(p)[0] < a.good1]) for p in prices]
    #return dict(zip(prices, quantities))
    return result


def find_market_equilibrium(supply, demand):
    surplus = dict(zip(supply.keys(),
                       [s - d for s, d in zip(supply.values(), demand.values())]))
    min_surplus = np.min(np.abs(surplus.values()))
    equilibrium_price = [p for p in surplus if abs(surplus[p]) == min_surplus][0]
    equilibrium_quantity = supply[equilibrium_price]
    return (equilibrium_price, equilibrium_quantity)