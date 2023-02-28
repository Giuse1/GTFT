import random
from node import Node
random.seed(0)


import argparse


parser = argparse.ArgumentParser()


args = parser.add_argument_group('')
args.add_argument('--out_path', type=str, default="NAR")
args.add_argument('--eps', type=float, default=0.3)
args = parser.parse_args()

out_path = args.out_path
final_eps = args.eps

N_round = 100000
N_nodes = 25
N_classes = 5
power_costraints = [0.03, 0.025, 0.02, 0.015, 0.01]
tau = [0.84,0.49,0.3,0.2,0.12]
initial_eps = 0.3
current_eps = initial_eps
# EPS = 0.3 #todo


dict_nodes = {}
idx = 0
print(f"---------")

print(f"EPS {final_eps}")
for _ in range(N_nodes):
    cls = (idx//N_classes)
    n = Node(idx+1, cls, power_costraints[cls-1], N_classes)
    print((idx+1, cls, power_costraints[cls-1], N_classes))
    dict_nodes[idx+1] = n
    idx += 1


for r in range(N_round):
    if r%10000 == 0:
        print(f"Round {r}")

    # idx_r = random.randint(1,N_nodes) # index_requester
    idx_r, idx_l = random.sample(range(1,N_nodes+1), 2) # index_requester and index_learner
    requester_node = dict_nodes[idx_r]
    learner_node = dict_nodes[idx_l]
    class_round = max(requester_node.cls, learner_node.cls)

    learner_node_psi = learner_node.get_psi(class_round)
    learner_node_fi = learner_node.get_fi(class_round)

    learner_node.increase_received_request(class_round)
    requester_node.increase_made_request(class_round,r)
    # if class_round == 1:
    #     print(1)

    if r==1000:
        current_eps = final_eps

    if learner_node_psi > tau[class_round-1] or learner_node_fi < learner_node_psi - current_eps:
        pass
    else:
        learner_node.increase_received_request_accepted(class_round)
        requester_node.increase_made_request_accepted(class_round, r)


for k,n in dict_nodes.items():

    tot_tx = sum(n.received_requests_accepted) + sum(n.made_requests_accepted)
    print(f"Node {n.idx} mean spent power: {tot_tx/N_round}")
    n.NAR.to_csv(f"{out_path}/one_node/node_{k}_{final_eps}.csv")



