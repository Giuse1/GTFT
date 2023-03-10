import random
from node import Node
import argparse
import numpy as np
from sympy.solvers import solve
from sympy import Symbol
import matplotlib.pyplot as plt
import pandas as pd


from sympy import symbols, nonlinsolve
from functools import reduce
from operator import add

import itertools
from operator import mul

random.seed(0)

parser = argparse.ArgumentParser()

args = parser.add_argument_group('')
args.add_argument('--out_path', type=str, default="NAR")
args.add_argument('--eps', type=float, default=0.01)
args = parser.parse_args()


out_path = args.out_path
final_eps = args.eps

N_round = 100000
N = 12
n1, n2 = 6,6
N_classes = 2
M = 2
nodes_per_class = [6,6]
power_costraints = [0.03,  0.015]
initial_eps = final_eps
current_eps = initial_eps
# EPS = 0.3 #todo

l_list = list(range(1,M+1))
q_l = [1/M]*M

a, b = symbols('a, b', real=True)
symbol_list = [a,b]

eq_list = []


eq_2_r = [(q_l[l-1]*b**l)/N for l in range(1,M+1) ]
eq_2_l = [(q_l[l-1]*l*b**(l))/N for l in range(1,M+1) ]
eq_2_r = reduce(add, eq_2_r)
eq_2_l = reduce(add, eq_2_l)
eq_2 = eq_2_l+eq_2_r-power_costraints[1]


eq_1_r = (1/N)*q_l[0]*(n2*b/(N-1) + (1-n2/(N-1))*a) + (1/N)*q_l[1]*((n1-1)*(n1-2)*a*a/((N-1)*(N-2)) + (1-(n1-1)*(n1-2)/((N-1)*(N-2) ))*b*b)
eq_1_l = (1/N)*q_l[0]*(n2*b/(N-1) + (1-n2/(N-1))*a) + (2/N)*q_l[1]*((n1-1)*(n1-2)*a*a/((N-1)*(N-2)) + (1-(n1-1)*(n1-2)/((N-1)*(N-2)))*b*b)
eq_1 = eq_1_l+eq_1_r-power_costraints[0]


eq_list = [ eq_1, eq_2]
tau_all  = nonlinsolve(eq_list, symbol_list).args

for t in tau_all:
    if t[0]>=0 and t[1] >=0:
        tau = t
# tau = [0.56,0.12]

# L[r,c] for L value when node is of class r and ession of class c
# L = np.matrix([[5/11+2*tau[0]/11, 6/11+6*tau[1]/11],
#                [np.NAN,1+tau[1] ]
#                ])


comb_list = []
l_list = [1, 2]
tau_list = tau

for r in range(1,3):
    for v in itertools.product(l_list, repeat=r):
        comb_list += [v]
# comb_list


# L = np.zeros((2,2))
# tmp = np.zeros((2,2))
# for requester in [1,2]:
#
#     for c in comb_list:
#         # print(requester)
#         # print(c)
#         cls_session = max(requester, max(c))
#         # print(cls_session)
#         probability_accept = [tau_list[t-1] for t in c]
#         # print(probability_accept)
#         prob = reduce(mul, probability_accept)
#         L[requester-1][cls_session-1] += prob
#         tmp[requester-1][cls_session-1] += 1
#         # print(prob)
#         # print("---")
# print(L)
# print(tmp)
# L = L/2
# print(L)
#
# for c in range(2):
#     L[:,c] =L[:,c]/tau_list[c]
#
# print(L)


L = np.array([[0.5*tau[0]*(1+tau[0]), 0.5*tau[1]*(1+tau[1])],[0, 0.5*tau[1]*(1+tau[1])]])
print(L)
for c in range(2):
    L[:,c] =L[:,c]/tau_list[c]

print(L)

dict_nodes = {}
idx = 0
print(f"---------")

print(f"EPS {final_eps}")

# df = pd.DataFrame(columns=["round","node","session_class","type","accepted"])

for cls, n in enumerate(nodes_per_class):

    for _ in range(n):
        n = Node(idx, cls, power_costraints[cls], N_classes)
        print((idx, cls, power_costraints[cls], N_classes))
        dict_nodes[idx] = n
        idx += 1



sessions = []
for r in range(N_round):
    if r%10000 == 0:
        print(f"Round {r}")

    l = np.random.choice(l_list, p=q_l) # number of learners required
    sessions.append(l)
    # idx_r = random.randint(1,N) # index_requester
    idx_nodes = random.sample(range(0,N), l+1) # index_requester and index_learners, l+1 cuase learners plus requester

    idx_r = idx_nodes[0]
    idx_learners = idx_nodes[1:]


    requester_node = dict_nodes[idx_r]
    learner_nodes = [dict_nodes[idx_l] for idx_l in idx_learners]
    learner_classes = [learner.cls for learner in learner_nodes]

    class_round = max(requester_node.cls, max(learner_classes))

    learner_node_psi_list = [learner.get_psi(class_round) for learner in learner_nodes]
    learner_node_fi_list = [learner.get_fi(class_round) for learner in learner_nodes]

    [learner.increase_received_request(class_round, r) for learner in learner_nodes]
    requester_node.increase_made_request(class_round,r)
    # if class_round == 1:
    #     print(1)

    if r==1000:
        current_eps = final_eps

    accepted_request = True
    for idx, learner in enumerate(learner_nodes):

        if learner_node_psi_list[idx] > tau[class_round] or learner_node_fi_list[idx] < L[learner.cls,class_round]*learner_node_psi_list[idx] - current_eps:
            accepted_request = False
            break

    if accepted_request:
            [learner.increase_received_request_accepted(class_round, r) for learner in learner_nodes]
            requester_node.increase_made_request_accepted(class_round, r)


power_list = []
for k,n in dict_nodes.items():

    print(f"Node {n.idx} mean spent power: {sum(n.received_requests_accepted)/N_round}")
    power_list.append(sum(n.received_requests_accepted)/N_round)
    # n.NAR.to_csv(f"{out_path}/multiple_nodes/node_{k}_{final_eps}.csv")
    n.df.to_csv(f"{out_path}/multiple_nodes/df_all_node_{k}_{final_eps}.csv")

# df.to_csv(f"{out_path}/multiple_nodes/df_all_{final_eps}.csv")


for k in range(N_classes):

    tmp = power_list[k*n1: k*n1+n1]
    plt.bar(range(k*n1, k*n1+n1), tmp)
    plt.hlines(xmin=k*n1-0.5, xmax=k*n1+n1-0.5,y=power_costraints[k], color="red")


plt.show()