import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from vcModel import vcModel as vc
import pytest as ptest

prob = vc()