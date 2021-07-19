import re


txt = " n_1234  =400 +  2 0  " #String de pruba (Reemplazar con la lectura del archivo txt)

#Separa el texto a partir del = y elimina los espacios de la expresion
def stringSplitter(txt):
    beginning = "" #String del inicio hasta el =
    end = "" #String despues del =
    splitString = [] #Lista que contiene el las mitades separadas
    postEqual = False #Para checar lo que va despues del =

    #Va checando toda la string para ver si esta antes o despues del =
    for character in txt:
        if character == " " and postEqual == False: #Si hay un espacio en la variable, lo agrega para analizar
            beginning += character
        elif character == " " and postEqual == True: #Si hay un espacio en la expresion, lo ignora
            continue
        elif character != "=" and postEqual == False: #Caracteres antes del =
            beginning += character
        elif character == "=" and postEqual == False: #Encuentra el =
            beginning += character
            postEqual = True
        elif character != "=" and postEqual == True: #Caracteres despues del =
            end += character
        elif character == "=" and postEqual == True: #Error de segundo =
            print("Se econtró un segundo operador de asignación")
            end += character
            break
    
    if postEqual == False: #Si no se encontro un =
        print("No hay operador de asignacion")

    #Agrega ambas partes a una lista
    splitString.append(beginning)
    splitString.append(end)

    return splitString

#Hace el desglose del string hasta el operador de asignacion
def lexerAritmeticoBeginning(txt):
    begSpace = False

    #La idea para checar los espacios es que si es un espacio del principio (antes de cualquier otro caracter), es valido
    #, pero después de eso, debe checar el siguiente caracter, si es espacio o igual, es válido, si no, no

    for index, character in enumerate(txt):
        if index == len(txt)-1 and character == "=": #Si el ultimo caracter es un =
            #Reportar el =
            print(character + " asignación")
        elif index == len(txt)-1 and character != "=": #Si el ultimo caracter no es un =
            print("No hay operador de asignación")
        elif character != " " and begSpace == False:
            begSpace = True
        elif character == " " and begSpace == True:
            print("Space at invalid position")


def lexerAritmeticoEnd(txt):
    #Aqui pondria mi lexer para la expresion... SI TUVIERA UNO

    if len(txt) == 0: #Si le pasan "end" vacio
        print("No hay operador de asignacion")
    print("Lexer end")

#Testing
twoParts = stringSplitter(txt) #Contiene el string con las partes separadas por el =
beginning = twoParts[0]
end = twoParts[1]

lexerAritmeticoBeginning(beginning)

#print(twoParts)
print("First part: " + beginning)
print("Second part: " + end)