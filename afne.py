from automato import *
from afn import *

class AFNe(Automato):
    def __init__(self, sigma, Q, delta, q0, F):
        super().__init__(sigma, Q, delta, q0, F)
    
    def afne_to_afn(self):
        # M = (sigma, Q, delta, q0, F)
        sigma = self.sigma
        q0 = self.initial_state
        Q = [q0]
        delta = {} # self.program_function # delta = {"q0": [("a", "q1"), ("b", q2)], ...}
        F = []

        closure_e = {} # {"q0": [q1, q2, q3], "q1": [...]}
        closure_e_final = set() # estados que viraram finais

        def calculate_closure_e(state):
            if state in closure_e: return closure_e[state] # closure_e(q) ja foi calculado
            closure_e[state] = [state]

            if state not in self.program_function: return closure_e[state]

            transitions = self.program_function[state]

            for transition in transitions:
                if transition[0] == "e": # ("e", destination_state)
                    for reached_state in calculate_closure_e(transition[1]):
                        #if reached_state in self.final_states: closure_e_final.add(reached_state)
                        if reached_state in self.final_states: closure_e_final.add(state)
                        
                        closure_e[state].append(reached_state)
            
            return closure_e[state]

        for q in Q:
            q_delta = [] # transicoes de q
            closure_e_of_q = calculate_closure_e(q)
            for closure_state in closure_e_of_q:
                if closure_state in self.final_states and q != closure_state and q not in F:
                    F.append(q) # se q alcanca um estado final atraves de transicoes "e", ele tb sera final

                transitions = []

                if closure_state in self.program_function:
                    transitions = self.program_function[closure_state]

                for symbol in sigma:
                        
                    for i in range(len(transitions)-1,-1,-1):
                        if transitions[i][0] == symbol:
                            #q_delta.append(transitions[i])
                            
                            state = transitions[i][1]
                            
                            for closure_e_of_state in calculate_closure_e(state):
                                q_delta.append((symbol, closure_e_of_state))

                                if closure_e_of_state not in Q: Q.append(closure_e_of_state)

                                if closure_e_of_state not in F and (closure_e_of_state in closure_e_final or closure_e_of_state in self.final_states):
                                    F.append(closure_e_of_state)


        
            if len(q_delta) > 0:
                delta[q] = q_delta

        return AFN(sigma, Q, delta, q0, F)