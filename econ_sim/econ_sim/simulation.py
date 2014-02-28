"""
Created on Jan 22, 2014

@author: Peter Norvig, Cliff Clive
"""

import matplotlib.pyplot as plt
import numpy as np

import populations
import transactions
import interactions


def simulate(population, transaction_fn, interaction_fn, T, percentiles, record_every):
    """
    Run simulation for T steps; collect percentiles every 'record_every' time steps.
    """
    results = []
    prices = []
    for t in range(T):
        i, j = interaction_fn(population)
        #population[i], population[j] = transaction_fn(population[i], population[j]) 
        population[i].allocation, population[j].allocation, price_t = transaction_fn(population[i], population[j])
        if t % record_every == 0:
            results.append(record_percentiles(population, percentiles))
            prices.append(price_t)
    return results, prices


def report(distribution=populations.gauss, 
           transaction_fn=transactions.random_split, 
           interaction_fn=interactions.anyone, 
           N=populations.N, mu=populations.mu, T=5*populations.N, 
           #percentiles=(1, 10, 25, 33.3, 50, -33.3, -25, -10, -1), record_every=25):
           percentiles=(1, 25, 50, -25, -1), record_every=25):
    """ Print and plot the results of the simulation running T steps. """
    # Run simulation
    pop = populations.sample(distribution, N, mu)
    supply = populations.aggregate_supply(pop)
    demand = populations.aggregate_demand(pop)
    eqbm_price = populations.find_market_equilibrium(supply, demand)[0]
    results, prices = simulate(pop, transaction_fn, interaction_fn, T, percentiles, record_every)
    # Print summary
    print('Simulation: {} * {}(mu={}) for T={} steps with {} doing {}:\n'.format(
          N, name(distribution), mu, T, name(interaction_fn), name(transaction_fn)))
    fmt = '{:6}' + '{:10.2f} ' * len(percentiles)
    print(('{:6}' + '{:>10} ' * len(percentiles)).format('', *map(percentile_name, percentiles)))
    for (label, nums) in [('start', results[0]), ('mid', results[len(results)//2]), ('final', results[-1])]:
        print fmt.format(label, *nums)
    # Plot results
    col = 1.0
    fig, axes = plt.subplots(1, 2)
    '''
    for line in zip(*results):
        norm_line = [x/line[0] for x in line]
        axes[0].plot(line, color=(col, 0, 1-col))
        axes[1].plot(norm_line, color=(col, 0, 1-col))
        col *= 0.75
    '''
    axes[0].scatter(np.array(demand.values())/1000., demand.keys(), c='g')
    axes[0].scatter(np.array(supply.values())/1000., supply.keys())
    axes[0].plot([eqbm_price] * len(prices), 'r')
    axes[0].set_xlim(0, 100)
    axes[0].set_ylim(0, 5)

    axes[1].plot(prices)
    axes[1].plot([eqbm_price] * len(prices), 'r')
    axes[1].set_ylim(0, 5)

    plt.show()


def record_percentiles(population, percentiles):
    """ Pick out the percentiles from population. """
    population = sorted(population, reverse=True)
    N = len(population)
    #return [population[int(p*N/100.)] for p in percentiles] 
    return [population[int(p*N/100.)].utility for p in percentiles]


def percentile_name(p):
    return ('median' if p == 50 else 
            '{} {}%'.format(('top' if p > 0 else 'bot'), abs(p)))

    
def name(obj):
    return getattr(obj, '__name__', str(obj))