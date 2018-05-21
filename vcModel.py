# coding=utf-8
import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np
import docplex.mp
from docplex.mp.model import Model
from docplex.util.environment import get_environment



class vcModel:
  
  nodes = range(1, 6)
  
  def criterio1(self, l, x, vcm, L):
    x = {(0, i): vcm.continuous_var(name = 'x_{0}_{1}'.format(0, i)) for i in l}
    x = {}
    for u in range(0, len(l), 1):
      for i in range(0, L+1, 1): 
        for j in range(i, L+1, 1):
          for k in range(0, u+1, 1):
            if ((0 < i) & (i < j) & (j <= L) & (j-i == l[u]) & (self.inarc(i - l[k], i, vcm))): #problemas
              if (not self.inarc(i, j, vcm)):
                x = {(i, j): vcm.continuous_var(name = 'x_{0}_{1}'.format(i, j))}
               
  def criterio2(self, L, lmin, x, vcm):
    x = {(i, i+1): vcm.continuous_var(name = 'x_{0}_{1}'.format(i, i+1)) for i in range(lmin, L, 1)}
    

  def conservF(self, vcm, p, q, L, l, f, r1, r2, D, d, ek):
    vcm.continuous_var(name='z')
    #vcm.integer_var(name='z')
    vcm.set_objective('min', vcm.get_var_by_name('z'))
    #restrições de conservação de fluxo
    j = vcm.number_of_continuous_variables
    for i in range(0, j-1):
      if (vcm.get_var_by_name('x_' + str(0) + '_' + str(i))):
        p.append(vcm.get_var_by_name('x_' + str(0) + '_' + str(i)))
      if (vcm.get_var_by_name('x_' + str(i) + '_' + str(L))):
        q.append(vcm.get_var_by_name('x_' + str(i) + '_' + str(L)))
    vcm.add_constraint(vcm.get_var_by_name('z') == vcm.sum(p))
    vcm.add_constraint(- vcm.get_var_by_name('z') == - vcm.sum(q))
    for j in range(1, L, 1):
      for i in range(0, j, 1):
        if (vcm.get_var_by_name('x_' + str(i) + '_' + str(j))):
          r1.append(vcm.get_var_by_name('x_' + str(i) + '_' + str(j)))
      for k in range(j, L+1, 1):
        if (vcm.get_var_by_name('x_' + str(j) + '_' + str(k))):
          r2.append(vcm.get_var_by_name('x_' + str(j) + '_' + str(k)))
      if (bool(r1) & bool(r2)):
        vcm.add_constraint(vcm.sum(r1) - vcm.sum(r2) == 0)
      r1 = []
      r2 = []  
    for i in range(len(l)):
      d = []
      for k in range(0, L+1):
        if (vcm.get_var_by_name('x_' + str(k) + '_' + str(k+l[i]))):
          d.append(vcm.get_var_by_name('x_' + str(k) + '_' + str(k+l[i])))

      if (bool(d)):
        vcm.add_constraint(vcm.sum(d) == D[i])  
    vcm.print_information()

  def getvar(self, vcm, y):
    j = vcm.number_of_continuous_variables
    for i in range(0, j):
      y.append(vcm.get_var_by_index(i))
   

  def inarc(self, i, j, vcm):
    y = []
    straux = ""
    straux2 = []
    if (i<0):
      return False
    self.getvar(vcm, y)
    for k in range(len(y)):
      straux = y[k].name
      straux2 = straux.rsplit('_', 2)
      if((str(i) == straux2[1]) & (str(j) == straux2[2])):
        return True
    return False

  
  def __init__(self, l, D, L, ek, name):
    print("iniciovalerio")
    x = {}
    y = [] #variavel auxiliar para imprimir a construção de arcos
    p = [] #variável auxiliar para construção das restrições
    q = [] #variável auxiliar para construção das restrições
    r1 = [] #variável auxiliar para construção das restrições
    r2 = [] #variável auxiliar para construção das restrições
    d = [] #variável auxiliar para a construção da demanda
    f = []
    vcm = Model(name='valeriodecarvalho')
    lmin = np.amin(l)
    self.criterio2(L, lmin, x, vcm)
    self.criterio1(l, x, vcm, L)
    self.getvar(vcm, y)
    self.conservF(vcm, p, q, L, l, f, r1, r2, D, d, ek)
    vcms = vcm.solve(url=None, key=None)
    reseau = open(name, 'w', 0)
    reseau.write('Função Objetivo: ' + str(vcm.solution.get_objective_value))
    reseau.close()
    with get_environment().get_output_stream("solution.json") as fp:
      vcm.solution.export(fp, "json")
