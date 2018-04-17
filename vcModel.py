import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np
import docplex.mp
from docplex.mp.model import Model


"""tm = Model(name='transportation')
capacities = {1: 15, 2: 20}
demands = {3: 7, 4: 10, 5: 15}
costs = {(1,3): 2, (1,5):4, (2,4):5, (2,5):3}
# Python ranges will be used to iterate on source, target nodes.
source = range(1, 3) # {1, 2}
target = range(3, 6) # {3,4,5}
# create flow variables for each couple of nodes
# x(i,j) is the flow going out of node i to node j
x = {(i,j): tm.continuous_var(name='x_{0}_{1}'.format(i,j)) for i in source for j in target}

# each arc comes with a cost. Minimize all costed flows
tm.minimize(tm.sum(x[i,j]*costs.get((i,j), 0) for i in source for j in target))

tm.print_information()
#def method(self):"""

class vcModel:
  
  nodes = range(1, 6)
  
  
  def method(self):
    vcm = Model(name='valeriodecarvalho')
    x = {(i,j): vcm.continuous_var(name='x_{0}_{1}'.format(i,j)) for i in range(1, 6) for j in range(1, 6)}
    print(x)
  
  def __init__(self):
    print("iniciovalerio")
    self.method()