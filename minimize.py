"""
	Clase para la minimización de un autómara finito determinista

	REFERENCIAS: 

	-> http://www-igm.univ-mlv.fr/~berstel/Exposes/2009-06-08MinimisationLiege.pdf
	-> https://github.com/osandov/pylex
	-> https://mathematica.stackexchange.com/questions/191205/hopcrofts-algorithm-for-minimization-of-deterministic-finite-state-automaton
"""

from afd import AFD, EstadoAFD

# Numero máximo de catacteres
NUM_SYMBOLS = 0x100
# definimos el alfabeto
SIGMA = ''.join(chr(c) for c in range(NUM_SYMBOLS))

class Minimize():

	def __init__(self, afd):
		self.initial = afd.initial

	def __call__(self):
		#Dividimos en estados de aceptación y no aceptación
		T = self.initial_partition()

		#Inicializamos conjunto
		self.P = set()

		#Iterar hasta un punto fijo
		while self.P != T:
			self.P = T
			T = set()

			for p in self.P:
				T |= self.split(p)

		afd_states = {}

		def aux(subset):
			state = subset
			afd_state = EstadoAFD(state.accept)
			afd_states[subset] = afd_state

			for (symbol, target) in state.transitions.items():
				target_subset = self.partition_containing(target)

				if target_subset not in afd_states:
					aux(target_subset)
				afd_state.add_transition(symbol, afd_states[target_subset])

			return afd_state

		initial_subset = self.partition_containing(self.initial)
		return AFD(aux(initial_subset))

	def initial_partition(self):
		"""
			Hace una partición en el conjunto de estados del AFD entre los que son estados de aceptación y los que no
		"""

		from collections import defaultdict

		T = defaultdict(lambda: set())

		def aux(state):
			T[state.accept].add(state)
			for target in state.transitions.values():
				if target not in set.union(*T.values()):
					while target:
						aux(target.pop())

		aux(self.initial)

		return set(frozenset(s) for s in T.values())

	def split(self, S):
		"""Attempt to split a set of DFA states based on their transitions to
		other subsets in the partition.

		"""

		def splits(c):

			for i in S:
				s1 = set()
				s2 = set()

				expected = i.transitions.get(c, None)
				expected = self.partition_containing(expected)
				for j in S:
					actual = j.transitions.get(c, set())
					actual = self.partition_containing(actual)
					if actual == expected:
						s1.add(j)
					else:
						s2.add(j)

				if s1 and s2:
					return {frozenset(s1), frozenset(s2)}

		for c in SIGMA:
			split = splits(c)
			if split:
				return split
		else:
			return {S}

	def partition_containing(self, state):
		try:
			for p in self.P:
				if state in p:
					return next(iter(p))
		except StopIteration:
			return None