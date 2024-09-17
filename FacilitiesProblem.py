#
# FacilitiesProblem - Tony Martin, Makiah Randolph, Zach Whelan
#
# We confirm that all code is our own and is submitted according to 
# the integrity of MA491.
#

from __future__ import division # safety with double division
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Instantiate and name the model
M = AbstractModel()
M.name = "FacilitiesProblem"

# Sets

# Parameters

# Variables

# Objective
def CalcTotalDistance(M):
   return 
M.TotalDistance = Objective(rule=CalcTotalDistance, sense=minimize)

# Constraints

# Create a problem instance
instance = M.create_instance("FacilitiesProblem.dat")

# Indicate which solver to use
Opt = SolverFactory("gurobi")

# Generate a solution
Soln = Opt.solve(instance)
instance.solutions.load_from(Soln)

# Print the output
print("Termination Condition was "+str(Soln.Solver.Termination_condition))
display(instance)