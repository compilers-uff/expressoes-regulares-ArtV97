from automato import *
from afd import *

class AFN(Automato):
    def __init__(self, sigma, Q, delta, q0, F):
        super().__init__(sigma, Q, delta, q0, F)
    
    def afn_to_afd(self):
        # M = (sigma, Q, delta, q0, F)
        sigma = self.sigma
        q0 = self.initial_state
        Q = [q0]
        delta = {} # self.program_function # delta = {"q0": [("a", "q1"), ("b", q2)], ...}
        F = []

        def reached_states_from_q(ql, symbol):
            reached_states = []
            if ql not in self.program_function: return reached_states

            for transition in self.program_function[ql]:
                if transition[0] == symbol and transition[1] not in reached_states:
                    reached_states.append(transition[1])
            
            reached_states.sort()

            return reached_states

        # calculando os estados e delta do AFD
        for q in Q:
            if q not in delta: delta[q] = []

            list_q = q.split(",")
            for symbol in sigma:
                reached_states = [] # estados alcancados por simbolo
                for ql in list_q:
                    if ql in self.final_states and ql not in F: F.append(ql)

                    for reached_state in reached_states_from_q(ql, symbol):
                        if reached_state not in reached_states:
                            reached_states.append(reached_state)
                

                new_state = "" # possivel novo estado
                for state in reached_states:
                    new_state += state + ","
                new_state = new_state[:-1]

                if new_state != "":
                    delta[q].append((symbol, new_state))
                
                    if new_state not in Q: Q.append(new_state)

            # nenhuma transicao encontrada para o estado q
            if len(delta[q]) == 0:
                del delta[q]

        return AFD(sigma, Q, delta, q0, F)
        
                

            