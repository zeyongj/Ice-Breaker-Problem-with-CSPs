# This is the question 2 of Assignment 2.
# The following codes are modified and inspired via the website:https://github.com/Duo-Lu/CMPT310/tree/master/Assignment2 .
# I would like to appreciate the original author for his work.

from a2_q2 import * 


def check_teams(graph , csp_sol):
    length = len(csp_sol)
    check_dic = {}

    # To make teams.
    for i in range(length):
        check_dic.setdefault(i , [])
        check_dic.setdefault(csp_sol[i] , []).append(i)

    length_check = len(check_dic)

    # For nestered loops, they would be checked in teams whether it has friendship relations 
    for i in range(length_check):
        group_list =  check_dic[i]
 
        for i in range(len(group_list)):
            j = i + 1          
            for j in range(len(group_list)):
                if group_list[j] in graph[group_list[i]]:
                    return False
    return True
    return check_dic
