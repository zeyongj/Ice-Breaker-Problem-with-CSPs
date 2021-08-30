# This is the question 3 of Assignment 2.
# The following codes are modified and inspired via the website:https://github.com/Duo-Lu/CMPT310/tree/master/Assignment2 .
# I would like to appreciate the original author for his work.

from csp import *
from a2_q1 import *
from a2_q2 import * 
import random
import time 


# Modify the CSP class from the course handbook.
class CSP(search.Problem):

    def __init__(self, variables, domains, neighbors, constraints):

        variables = variables or list(domains.keys())

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0
        self.nuassigns = 0               # extra attribute for remembering unassign

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]
            self.nuassigns = self.nuassigns + 1    # same as assign, when function calls, increase the unassign

    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""
        # Subclasses may implement this more efficiently
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))
        return count(conflict(v) for v in self.neighbors[var])

    def display(self, assignment):
        """Show a human-readable representation of the CSP."""
        # Subclasses can print in a prettier way, or display with a GUI
        print('CSP:', self, 'with assignment:', assignment)

    # These methods are for the tree and graph-search interface:

    def actions(self, state):
        """Return a list of applicable actions: nonconflicting
        assignments to an unassigned variable."""
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, action):
        """Perform an action and return the new state."""
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        """The goal is to assign all variables, with all constraints satisfied."""
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    # These are for constraint propagation

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        """Return the partial assignment implied by the current inferences."""
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)

    # This is for min_conflicts search

    def conflicted_vars(self, current):
        """Return a list of variables in current assignment that are in conflict"""
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]
    
    def mac(csp, var, value, assignment, removals):
        """Maintain arc consistency."""
        return AC3(csp, {(X, var) for X in csp.neighbors[var]}, removals)

    
# Constraint Propagation with AC-3


def AC3(csp, queue=None, removals=None):
    """[Figure 6.3]"""
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True


def revise(csp, Xi, Xj, removals):
    """Return true if we remove a value."""
    count = 0
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
            count += 1
    return revised

# CSP Backtracking Search

#-----------------------------------------------------------------------------------------------------------------
# Input the graphs as requirement.
graphs = [rand_graph(30, 0.1), rand_graph(30, 0.2), rand_graph(30, 0.3),
          rand_graph(30, 0.4), rand_graph(30, 0.5)]
#-----------------------------------------------------------------------------------------------------------------


# The following code is taken from the website: https://www.cs.cmu.edu/afs/cs/academic/class/15381-s07/www/slides/020107CSP.pdf .
def constraints(A, a, B, b):
    return a != b


def max_team(assignment):
    """ people are random arrange in team. Search for max value of team. Help function for num_teams"""
    length = len(assignment)
    max = -1
    for i in range(length):
        if assignment[i] > max:
            max = assignment[i]

    return max + 1

def num_teams(assignment):
    """ given assignment , calculate exactly number of team people are exactly divided into"""
    max_number = max_team(assignment)

    check_team = []
    for i in range(max_number):
        check_team.append(0)

    for x in assignment:
        check_team[assignment[x]] = 1
    
    return sum(check_team)


def run_q3_all_domain(graph_given):
    graph = graph_given
    
    variable = []
    domain = {}
    neighbors = graph

    for key in graph:                   # To make variable list
        variable.append(key)


    total_number_of_assign = 0          # Set extra variable for remember  
    total_number_of_unassign = 0
    last_time_assign = 0;
    last_time_unassign = 0

    new_len = [];           
    for i in range(len(variable)):
        new_len.append(i)               
        for j in range(len(variable)):
            domain.setdefault(j , new_len)
        csp_obj = CSP(variable , domain , neighbors , constraints)      # To create the CSP object 
        AC3(csp_obj)
        assignment = backtracking_search(csp_obj , mrv , lcv , mac)
        total_number_of_assign += csp_obj.nassigns
        total_number_of_unassign += csp_obj.nuassigns
        if assignment != None:
            break
    last_time_assign = csp_obj.nassigns                                 # To remember the last time(when we find the first solution)
    last_time_unassign = csp_obj.nuassigns
    number_people_divided = num_teams(assignment)                       # To calculate the exactly people are divided into 
 
    return assignment , number_people_divided , total_number_of_assign , total_number_of_unassign , last_time_assign , last_time_unassign

graph = graphs[4]
run_q3_all_domain(graph)


def run_q3():
    
    assignment = {0:[] , 1:[] , 2:[] , 3:[] , 4:[]}
    number_people_divided = {0:[] , 1:[] , 2:[] , 3:[] , 4:[]}
    time_ = {0:[] , 1:[] , 2:[] , 3:[] , 4:[]}
    total_number_of_assign = {0:[] , 1:[] , 2:[] , 3:[] , 4:[]}
    total_number_of_unassign = {0:[] , 1:[] , 2:[] , 3:[] , 4:[]}
    last_time_assign = {0:[] , 1:[] , 2:[] , 3:[] , 4:[]}
    last_time_unassign = {0:[] , 1:[] , 2:[] , 3:[] , 4:[]}

    for i in range(5):
        for j in range(5):
            graph = graphs[i]
            
            start_time = time.time()
            assignment_ , number_people_divided_ , total_number_of_assign_ , total_number_of_unassign_ , last_time_assign_ , last_time_unassign_ = run_q3_all_domain(graph)
            elapsed_time = time.time() - start_time
            assignment[i].append(assignment_)
            number_people_divided[i].append(number_people_divided_)
            time_[i].append(elapsed_time)
            total_number_of_assign[i].append(total_number_of_assign_)
            total_number_of_unassign[i].append(total_number_of_unassign_)
            last_time_assign[i].append(last_time_assign_)
            last_time_unassign[i].append(last_time_unassign_)
    
    
            print('________________________________________________________________________________________________')
            
            print('The assignment is (exactly min solution)' , assignment_)
            print('The number of teams that the people are divided into' , number_people_divided_)
            print('________________________________________________________________________________________________')

            print(f'elapsed time (in seconds): {elapsed_time}')

            print('The total number of times CSP variables were assigned' , total_number_of_assign_)
            print('The total number of times CSP variables were unassigned' , total_number_of_unassign_)
            
            print('The last time CSP variables were assigned (complete find min number team)' , last_time_assign_)
            print('The last time CSP variables were unassigned (complete find min number team)' , last_time_unassign_)
            print('________________________________________________________________________________________________')


    print('\n\n\n')
    print('The number of teams that the people are divided into')
    for i in range(5):
        print(number_people_divided[i])

    
    print('The total number of times CSP variables were assigned')
    for i in range(5):
        print(total_number_of_assign[i])

    print('The running time')
    for i in range(5):
        print(time_[i])

    print('The total number of times CSP variables were unassigned')
    for i in range(5):
        print(total_number_of_unassign[i])

    print('The last time CSP variables were assigned (complete find min number team)')
    for i in range(5):
        print(last_time_assign[i])
        
    print('The last time CSP variables were unassigned (complete find min number team)')
    for i in range(5):
        print(last_time_unassign[i])

            

if __name__ == "__main__":
    run_q3()






















