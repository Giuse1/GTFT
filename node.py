import  pandas as pd

class Node:
    def __init__(self, idx, cls, power, n_classes):
        self.idx = idx
        self.cls = cls
        self.power = power
        self.made_requests = [0] * n_classes  # B
        self.made_requests_accepted = [0] * n_classes  # A
        self.received_requests = [0] * n_classes  # D
        self.received_requests_accepted = [0] * n_classes  # C
        self.NAR = pd.DataFrame(columns=["round","class","made","made_accepted"])

    def get_psi(self, class_round):

        class_round -= 1  # to consider that class 1 has index 0
        try:
            to_return = self.received_requests_accepted[class_round] / self.received_requests[class_round]
        except:
            to_return = 0
        return to_return

    def get_fi(self, class_round):
        class_round -= 1  # to consider that class 1 has index 0
        try:
            to_return = self.made_requests_accepted[class_round] / self.made_requests[class_round]
        except:
            to_return = 0
        return to_return

    def increase_made_request(self, class_round, rnd):
        class_round -= 1
        self.made_requests[class_round] += 1
        self.NAR.loc[len(self.NAR)] = [rnd,class_round+1, self.made_requests[class_round],self.made_requests_accepted[class_round]]

    def increase_made_request_accepted(self, class_round,rnd):
        class_round -= 1
        self.made_requests_accepted[class_round] += 1
        self.NAR.loc[len(self.NAR)-1] = [rnd, class_round+1, self.made_requests[class_round],self.made_requests_accepted[class_round]]


    def increase_received_request(self, class_round):
        class_round -= 1
        self.received_requests[class_round] += 1

    def increase_received_request_accepted(self, class_round):
        class_round -= 1
        self.received_requests_accepted[class_round] += 1
