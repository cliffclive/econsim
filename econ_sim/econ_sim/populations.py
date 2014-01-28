'''
Created on Jan 22, 2014

@author: Peter Norvig, Cliff Clive
'''

import random


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
    "Scale the numbers so that they add up to total."
    factor = total / float(sum(numbers))
    return [x * factor for x in numbers]


def random_agent(mu_e1=mu, mu_e2=mu, sigma_e1=mu/3, sigma_e2=mu/3, 
                 mu_p1=0.5, mu_p2=0.5, width_p1=0.5, width_p2=0.5):
    e1 = gauss(mu_e1, sigma_e1)
    e2 = gauss(mu_e2, sigma_e2)
    p1 = uniform(mu_p1, width_p1)
    p2 = uniform(mu_p2, width_p2)
    return agent(e1, e2, p1, p2)


class agent(object):
    def __init__(self, endowment1, endowment2, preference1, preference2):
        self.good1 = max(0, endowment1)
        self.good2 = max(0, endowment2)
        self.pref1 = preference1
        self.pref2 = preference2
        
    @property
    def utility(self): return pow(self.good1, self.pref1) * pow(self.good2, self.pref2)
    
    @property
    def allocation(self): return (self.good1, self.good2)
    
    @allocation.setter
    def allocation(self, values):
        self.good1 = values[0]
        self.good2 = values[1]
        if self.good1 < 0: print "We've gone negative!"
        if self.good2 < 0: print "We've gone negative!"
    
    def __gt__(self, other): return self.utility > other
    def __lt__(self, other): return self.utility < other
    def __eq__(self, other): return self.utility == other
    def __ge__(self, other): return self.utility >= other
    def __le__(self, other): return self.utility <= other
    def __ne__(self, other): return self.utility != other
    
    def __mul__(self, other):
        self.good1 *= other
        self.good2 *= other
        return self
    
    def __radd__(self, other):
        return other + self.good1 + self.good2
        


        