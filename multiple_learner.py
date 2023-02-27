import random
from node import Node
import argparse
import numpy as np

random.seed(0)

parser = argparse.ArgumentParser()

args = parser.add_argument_group('')
args.add_argument('--out_path', type=str, default="NAR")
args.add_argument('--eps', type=float, default=0.3)
args = parser.parse_args()


out_path = args.out_path
final_eps = args.eps

N_round = 100000
N_nodes = 12
N_classes = 2
M = 2
nodes_per_class = [6,6]
power_costraints = [0.03,  0.015]
tau = [0.35,0.11]
initial_eps = 0.3
current_eps = initial_eps
# EPS = 0.3 #todo

l_list = range(1,M+1)
q_l_uniform = [1/M]*M



dict_nodes = {}
idx = 0
print(f"---------")

print(f"EPS {final_eps}")
for cls, n in enumerate(nodes_per_class):

    for _ in range(n):
        n = Node(idx+1, cls, power_costraints[cls], N_classes)
        print((idx+1, cls, power_costraints[cls], N_classes))
        dict_nodes[idx+1] = n
        idx += 1


for r in range(N_round):
    if r%10000 == 0:
        print(f"Round {r}")

    l = np.random.choice(l_list, p=q_l_uniform) # number of learners required
    # idx_r = random.randint(1,N_nodes) # index_requester
    idx_nodes = random.sample(range(1,N_nodes+1), l+1) # index_requester and index_learners

    idx_r = idx_nodes[0]
    idx_learners = idx_nodes[1:]


    requester_node = dict_nodes[idx_r]
    learner_nodes = [dict_nodes[idx_l] for idx_l in idx_learners]
    learner_classes = [learner.cls for learner in learner_nodes]

    class_round = max(requester_node.cls, max(learner_classes))

    learner_node_psi_list = [learner.get_psi(class_round) for learner in learner_nodes]
    learner_node_fi_list = [learner.get_fi(class_round) for learner in learner_nodes]

    [learner.increase_received_request(class_round) for learner in learner_nodes]
    requester_node.increase_made_request(class_round,r)
    # if class_round == 1:
    #     print(1)

    if r==1000:
        current_eps = final_eps

    accepted_request = True
    for idx, learner in enumerate(learner_nodes):

        if learner_node_psi_list[idx] > tau[class_round-1] or learner_node_fi_list[idx] < learner_node_psi_list[idx] - current_eps:
            accepted_request = False
            break

    if accepted_request:
            [learner.increase_received_request_accepted(class_round) for learner in learner_nodes]
            requester_node.increase_made_request_accepted(class_round, r)


for k,n in dict_nodes.items():

    n.NAR.to_csv(f"{out_path}/multiple_nodes/node_{k}_{final_eps}.csv")



