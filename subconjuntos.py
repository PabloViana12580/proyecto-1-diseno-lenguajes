"""
	Clase para implementar la transformación de un afn a afd por medio del algoritmo de subconjuntos

	Referencias:

	-> https://cs.uwaterloo.ca/~eblais/cs365/docs/automata/rabinscott/
	-> https://www.geeksforgeeks.org/conversion-from-nfa-to-dfa/
"""

from afd import AFD, EstadoAFD
from afn import AFN, EstadoAFN

# Numero máximo de catacteres
NUM_SYMBOLS = 0x100
# definimos el alfabeto
SIGMA = ''.join(chr(c) for c in range(NUM_SYMBOLS))

class Subconjuntos():

	def __init__(self, AFN):
		"""
			Inicializamos el algoritmo con un AFN como entrada
		"""

		self.initial = AFN.initial

	def __call__(self):

		#Configuración inicial
		q0 = self.initial.e_closure()

		Q = {q0: self.configuration_to_AFD_state(q0)}

		wordlist = [q0]
		while wordlist:
			q = wordlist.pop()

			for c in SIGMA:
				t = self.delta_closure(q, c)

				if t:
					try:
						AFD_state = Q[t]
					except:
						AFD_state = self.configuration_to_AFD_state(t)
						Q[t] = AFD_state
						wordlist.append(t)

					Q[q].add_transition(c, AFD_state)

		return AFD(Q[q0])

	def delta_closure(self, q, c):

		delta_closure = set()
		for state in q:
			for target in state.transitions.get(c, set()):
				delta_closure |= target.e_closure()

		return frozenset(delta_closure)

	def configuration_to_AFD_state(self, q):
		try:
			accept = min(state.accept for state in q if state.accept)
		except ValueError:
			accept = None

		return EstadoAFN(accept)