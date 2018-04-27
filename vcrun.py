# coding=utf-8
import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from vcModel import vcModel as vc
import pytest as ptest

#prob = vc([4, 3, 2], [10, 5, 3], 9, 10, "exemplo1")
prob = vc([28, 27, 26, 24, 23, 19, 17, 16, 10, 5], [90, 69, 100, 88, 59, 25, 25, 34, 25, 39], 66, 1000, "exemplo 0")
