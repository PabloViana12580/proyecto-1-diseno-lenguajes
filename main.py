"""
Universidad del Valle de Guatemala 
Diseño de lenguajes de programación 1
Catedrático: Bidkar Pojoy 
Pablo Viana - 16091

o Implementación de algoritmo de Construcción de Thompsono
o Implementación de algoritmo de Construcción de Subconjuntoso
o Implementación de algoritmo de Construcción de AFD dada una expresión regular r.
o Implementación de simulación de un AFNoImplementación de simulación de un AFD
"""


from shuntingyard import shuntingyard
from thompson import compile_nfa, compile_string, match
from afn import AFN
from graphviz import Source, render
from contextlib import redirect_stdout
import time

DEBUG = False


def validate_expr(expr):

	operators = ["+", "|", "*", "?"]
	err = []

	cn_1 = 0
	cn_2 = 0

	for i in range(len(expr) - 1):
		if expr[i] == "(":
			cn_1 += 1
		elif expr[i] in operators and expr[i+1] in operators:
				print("dos operadores juntos")
				return False

	for n in expr:
		if n == ")":
			cn_2 += 1

	if cn_1 == cn_2:
		pass
	else:
		print("Falta un parentesis")
		return False



if __name__ == '__main__':

	flag = True
	options = [1,2,3,4,5,6]

	while(flag):
		second_flag = False
		print("\n------------------------ IMPLEMENTACIÓN DE ALGORITMOS ------------------------")
		print("		(1) Construcción McNaughton–Yamada–Thompson")
		print("		(2) Construcción de Subconjuntos")
		print("		(3) Construcción directa de Autómata Finito Determinista")
		print("		(4) Minimización")
		print("		(5) Ver grafo")
		print("		(6) Salir")

		try:
			choice = int(input("Escoja una opción: "))
			if choice in options:
				second_flag = True
			else:
				print("\nNúmero no esta en las opciones\n")
		except ValueError as e:
			print("\nSolo números\n")

		if second_flag:
			if choice == 1:
				#Pedimos a usuario la expresion regular
				expresion_regular = input("Expresion regular: ")

				if validate_expr(expresion_regular) == False:
					break;

				#Pedimos a usuario palabra a evaluar
				palabra = input("Palabra: ")
				postfix = shuntingyard(expresion_regular, DEBUG)
				print("\n ******** INICIANDO CONSTRUCCIÓN THOMPSON ********\n")
				start = time.time()
				nfa = compile_nfa(postfix, DEBUG)
				print("---- %s segundos de ejecución ----\n" % (time.time() - start))
				nfa_real = AFN(nfa[0])
				with open('afn.gv', 'w', encoding="utf-8") as f:
					with redirect_stdout(f):
						nfa_real.print_graphviz()

				print("---- Se ha guardado el grafo ----\n")

				# Validamos si la palabra pertenece o no al vocabulario
				respuesta = match(expresion_regular, palabra)

				if respuesta == True:
					print("¡la palabra pertenece al lenguaje!")
				else:
					print("la palabra no pertenece al lenguaje")

			elif choice == 2:
				#Pedimos a usuario la expresion regular
				expresion_regular = input("Expresion regular: ")

				if validate_expr(expresion_regular) == False:
					break;

				#Pedimos a usuario palabra a evaluar
				palabra = input("Palabra: ")
				postfix = shuntingyard(expresion_regular, DEBUG)
				print("\n ******** INICIANDO CONSTRUCCIÓN THOMPSON ********\n")
				start = time.time()
				nfa = compile_nfa(postfix, DEBUG)
				print("---- %s segundos de ejecución ----\n" % (time.time() - start))
				nfa_real = AFN(nfa[0])
				print("\n ******** INICIANDO SUBCONJUNTOS ********\n")
				start2 = time.time()
				dfa = nfa_real.to_dfa()
				print("---- %s segundos de ejecución ----\n" % (time.time() - start2))
				with open('dfa_subconjuntos.gv', 'w', encoding="utf-8") as f:
					with redirect_stdout(f):
						dfa.print_graphviz()

				print("---- Se ha guardado el grafo ----\n")
			elif choice == 3: 
				print("Aún no implementado")
			elif choice == 4:
				#Pedimos a usuario la expresion regular
				expresion_regular = input("Expresion regular: ")

				if validate_expr(expresion_regular) == False:
					break;

				#Pedimos a usuario palabra a evaluar
				palabra = input("Palabra: ")
				postfix = shuntingyard(expresion_regular, DEBUG)
				print("\n ******** INICIANDO CONSTRUCCIÓN THOMPSON ********\n")
				start = time.time()
				nfa = compile_nfa(postfix, DEBUG)
				print("---- %s segundos de ejecución ----\n" % (time.time() - start))
				nfa_real = AFN(nfa[0])
				print("\n ******** INICIANDO SUBCONJUNTOS ********\n")
				start2 = time.time()
				dfa = nfa_real.to_dfa()
				print("---- %s segundos de ejecución ----\n" % (time.time() - start2))
				print("\n ******** INICIANDO MINIMIZACIÓN ********\n")
				start3 = time.time()
				mini = dfa.minimize()
				print("---- %s segundos de ejecución ----\n" % (time.time() - start3))
				with open('mini.gv', 'w', encoding="utf-8") as f:
					with redirect_stdout(f):
						mini.print_graphviz()
			elif choice == 5:
				filename = input("nombre del archivo: ")

				src = Source.from_file(filename)
				src.render('graph.gv', view=True)
			elif choice == 6:
				flag = False
				second_flag = False
