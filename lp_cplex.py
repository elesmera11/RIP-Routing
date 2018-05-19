
import subprocess
import itertools
import time

#==============================================================================#
# Global Variables
#==============================================================================#
# cplex path (change if your cplex is in a different path)
CPLEX = "/home/cosc/student/ysk28/cplex/cplex/bin/x86-64_linux/cplex"
# lp file path (change if your files are in a different file)
FILE = "/home/cosc/student/ysk28/Documents/COSC364/Assignment2/out.lp"
# cplex command line 
COMMAND = CPLEX + ' -c "read ' + FILE + '" "optimize" "display solution variables -"'

print(COMMAND)