"""
Shunting yard algorithm 

Para pasar una expresión infix_input a una postfix estableciendo precedencia de operadores

REFERENCIA: https://www.youtube.com/watch?v=cD6qkvOYL_o

"""

def shuntingyard(infix_input, debug):
    """
        Funcion para realizar algoritmo de shunting yard

        Parameters: infix_input - expresión regular en infix
    """

    #Establecemos los operadores y su precedencia
    precedencia_operadores = {'*': 40, '+': 30, '?': 20, '.': 10, '|': 1}

    #variable para output
    postfix = ""
    #stack para operadores
    stack = ""

    for c in infix_input:
        #Si encontramos un paréntesis izquierdo lo agregamos al stack
        if c == '(':
            stack = stack + c

            if debug:
                print("stack: ", stack)
        elif c == ')':
            #Recorremos el stack hasta encontrar el parentesis izquierdo
            while stack[-1] != '(':
                #hacemos pop de todos los elementos del stack que no son el "("
                postfix = postfix + stack[-1]
                stack = stack[:-1]

            if debug:
                print("stack: ", stack)
            # Removemos "(" del stack
            stack = stack[:-1]

            if debug:
                print("stack: ", stack)
        #Si encontramos un operador
        elif c in precedencia_operadores:
            #Mientras aún tenga elementos el stack y la precedencia de "c" sea menor que la del operador en stack
            while stack and precedencia_operadores.get(c, 0) <= precedencia_operadores.get(stack[-1], 0):
                #agregamso todo el stack al output menos el último elemento
                postfix = postfix + stack[-1]
                #Dismuimos stack en 1
                stack = stack[:-1]
            #Agregamos operados al stack
            stack = stack + c

            if debug:
                print("stack: ", stack)
        #Todo lo demás agreguelo al stack
        else:
            postfix = postfix + c

            if debug:
                print("postfix: ", postfix)

    #Si todavía queda algo en el stack 
    while stack:
        #Agregarlo al output
        postfix = postfix + stack[-1]
        #reducir stack para salir del while
        stack = stack[:-1]
    
    #Return expresión en postfix
    return postfix