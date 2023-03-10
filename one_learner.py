import os
import random
import argparse
from node import Node
random.seed(0)

from sympy import symbols, nonlinsolve


parser = argparse.ArgumentParser()
args = parser.add_argument_group('')
args.add_argument('--out_path', type=str, default="NAR")
args.add_argument('--in_eps', type=float, default=0.3)
args.add_argument('--fin_eps', type=float, default=0.3)
args.add_argument('--in_round', type=int, default=1000)
args = parser.parse_args()

out_path = args.out_path

in_eps = args.in_eps
current_eps = in_eps
fin_eps = args.fin_eps
in_round = args.in_round

N_round = 100000
N_nodes = 25
N_classes = 5
K = N_classes
n_list = [5] * 5 # todo
power_costraints = [0.03, 0.025, 0.02, 0.015, 0.01] # todo

a, b, c, d, e = symbols('a, b, c, d, e', real=True)
symbol_list = [a,b,c,d, e]

from functools import reduce
from operator import add



eq_list = []
for i in range(0,K):
    eq = []
    eq += [(n_list[k]*symbol_list[i]) for  k in range(0,i)]
    eq += [(n_list[i]-1) * symbol_list[i]]
    eq += [(n_list[l] * symbol_list[l]) for l in range(i+1,K)]

    eq += [-power_costraints[i]*N_nodes*(N_nodes-1)/2]
    eq = reduce(add, eq)
    eq_list.append(eq)
    print(eq)


# eq_list = []
# for i in range(0,K):
#     eq = 0
#     for k in range(0,i):
#         eq += (n_list[k]*symbol_list[i])
#
#     eq += (n_list[i]-1) * symbol_list[i]
#
#     for l in range(i+1,K):
#         eq += (n_list[l] * symbol_list[l])
#
#     eq -= power_costraints[i]*N_nodes*(N_nodes-1)/2
#     eq_list.append(eq)
#     print(eq)



tau  = nonlinsolve(eq_list, symbol_list).args
# tau = [0.84,0.49,0.3,0.2,0.12]

os.makedirs(f"{out_path}/one_node/in_round_{in_round}/inG_{in_eps}_fG_{fin_eps}", exist_ok=True)


dict_nodes = {}
idx = 0
print(f"---------")

print(f"Initial EPS {in_eps}, final EPS {fin_eps}")
for _ in range(N_nodes):
    cls = (idx//N_classes)
    n = Node(idx, cls, power_costraints[cls], N_classes)
    print((idx, cls, power_costraints[cls], N_classes))
    dict_nodes[idx] = n
    idx += 1


for r in range(N_round):
    if r%10000 == 0:
        print(f"Round {r}")

    if r==in_round:
        current_eps = fin_eps

    # idx_r = random.randint(1,N_nodes) # index_requester
    idx_r, idx_l = random.sample(range(0,N_nodes), 2) # index_requester and index_learner
    requester_node = dict_nodes[idx_r]
    learner_node = dict_nodes[idx_l]
    class_round = max(requester_node.cls, learner_node.cls)

    learner_node_psi = learner_node.get_psi(class_round)
    learner_node_fi = learner_node.get_fi(class_round)

    learner_node.increase_received_request(class_round)
    requester_node.increase_made_request(class_round,r)
    # if class_round == 1:
    #     print(1)
    # print(class_round)
    # print(tau[class_round])
    if learner_node_psi > tau[class_round] or learner_node_fi < learner_node_psi - current_eps:
        pass
    else:
        learner_node.increase_received_request_accepted(class_round)
        requester_node.increase_made_request_accepted(class_round, r)

power_list = []

for k,n in dict_nodes.items():

    tot_tx = sum(n.received_requests_accepted) + sum(n.made_requests_accepted)
    print(f"Node {n.idx} mean spent power: {tot_tx/N_round}")
    power_list.append(tot_tx/N_round)
    n.NAR.to_csv(f"{out_path}/one_node/in_round_{in_round}/inG_{in_eps}_fG_{fin_eps}/node_{k}.csv")

import json
with open(f"{out_path}/one_node/in_round_{in_round}/power_inG_{in_eps}_fG_{fin_eps}.json", 'w') as f:
    json.dump(power_list, f)

