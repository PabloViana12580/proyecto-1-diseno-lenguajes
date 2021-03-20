"""
	Arbol de análisis sintáctico 

	Referencias: 

	-> libro sección 2.2.3 
	-> https://www.youtube.com/watch?v=kzDuHh6kolk
	-> https://ruslanspivak.com/lsbasi-part7/#:~:text=An%20abstract%20syntax%20tree%20(AST,the%20operands%20of%20that%20operator.
"""

from afn import AFN, EstadoAFN
from automata import EstadoAutomata

"""
	Clase para un nodo de un arbol de analisis sintáctico
"""
class Nodo:

	def convertir_afn(self, accept_id = 1):
		"""
			Convertir el nodo en un AFN

			Estado de aceptación por defecto es 1
		"""

		(initial, accept) = self.thompson()
		accept.accept = accept_id
		return NFA(initial)

	def _thompson(self):
		"""
			Función para la construcción de thompson
		"""

		raise NotImplementedError

"""
	Clase para definir un nodo que contiene cualquier simbolo del lenguaje
"""
class NodoSimbolo(Nodo):

	def __init__(self, symbol):
		super().__init__()
		self.symbol = symbol

	def thompson(self):
		#automaton_state1 = EstadoAutomata()
		#automaton_state2 = EstadoAutomata()

		initial = EstadoAFN()
		accept = EstadoAFN()
		initial.add_transition(self.symbol, accept)
		return (initial, accept)

	def __str__(self):
		return 'NodoSimbolo({})'.format(repr(self.symbol))

"""
	Clase para definir un nodo de cerradura Kleene
"""
class NodoKleene(Nodo):

	def __init__(self, operand):
		super().__init__()
		self.operand = operand

	def thompson(self, initial, accept):

		initial.add_transition(None, accept)
		accept.add_transition(None, initial)

		return (initial, accept)

	def __str__(self):
		return 'NodoKleene({})'.format(repr(self.operand))

"""
	Clase para cerradura positiva (+)
"""
class NodoPositivo(Nodo):

	def __init__(self, operand):
		super().__init__()
		self.operand = operand

	def thompson(self, initial, accept):

		accept.add_transition(None, initial)

		return (initial, accept)

	def __str__(self):
		return 'NodoPositivo({})'.format(repr(self.operand))

"""
	Clase para "al menos una vez" (?)
"""
class NodoInterrogacion(Nodo):

	def __init__(self, operand):
		super().__init__()
		self.operand = operand

	def thompson(self, initial, accept):

		accept.add_transition(None, initial)

		return (initial, accept)

	def __str__(self):
		return 'NodoInterrogacion({})'.format(repr(self.operand))

"""
	Clase para cerradura Or (|)
"""
class NodOr(Nodo):

	def __init__(self, *operands):

		super().__init__()

		if len(operands) < 2:
			raise ValueError('Se necesitan dos nodos hijos')

		self.operands = ()
		for nodo in operands:
			#Si hay otro OR en un nodo hijo, agregue sus operandos para el OR
			if isinstance(nodo, NodOr):
				self.operands += nodo.operands
			else:
				self.operands += (nodo,)

	def thompson(self):
		initial = EstadoAFN()
		accept = EstadoAFN()

		for nodo in self.operands:
			if nodo == "|":
				pass
			else:
				#Agregamos los las dos transiciones ephsilon que dicta el OR
				(initial_new, accept_new) = (nodo[0], nodo[1])
				initial.add_transition(None, initial_new)
				accept_new.add_transition(None, accept)
			
		return (initial, accept)

	def __str__(self):
		return 'Nodo OR ({})'.format(', '.join(repr(o) for o in self.operands))

"""
	Clase para concatenación
"""
class NodoConcatenacion(Nodo):

	def __init__(self, *operands):

		super().__init__()

		if len(operands) < 2:
			raise ValueError("se necesitan dos nodos para concatenarlos")

		self.operands = ()

		for nodo in operands:
			if isinstance(nodo, NodoConcatenacion):
				self.operands += nodo.operands
			else:
				self.operands += (nodo, )

	def thompson(self):

		(initial, accept) = self.operands[1]

		for i in range(1, len(self.operands)):
			(nxt_initial, nxt_accept) = self.operands[i]
			accept.add_transition(None, nxt_initial)
			accept = nxt_accept

		return (initial, accept)

	def __str__(self):
		return 'NodoConcatenacion ({})'.format(', '.join(repr(o) for o in self.operands))