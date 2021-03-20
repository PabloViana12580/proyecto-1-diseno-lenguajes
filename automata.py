"""
Un autómata finito

Referencias: https://www.python-course.eu/finite_state_machine.php
"""

import sys

class Automata:
	
	def __init__(self, initial):
		"""
			constructor de la clase para definir un autómata de estados finito
		"""
		self.initial = initial
		self.num_states = self.assign_number_state(self.initial, 0)

	def assign_number_state(self, state, nxt_num):
		"""
			Asignar un número a todos los estados alcanzables dado un estado inicial

			return -> el número de estados en el automata/nodos en el árbol
		"""

		#Si no tiene número le asignamos
		if state.number is None:
			state.number = nxt_num
			nxt_num += 1
			# asignele número al siguiente estado
			for (symbol, target) in state.all_transitions():
				nxt_num = self.assign_number_state(target, nxt_num)
		return nxt_num

	def print_graphviz(self):
		"""Imprimir al automara para ser graficado con graphviz dot rendering"""

		print('digraph {} {{'.format(type(self).__name__))
		print('    edge [dir="back"];')
		print('    rankdir = RL;')
		print('    I [style = invis];')

		print('    I -> S{};'.format(self.initial.number))
		
		self.initial._print_graphviz(set())

		print('}')

"""
Clase para definir un estado en un automata de estados fínito
"""
class EstadoAutomata:

	def __init__(self, accept=None):
		"""
		Constructor de la clase de estados
		"""
		self.accept = accept
		self.transitions = {}
		self.number = None

	def _ensure_not_numbered(self):
		"""
			Función para indicar que el estado ya esta numerado
		"""
		if self.number is not None:
			raise ValueError('Estado previamente numerado')

	def all_transitions():
		"""
			Función para mostrar todas las transiciones se usa excepción, función para heredar
		"""

		raise NotImplementedError

	def add_transition(self, symbol, to):
		"""
			FUnción para añadir una transición al estado, se hereda
		"""

		raise NotImplementedError

	def _print_graphviz(self, seen):
		if self in seen:
			return
		seen.add(self)

		if self.accept:
			subscript = '{},{}'.format(self.number, self.accept)
		else:
			subscript = self.number

		print('    S{} [label = <s<sub>{}</sub>>, shape = circle'.format(self.number, subscript),
			  end='')

		if self.accept:
			print(', peripheries = 2', end='')
		print('];')

		for (symbol, target) in self.all_transitions():
			target._print_graphviz(seen)
			if symbol is None:
				label = '\u03b5'  # Lower case epsilon
			else:
				label = repr(symbol).replace('\\', '\\\\')  # Escape slashes
			print('    S{} -> S{} [label = "{}"];'.format(self.number, target.number, label))