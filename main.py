import random

from node import Node

random.seed(0)

N_round = 100000
N_nodes = 25
N_classes = 5
power_costraints = [0.03, 0.025, 0.02, 0.015, 0.01]
tau = [0.84,0.49,0.3,0.2,0.12]
# EPS = 0.3 #todo


for EPS in [0]:
    dict_nodes = {}
    idx = 0
    print(f"---------")

    print(f"EPS {EPS}")
    for _ in range(N_nodes):
        cls = (idx//N_classes)+1
        n = Node(idx+1, cls, power_costraints[cls-1], N_classes)
        print((idx+1, cls, power_costraints[cls-1], N_classes))
        dict_nodes[idx+1] = n
        idx += 1



    for r in range(N_round):
        if r%1000 == 0:
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
        if r == 0:
            psi_start = 0.8
            fi_start = 0.1
            if psi_start > tau[class_round-1] or fi_start < psi_start - EPS:
                pass
            else:
                learner_node.increase_received_request_accepted(class_round)
                requester_node.increase_made_request_accepted(class_round, r)


        else:
            if learner_node_psi > tau[class_round-1] or learner_node_fi < learner_node_psi - EPS:
                pass
            else:
                learner_node.increase_received_request_accepted(class_round)
                requester_node.increase_made_request_accepted(class_round, r)


    for k,n in dict_nodes.items():

        n.NAR.to_csv(f"NAR/node_{k}_{EPS}.csv")



