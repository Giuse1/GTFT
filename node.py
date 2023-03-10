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
        # self.NAR = pd.DataFrame(columns=["round","class","made","made_accepted"])
        # self.df = df
        self.df = pd.DataFrame(columns=["round", "node", "session_class", "type", "accepted"])

    def get_psi(self, class_round):

        try:
            to_return = self.received_requests_accepted[class_round] / self.received_requests[class_round]
        except:
            to_return = 0
        return to_return

    def get_fi(self, class_round):
        try:
            to_return = self.made_requests_accepted[class_round] / self.made_requests[class_round]
        except:
            to_return = 0
        return to_return

    def increase_made_request(self, class_round, rnd):
        self.made_requests[class_round] += 1
        # self.NAR.loc[len(self.NAR)] = [rnd,class_round, self.made_requests[class_round],self.made_requests_accepted[class_round]]
        self.df.loc[len(self.df)] = [rnd, self.idx, class_round, "made", False]

    def increase_made_request_accepted(self, class_round,rnd):
        self.made_requests_accepted[class_round] += 1
        # self.NAR.loc[len(self.NAR)-1] = [rnd, class_round, self.made_requests[class_round],self.made_requests_accepted[class_round]]
        self.df.loc[len(self.df)-1] = [rnd, self.idx, class_round, "made", True]


    def increase_received_request(self, class_round, rnd):
        self.received_requests[class_round] += 1
        self.df.loc[len(self.df)] = [rnd, self.idx, class_round, "received", False]


    def increase_received_request_accepted(self, class_round, rnd):
        self.received_requests_accepted[class_round] += 1
        self.df.loc[len(self.df)-1] = [rnd, self.idx, class_round, "received", True]

    # def get_l(self, class_round):
    #
    #     print(no) # todo
    #
    #     return (self.made_requests_accepted[class_round]/self.made_requests[class_round])/ self.tau # (self.received_requests_accepted[class_round]/self.received_requests[class_round])
    #
