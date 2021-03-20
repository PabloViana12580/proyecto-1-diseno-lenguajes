"""
Un automata finito no-determinista

Referencias:

-> https://stackoverflow.com/questions/30551731/data-structure-in-python-for-nfa-regex
-> https://github.com/caleb531/automata/blob/master/automata/fa/nfa.py
"""

from automata import Automata, EstadoAutomata

class AFN(Automata):
	"""
		Clase para definir un AFN 
	"""

	def __init__(self, inital):
		# Llamamos a init de clase Automata 
		super().__init__(inital)

	def to_dfa(self):
		"""Convert this NFA to an equivalent DFA."""

		from subconjuntos import Subconjuntos
		return Subconjuntos(self)()

class EstadoAFN(EstadoAutomata):
	"""
		Un estado de un autómata finito no determinista
	"""

	def __init__(self, accept=None):
		super().__init__(accept)

	def all_transitions(self):
		#Inicializamos el conjunto de transiciones
		transitions = set()
		for symbol, targets in self.transitions.items():
			#union de conjuntos
			transitions |= {(symbol, target) for target in targets}
		return transitions

	def add_transition(self, symbol, state):
		"""
			Función para añadir una transición al estado
		"""

		self._ensure_not_numbered()

		try:
			self.transitions[symbol].add(state)
		except KeyError:
			self.transitions[symbol] = {state}

	def e_closure(self):
		"""
			Función para computar la cerradura ephsilon de este estado
		"""

		ephsilon = {self}
		stack = [self]
		while stack:
			state = stack.pop()
			for target in state.transitions.get(None, set()):
				if target not in ephsilon:
					ephsilon.add(target)
					stack.append(target)

		self.inmutable_ephsilon = frozenset(ephsilon)
		return self.inmutable_ephsilon
