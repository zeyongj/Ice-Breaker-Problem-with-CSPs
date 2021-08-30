# This is the question 3 of Assignment 2.
# The following codes are modified and inspired via the website:https://github.com/Duo-Lu/CMPT310/tree/master/Assignment2 .
# I would like to appreciate the original author for his work.

from csp import *
import random


def rand_graph(number_node , probability):

    # The empty dictionary
    graph_dic = {}
    # To set the default value to the empty list to dictionary 
    for i in range(number_node):
        graph_dic.setdefault(i , [])


    for i in range(number_node - 1):            # Because j reached number_node - 1, i does not need touch the number_node - 1
        for j in range(i , number_node):
            if i != j:                         
                r = random.random()
                if r <= probability:            # If the random number(0 , 1) fall in given probability, then assign each other
                    graph_dic.setdefault(i , []).append(j)
                    graph_dic.setdefault(j , []).append(i)

    return graph_dic












