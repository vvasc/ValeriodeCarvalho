# coding=utf-8
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
  
  def criterio1(self, l, x, vcm, L):
    """x = {(i,j): vcm.continuous_var(name='x_{0}_{1}'.format(i,j)) for i in range(1, 6) for j in range(1, 6)}"""
    x = {(0, i): vcm.continuous_var(name = 'x_{0}_{1}'.format(0, i)) for i in l}
    x = {}
    for u in range(1, len(l), 1):
      for i in range(0, L+1, 1): 
        for j in range(0, L+1, 1):
          for k in range(1, u, 1):
            if ((0 < i) & (i < j) & (j <= L) & (j-i == l[u])):
              x = {(i, j): vcm.continuous_var(name = 'x_{0}_{1}'.format(i, j))}
    vcm.print_information()

  def criterio2(self, L, lmin, x, vcm):
    x = {(i, i+1): vcm.continuous_var(name = 'x_{0}_{1}'.format(i, i+1)) for i in range(lmin, L-1, 1)}
    #print(x)

  def conservF(self, vcm, p, q, L, f, r1, r2, D):
    vcm.minimize(vcm.integer_var())
    #tm.add_constraint(tm.sum(x[i,j] for j in target) <= capacities[i])
    j = vcm.number_of_continuous_variables
    for i in range(0, j-1):
      if (vcm.get_var_by_name('x_' + str(0) + '_' + str(i))):
        p.append(vcm.get_var_by_name('x_' + str(0) + '_' + str(i)))
      else if (vcm.get_var_by_name('x_' + str(i) + '_' + str(L))):
        q.append(vcm.get_var_by_name('x_' + str(i) + '_' + str(L)))
    vcm.add_constraint(vcm.sum(p) == vcm.integer_var())
    vcm.add_constraint(vcm.sum(q) == vcm.integer_var())
    for h in range(1, L):
      for j in range(0, L+1):
        for g in range(0, L+1):
          if (vcm.get_var_by_name('x_' + str(j) + '_' + str(h)) & vcm.get_var_by_name('x_' + str(h) + '_' + str(g))):
            r1.append(vcm.get_var_by_name('x_' + str(j) + '_' + str(h)))
            r2.append(vcm.get_var_by_name('x_' + str(h) + '_' + str(g)))
    vcm.add_constraint(vcm.sum(r1) - vcm.sum(r2) == 0)
    


    #vcm.add_constraint(vcm.continuous_var() <= )
    #vcm.get_var_by_index()
    #print(p)
    #print(q)

  def getvar(self, vcm, y):
    j = vcm.number_of_continuous_variables
    for i in range(0, j):
      y.append(vcm.get_var_by_index(i))

    #print(y)
  
  def method(self):
    vcm = Model(name='valeriodecarvalho')
    x = {(i,j): vcm.continuous_var(name='x_{0}_{1}'.format(i,j)) for i in range(1, 6) for j in range(1, 6)}
    print(x)
  
  def __init__(self):
    print("iniciovalerio")
    l = [4, 3, 2]
    D = [10, 5, 3]
    x = {}
    y = [] #variavel auxiliar para imprimir a construção de arcos
    p = [] #variável auxiliar para construção das restrições
    q = [] #variável auxiliar para construção das restrições
    r1 = [] #variável auxiliar para construção das restrições
    r2 = [] #variável auxiliar para construção das restrições
    L = 9
    f = []
    vcm = Model(name='valeriodecarvalho')
    lmin = np.amin(l)
    #self.method()
    self.criterio1(l, x, vcm, L)
    self.criterio2(L, lmin, x, vcm)
    self.getvar(vcm, y)
    self.conservF(vcm, p, q, L, f, r1, r2, D)
