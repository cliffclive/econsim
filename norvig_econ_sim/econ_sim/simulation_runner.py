'''
Created on Jan 22, 2014

@author: Peter Norvig
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
    
    X = populations.agent(3, 5, 0.25, 0.75)
    Y = populations.agent(2, 4, 0.33, 0.67)
    
    print 'X has ', X.allocation
    print 'U(X): ', X.utility
    print 'Y has ', Y.allocation
    print 'U(Y): ', Y.utility
    
    allocX, allocY = transactions.edgeworth_trade(X, Y)
    
    print 'X gets ', allocX
    print 'Y gets ', allocY
    
    X.allocation = allocX
    Y.allocation = allocY
    
    print 'X has ', X.allocation
    print 'U(X): ', X.utility
    print 'Y has ', Y.allocation
    print 'U(Y): ', Y.utility
    print '-' * 80
    
    simulation.report(populations.random_agent,
                      transactions.edgeworth_trade,
                      interactions.anyone)
