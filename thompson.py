from shuntingyard import shuntingyard
from arbolsintactico import NodoSimbolo, NodoKleene, NodoPositivo, NodoInterrogacion, NodOr, NodoConcatenacion
from afn import EstadoAFN
""" Thompson's Construction """

symbols = {
	0: "?",
	1: "+",
	2: "*",
	3: "|",
	4: ".",
}


""" Compiles a postfix regular expression into an NFA """
def compile_nfa(pofix, DEBUG):
	nfaStack = []

	print("\nexpresión: ", pofix) 
	for c in pofix:
		if c == '?':
			nfa = nfaStack.pop()
			# Push new NFA to the stack
			newNFA = NodoInterrogacion(symbols[0])
			nfaStack.append(newNFA.thompson(nfa[0], nfa[1]))
			if DEBUG:
				print("despues de ? quedan: ",  len(nfaStack))
		elif c == '+':
			nfa = nfaStack.pop()
			# Push new NFA to the stack
			newNFA = NodoPositivo(symbols[1])
			nfaStack.append(newNFA.thompson(nfa[0], nfa[1]))
			if DEBUG:
				print("despues de + quedan: ", len(nfaStack))
		elif c == '*':
			nfa = nfaStack.pop()
			newNFA = NodoKleene(symbols[2])
			nfaStack.append(newNFA.thompson(nfa[0], nfa[1]))
			if DEBUG:
				print("despues de * quedan: ", len(nfaStack))
		elif c == '.':
			nfa1 = nfaStack.pop()
			nfa2 = nfaStack.pop()
			newNFA = NodoConcatenacion(symbols[4], nfa1, nfa2)
			nfaStack.append(newNFA.thompson())
			if DEBUG:
				print("despues de . quedan: ", len(nfaStack))
		elif c == '|':
			nfa1 = nfaStack.pop()
			nfa2 = nfaStack.pop()
			newNFA = NodOr(symbols[3], nfa1, nfa2)
			nfaStack.append(newNFA.thompson())
			if DEBUG:
				print("despues de | quedan: ", len(nfaStack))
		else:
			# Push new NFA to the stack
			newNFA = NodoSimbolo(c)
			nfaStack.append(newNFA.thompson())
			if DEBUG:
				print("despues de char quedan: ", len(nfaStack))

	# NFA stack should only have a single NFA on it at this point
	return nfaStack.pop()

class state: 
    label = None
    edge1 = None
    edge2 = None


# An NFA is represented by it's initial and accept states
class nfa:
    initial = None
    accept = None

    # 'self' represents current instance of the class - similar to 'this'
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

""" Compiles a postfix regular expression into an NFA """
def compile_string(pofix):
    nfaStack = []

    for c in pofix:
        if c == '?':
            # Pop a single NFA from the stack
            nfa1 = nfaStack.pop()

            # Create new initial and accept states
            initial = state()
            accept = state()

            # Join the new initial state to nfa1's initial state and the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept

            # Make the accept state equal to the the NFA's accept state
            nfa1.accept.edge1 = accept

            # Push new NFA to the stack
            newNFA = nfa(initial, accept)
            nfaStack.append(newNFA)
        elif c == '+':
            # Pop a single NFA from the stack
            nfa1 = nfaStack.pop()

            # Create new initial and accept states
            initial = state()
            accept = state()

            # Make the accept edge 1 and edge 2 of the NFA equal to the initial state of the NFA
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept

            # Push new NFA to the stack
            newNFA = nfa(initial, accept)
            nfaStack.append(newNFA)
        elif c == '*':
            # Pop a single NFA from the stack
            nfa1 = nfaStack.pop() 

            # Create new initial and accept states
            initial = state()
            accept = state()

            # Join the new initial state to nfa1's initial state and the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept

            # Join the old accept state to the new accept state and nfa1's initial state
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept

            # Push new NFA to the stack
            newNFA = nfa(initial, accept)
            nfaStack.append(newNFA)
        elif c == '.':
            # Pop two NFAs off the stack
            nfa2 = nfaStack.pop() 
            nfa1 = nfaStack.pop()

            # Connect first NFA's accept state to the second's initial
            nfa1.accept.edge1 = nfa2.initial

            # Push new NFA to the stack
            newNFA = nfa(nfa1.initial, nfa2.accept)
            nfaStack.append(newNFA)
        elif c == '|':
            # Pop two NFAs off the stack
            nfa2 = nfaStack.pop() 
            nfa1 = nfaStack.pop()

            # Create a new initial state, connect it to initial states
            # of the two NFAs popped from the stack
            initial = state()

            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial

            # Create a new accept state, connecting the accept states
            # of the two NFAs popped from the stack to the new state
            accept = state()

            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept

            # Push new NFA to the stack
            newNFA = nfa(initial, accept)
            nfaStack.append(newNFA)
        else:
            # Create new initial and accept states
            accept = state()
            initial = state()

            # Join the initial state and the accept state using an arrow labelled 'c'
            initial.label = c 
            initial.edge1 = accept 

            # Push new NFA to the stack
            newNFA = nfa(initial, accept)
            nfaStack.append(newNFA)
    
    # NFA stack should only have a single NFA on it at this point
    return nfaStack.pop()

""" Return the set of states that can be reached from a state following
    'e' arrows """
def followArrowE(state):
    # Create a new set, with each state as it's only member
    states = set()
    states.add(state)

    # Check if state has arrows labelled 'e' from it
    if state.label is None:
        # Check if edge1 is a state
        if state.edge1 is not None:
            # If there's an edge1, follow it 
            states |= followArrowE(state.edge1)
        # Check if edge2 is a state
        if state.edge2 is not None:
            # If there's an edge2, follow it
            states |= followArrowE(state.edge2)

    # Return the set of states
    return states

""" Matches string to infix regular expression """
def match(infix, string):
    # Shunt and compile the regular expression
    postfix = shuntingyard(infix, False)
    nfa = compile_string(postfix)

    # The current set of states and the next set of states
    currentState = set()
    nextState = set()

    # Add the initial state to the current set of states
    currentState |= followArrowE(nfa.initial)

    # Loop through each character in the string
    for s in string:
        # Loop through current set of states
        for c in currentState:
            # Check if that state is labelled 's'
            if c.label == s:
                # Add edge1 state to the next set of states
                nextState |= followArrowE(c.edge1)

        # Set currentState to next and clear out nextState
        currentState = nextState
        nextState = set()
    
    # Check if the accept state is in the current set of states
    return(nfa.accept in currentState)
