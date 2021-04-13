from automato import *
from afd_min import *

class AFD(Automato):
    def __init__(self, sigma, Q, delta, q0, F):
        super().__init__(sigma, Q, delta, q0, F)
    
    def afd_to_afd_min(self):
        # M = (sigma, Q, delta, q0, F)
        sigma = self.sigma
        q0 = None
        Q = []
        delta = {} # self.program_function # delta = {"q0": [("a", "q1"), ("b", q2)], ...}
        F = []

        # checando se a funcao de transicao eh total
        is_total = True
        for q in self.states:
            if q not in self.program_function or len(self.program_function[q]) < len(self.sigma):
                is_total = False
                break
        
        # transforma em total
        if not is_total:
            self.states.append("d")
            
            for q in self.states:
                if q not in self.program_function: 
                    self.program_function[q] = []
                    
                    for s in self.sigma:
                        self.program_function[q].append((s, "d"))
                
                else:
                    transitions = self.program_function[q]

                    used_symbols = []
                    for transition in transitions:
                        used_symbols.append(transition[0])
                    
                    for s in self.sigma:
                        if s not in used_symbols:
                            self.program_function[q].append((s, "d"))




        # criando pares
        pairs = []

        for i in range(len(self.states)):
            q1 = self.states[i]
            for q2 in self.states[i+1:]:
                pairs.append({q1, q2})

        def transition(state, symbol):
            if state not in self.program_function: return None
            
            for transition in self.program_function[state]:
                if transition[0] == symbol:
                    return transition[1] # retorna o estado
        
        def mark_recursive(i, recursion_control = 0):
            if recursion_control > 40: return

            l = list_of_each_pair[i]
            for p in l:
                table[p] = False
                mark_recursive(p, recursion_control + 1)
        
        # criando a tabela
        table = [True] * len(pairs)

        # marcando os triviais
        for i, s in enumerate(pairs):
            k = list(s)
            if (k[0] in self.final_states and k[1] not in self.final_states) or (k[1] in self.final_states and k[0] not in self.final_states):
                table[i] = False

        # marcando estados não triviais
        list_of_each_pair = {i: [] for i in range(len(pairs))}
        for i, p in enumerate(pairs):
            if table[i]:
                l = list(p)
                qu = l[0]
                qv = l[1]
                for s in sigma:

                    pu = transition(qu, s)
                    pv = transition(qv, s)
                    
                    if pu == pv:
                        continue
                    else:
                        pu_pv_idx = pairs.index({pu, pv})
                        if table[pu_pv_idx]:
                            
                            if i not in list_of_each_pair[pu_pv_idx]:
                                list_of_each_pair[pu_pv_idx].append(i)
                                
                        else:
                            table[i] = False
                            mark_recursive(i)

        # construindo estados do AFDmin
        equiv_states = {}
        not_equiv_states = set(self.states) # estados que n tem equivalentes
        for i, p in enumerate(pairs):
            if table[i] == True:
                pair = list(p)
                pair.sort()

                not_equiv_states.discard(pair[0])
                not_equiv_states.discard(pair[1])
                
                if pair[0] not in equiv_states and pair[1] not in equiv_states:
                    equiv_states[pair[0]] = [pair[1]]
                elif pair[0] in equiv_states:
                    equiv_states[pair[0]].append(pair[1])
                else:
                    equiv_states[pair[1]].append(pair[0])
                
        equiv_states_delta = {}

        for q in self.states:
            if q in equiv_states:
                equiv_of_q = equiv_states[q]

                for q2 in equiv_of_q:
                    if q2 in equiv_states:
                        for q3 in equiv_states[q2]:
                            if q3 not in equiv_of_q:
                                equiv_of_q.append(q3)
                        
                        del equiv_states[q2]

                # usando um separador diferente do utilizado no AFNtoAFD
                new_state = q + "-"
                initial_state = False
                if q == self.initial_state: initial_state = True
                for q_equiv in equiv_of_q:
                    if q_equiv == self.initial_state: initial_state = True

                    new_state += q_equiv + "-"
                
                new_state = new_state[:-1] # remove ","

                final_state = False
                if q in self.final_states: final_state = True

                if initial_state: q0 = new_state
                if final_state: F.append(new_state)
                Q.append(new_state)

                # preparando para construir delta depois
                equiv_states_delta[q] = new_state
                for q_equiv in equiv_of_q:
                    equiv_states_delta[q_equiv] = new_state


        for q in not_equiv_states:
            Q.append(q)
            if q == self.initial_state: q0 = q
            if q in self.final_states: F.append(q)
        
        # construindo delta
        for q in Q:
            delta[q] = []

            q_aux = q
            if q not in self.states: # eh um estado novo
                q_aux = q.split("-")[0] # basta pegar o primeiro, pois sao equivalentes
            
            for s in sigma:
                state = transition(q_aux,s)

                if state == None: continue

                if state in equiv_states_delta:
                    delta[q].append((s, equiv_states_delta[state]))
                else:
                    delta[q].append((s, state))
                

        return AFDmin(sigma, Q, delta, q0, F)