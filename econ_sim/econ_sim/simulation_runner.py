'''
Created on Jan 22, 2014

@author: Peter Norvig, Cliff Clive
'''

import populations
import transactions
import interactions
import simulation

if __name__ == '__main__':
    """
    simulation.report(populations.gauss, 
                      transactions.random_split, 
                      interactions.anyone)
    """
    '''
    X = populations.Agent(3, 5, 0.25, 0.75)
    Y = populations.Agent(2, 4, 0.33, 0.67)
    
    print 'X has ', X.allocation
    print 'U(X): ', X.utility
    print 'Y has ', Y.allocation
    print 'U(Y): ', Y.utility
    
    allocX, allocY = transactions.cobb_douglas_competitive_eqbm(X, Y)
    
    print 'X gets ', allocX
    print 'Y gets ', allocY
    
    X.allocation = allocX
    Y.allocation = allocY
    
    print 'X has ', X.allocation
    print 'U(X): ', X.utility
    print 'Y has ', Y.allocation
    print 'U(Y): ', Y.utility
    print '-' * 80
    '''

    simulation.report(populations.random_agent,
                      transactions.cobb_douglas_competitive_eqbm,
                      interactions.anyone)
    '''
    simulation.report(populations.random_bargaining_agent,
                      transactions.cobb_douglas_negotiation,
                      interactions.anyone)
                      #T=20*populations.N)
    '''