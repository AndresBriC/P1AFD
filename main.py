import re
import csv

tokenTable = [] #Contiene la tabla con los caracteres y tipos
counter = 0

#Separa el texto a partir del = y elimina los espacios de la expresion
def stringSplitter(txt):
    beginning = "" #String del inicio hasta el =
    end = "" #String despues del =
    splitString = [] #Lista que contiene el las mitades separadas
    postEqual = False #Para checar lo que va despues del =

    #Va checando toda la string para ver si esta antes o despues del =
    for index, character in enumerate(txt):

        #Separa las strings si es antes o despues la asignacion
        if character != "=" and postEqual == False: #Caracteres antes del =
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
    
    """ if postEqual == False: #Si no se encontro un =
        print("No hay operador de asignacion") """

    #Agrega ambas partes a una lista
    splitString.append(beginning)
    splitString.append(end)

    return splitString

#Hace el desglose del string hasta el operador de asignacion
def lexerAritmeticoBeginning(txt):
    begSpace = False
    global tokenTable
    global counter

    for index, character in enumerate(txt): #Enumerate() se usa para poder tener el indice y el caracter
        counter += 1

        #Checa si hay un operador de asignacion
        if index == len(txt)-1 and character == "=": #Si el ultimo caracter es un =
            tokenTable.append(['', character, 'Asignación',counter])
        elif index == len(txt)-1 and character != "=": #Si el ultimo caracter no es un =
            print("No hay operador de Asignación")
        elif index != len(txt)-1 and character == "/" and txt[index+1] == "/": #Si detecta un comentario, deja de analizar el resto
            tokenTable.append(['', '//','Comentario',counter])
            break
        
        if character == " " and begSpace == False: #Ignora los espacios del principio
            continue
        elif character != " " and begSpace == False: #Aqui se encuentra algo despues de los espacios del principio, solo puede ser letra
            begSpace = True
            if re.search("[a-zA-Z]", character) != None: #Si es una letra
                tokenTable.append(['', character, 'Variable', counter])
            else: #Si no es letra, manda error y deja de leer la string
                tokenTable.append(['', character, 'Error, primer caracter diferente a una letra', counter])
        
        if index != len(txt)-1: #Para caracteres antes del ultimo
            if character == " " and begSpace == True and (txt[index+1] == " " or txt[index+1] == "="): #Si el actual es espacio y el sig. es espacio o igual
                continue
            elif character == " " and begSpace == True and (txt[index+1] != " " or txt[index+1] != "="):
                tokenTable.append(['', character, 'Error, espacio dentro de la variable o variable sin asignación', counter])


def lexerAritmeticoEnd(txt):
    #Aqui pondria mi lexer para la expresion... SI TUVIERA UNO
    opSpace = False #Checa si es un espacio despues de un operador

    if len(txt) == 0: #Si le pasan "end" vacio
        print("No hay operador de asignacion")
    print("Lexer end")

#Abre el texto con los casos de prueba
testsFile = open('P1_pruebas_.txt', "r")

#Lee cada linea del archivo
for line in testsFile:
    txt = line

    #Testing
    twoParts = stringSplitter(txt) #Contiene el string con las partes separadas por el =
    beginning = twoParts[0]
    end = twoParts[1]
    #print(twoParts)
    print("First part: " + beginning)
    if end == "":
        print("Second part: not found")
    else:
        print("Second part: " + end)

    #Agrega los resultados de la tabla del lexer a la tabla en general
    tokenTable.append([beginning+end,'','',counter])
    lexerAritmeticoBeginning(beginning)
    lexerAritmeticoEnd(end)

    print("______________________________________________________________________________________\n")

testsFile.close()

with open('tokenTable.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Expresión","Token","Type","Index"])
    writer.writerows(tokenTable)