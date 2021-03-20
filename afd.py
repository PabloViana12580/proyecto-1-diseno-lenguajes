"""
	Clase para un autómata finito determinista

	Referencias: 

	-> https://medium.com/swlh/automata-theory-in-python-part-1-deterministic-finite-automata-95d7c4a711f5
	-> https://github.com/caleb531/automata
"""

from automata import Automata, EstadoAutomata

class AFD(Automata):

	def __init__(self, initial):
		super().__init__(initial)

	def minimize(self):
		"""
			Función para minimizar un AFD
		"""

		from minimize import Minimize

		return Minimize(self)()

class EstadoAFD(EstadoAutomata):
	"""
		Un estado en un autómata finito determinista

		Solo una transición por simbolo y no se valen ephsilons
	"""

	def __init__(self, accept):
		super().__init__(accept)

	def _all_transitions(self):
		"""
			Función para obtener todas las transiciones como un conjunto
		"""
		return set(self.transitions.items())

	def add_transition(self, symbol, nodo):
		"""
			Función para añadir una transición a este estado
		"""

		self._ensure_not_numbered()

		assert symbol is not None, 'Automata finito determinista no acepta transiciones ephsilon'
		assert symbol not in self.transitions, 'El estado ya tiene esta transición'
		self.transitions[symbol] = nodo

