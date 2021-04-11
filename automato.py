class Automato():
    
    def __init__(self, sigma, Q, delta, q0, F):
        self.sigma = sigma
        self.initial_state = q0
        self.states = Q
        self.program_function = delta
        self.final_states = F
    
    def debug_print(self):
        print("##### Automato #####")
        print(f"Sigma: {self.sigma}")
        print(f"Estado Inicial: {self.initial_state}")
        print(f"States: {self.states}")
        print(f"Delta: {self.program_function}")
        print(f"Estados Finais: {self.final_states}")
        print("####################")
        print()

