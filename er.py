import sys
from afne import *
from afn import *
from afd import *
from afd_min import *

def erToAFNe(er, state_index = 0):
    # M = (sigma, Q, delta, q0, F)
    sigma = []
    q0 = "q" + "0" + str(state_index)
    Q = [q0]
    delta = {} # delta = {"q0": [("a", "q1"), ("b", q2)], ...}
    F = []

    er = er.replace(" ", "")
    if len(er) == 0:
        return AFNe(sigma, Q, delta, q0, F)
    elif len(er) == 1 and er == "e":
        F.append(q0)
        return AFNe(sigma, Q, delta, q0, F)
    elif len(er) == 1:
        sigma.append(er)
        qf = "q" + "f" + str(state_index)
        Q.append(qf)
        F.append(qf)
        delta = {q0: [(er, qf)]}
        return AFNe(sigma, Q, delta, q0, F)

    def process_er(er):
        split_at = None
        count = 1 # contador de operadores
        er = er[2:-1] # remove o op e os parentesis do inicio e fim
        for i in range(len(er)-1):
            if er[i] in ["+", "."]:
                count += 1
            elif er[i] == ",":
                count -= 1
            if count == 0:
                split_at = i
                break

        er1, er2 = er[:split_at], er[split_at+1:]
        return er1, er2
    
    def add_symbols(auto1, auto2):
        for symbol in auto1.sigma:
            if symbol not in sigma:
                sigma.append(symbol)
        
        if auto2 != None:
            for symbol in auto2.sigma:
                if symbol not in sigma:
                    sigma.append(symbol)

    c = er[0]
    if c == "+":
        er1, er2 = process_er(er)
        auto1 = erToAFNe(er1, state_index = state_index + 1)
        #print(f"erToAFNe: {er1}")
        #auto1.debug_print()

        auto2 = erToAFNe(er2, state_index = state_index + 2)
        #print(f"erToAFNe: {er2}")
        #auto2.debug_print()

        # Construindo Alfabeto
        add_symbols(auto1, auto2)

        # Construindo a função programa
        delta[q0] = [("e", auto1.initial_state), ("e", auto2.initial_state)]

        for state in auto1.states:
            if state not in Q:
                Q.append(state)

            if state in auto1.program_function:
                delta[state] = auto1.program_function[state]
        
        for state in auto2.states:
            if state not in Q:
                Q.append(state)

            if state in auto2.program_function:
                delta[state] = auto2.program_function[state]
        
        qf = "q" + "f" + str(state_index)

        delta[auto1.final_states[0]] = [("e", qf)]
        delta[auto2.final_states[0]] = [("e", qf)]

        F.append(qf)
        Q.append(qf)

    elif c == "*":
        auto = erToAFNe(er[2:-1], state_index = state_index + 1)
        #print(f"erToAFNe: {er[2:-1]}")
        #auto.debug_print()

        # Construindo Alfabeto
        add_symbols(auto, None)

        # Construindo a função programa
        delta[q0] = [("e", auto.initial_state)]

        for state in auto.states:
            if state not in Q:
                Q.append(state)

            if state in auto.program_function:
                delta[state] = auto.program_function[state]
        
        qf = "q" + "f" + str(state_index)

        delta[q0].append(("e", qf))
        if auto.final_states[0] not in delta:
            delta[auto.final_states[0]] = [("e", auto.initial_state), ("e", qf)]
        else:
            delta[auto.final_states[0]].append(("e", auto.initial_state))
            delta[auto.final_states[0]].append(("e", qf))

        Q.append(qf)
        F.append(qf)

    elif c == ".":
        er1, er2 = process_er(er)
        auto1 = erToAFNe(er1, state_index = state_index)
        #print(f"erToAFNe: {er1}")
        #auto1.debug_print()

        #auto2 = erToAFNe(er2, state_index = len(auto1.states) + 1)
        auto2 = erToAFNe(er2, state_index = state_index + 1)
        #print(f"erToAFNe: {er2}")
        #auto2.debug_print()

        # Construindo Alfabeto
        add_symbols(auto1, auto2)

        # Construindo a função programa
        delta[q0] = auto1.program_function[auto1.initial_state]

        for state in auto1.states[1:]: # o estado inicial ja foi inserido
            if state not in Q:
                Q.append(state)

            if state in auto1.program_function:
                delta[state] = auto1.program_function[state]

        delta[auto1.final_states[0]] = [("e", auto2.initial_state)]

        for state in auto2.states:
            if state not in Q:
                Q.append(state)

            if state in auto2.program_function:
                delta[state] = auto2.program_function[state]

        F = auto2.final_states

    return AFNe(sigma, Q, delta, q0, F)

def afneToAFN(automato):
    if not isinstance(automato, AFNe): return None

    return automato.afne_to_afn() # return afn

def afnToAFD(automato):
    if not isinstance(automato, AFN): return None

    return automato.afn_to_afd() # return afd

def afdToAFDmin(automato):
    if not isinstance(automato, AFD): return None

    return automato.afd_to_afd_min() # return afd_min

def match(er, w):
    return afdToAFDmin(afnToAFD(afneToAFN(erToAFNe(er)))).accepted(w)

def match_print(er, w):
    if match(er, w):
        print(f"match {er}, {w} == OK")
    else:
        print(f"match {er}, {w} == Not OK")

if __name__ == '__main__':
    def help():
        print("################### HINT ####################")
        print("# For one Expression Use the command bellow #")
        print("# python er.py \"<expression>\" \"<match>\"     #")
        print("#                                           #")
        print("# For Several Expressions use a file        #")
        print("# python er.py -f <filename> \"<match>\"    #")
        print("#############################################")
        
        sys.exit(1)

    args = sys.argv[1:]

    # Test for a validy entry
    if args[0] != "-f" and len(args) != 2:
        help()
    elif args[0] == "-f" and len(args) != 3:
        help()

    # only one expression
    if args[0] != "-f":
        er = args[0] # regular expression
        w = args[1] # word

        match_print(er, w)

    # expression from file
    else:
        filename = args[1]
        w = args[2] # word

        file = open(filename, "r")
        
        lines = file.readlines()

        for er in lines:
            er = er.replace("\n", "")
            match_print(er, w)
        
        file.close()
