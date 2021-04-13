from automato import *

class AFDmin(Automato):
    def __init__(self, sigma, Q, delta, q0, F):
        super().__init__(sigma, Q, delta, q0, F)
    
    def accepted(self, w):
        current_state = self.initial_state
        #print()
        #self.debug_print()

        for symbol in w:
            if current_state not in self.program_function: continue

            for transition in self.program_function[current_state]:
                if transition[0] == symbol:
                    current_state = transition[1]
                    break
        
        if current_state in self.final_states:
            return True # Accept
        
        return False