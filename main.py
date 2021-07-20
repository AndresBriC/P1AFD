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

    #Agrega ambas partes a una lista
    splitString.append(beginning)
    splitString.append(end)

    return splitString

#Hace el desglose del string hasta el operador de asignacion
def lexerAritmeticoBeginning(txt):
    begSpace = False #Checa si hay espacios antes de la variable
    varSpace = False #Checa si hay espacios dentro de la variable
    varBegMark = 0 #Para concatenar la variable
    varEndMark = 0 #Para concatenar la variable
    varConcat = "" #Almacena la variable concatenada
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
                varBegMark = index #Marca el inicio de la concatenacion
                varEndMark = index
            else: #Si no es letra, manda error y deja de leer la string
                tokenTable.append(['', character, 'Error, primer caracter diferente a una letra', counter])
        elif character != " " and begSpace == True:
            
            if re.search("\w", character) != None: #Si es una letra, numero o _
                if varBegMark == varEndMark:
                    varEndMark = index
                else:
                    varEndMark = index #Marca el posible final de la concatenacion
            else: #Si no es letra, manda error y deja de leer la string
                if character == '=': #Si no es letra, numero o _, pero es =, lo ignora
                    continue
                else:
                    tokenTable.append(['', character, 'Error, caracter no valido para variable', counter])

        #Checa espacios
        if index != len(txt)-1: #Para caracteres antes del ultimo
            if character == " " and begSpace == True and (txt[index+1] == " " or txt[index+1] == "="): #Si el actual es espacio y el sig. es espacio o igual
                continue
            elif character == " " and begSpace == True and varSpace == False and (txt[index+1] != " " or txt[index+1] != "="):
                tokenTable.append(['', character, 'Error, espacio dentro de la variable o variable sin asignación', counter])
                varSpace = True
    
    varConcat = txt[varBegMark:varEndMark+1] #Hace el subtring de la variable sola (sin espacios)
    tokenTable.append(['', varConcat, 'Variable', counter])


def lexerAritmeticoEnd(txt):
    opSpace = False #Checa si es un espacio despues de un operador
    afterOp = False #Nota si hubo un operador antes
    parentesisAbreCounter = 0 #Para saber si se cierran todos lo parentesis
    parentesisCierraCounter = 0
    numBegMark = 0 #Para concatenar los numeros
    numEndMark = 0
    checkingNum = False
    numType = ""
    numHasPoint = False
    checkingVar = False
    varBegMark = 0
    varEndMark = 0
    global tokenTable
    global counter

    if len(txt) == 0: #Si le pasan "end" vacio
        tokenTable.append(['','','Error, no hay operador de asignacion', counter])
        print("No hay operador de asignacion")
    else: #Si el end no esta vacio
        for index, character in enumerate(txt): #Enumerate() se usa para poder tener el indice y el caracter
            counter += 1
            
            #Analisis de operadores
            if re.search("[+]|[-]|[*]|[/]|[^]", character) != None and afterOp == False:
                afterOp = True
                if character == '-':
                    tokenTable.append(['',])



            #Analisis de parentesis
            if parentesisCierraCounter > parentesisAbreCounter:
                tokenTable.append(['',')','Error de paréntesis, cierra pero no abre', counter])
                break
            if character == '(':
                parentesisAbreCounter += 1
            elif character == ')':
                parentesisCierraCounter += 1
            
            #Analisis de numeros
            if re.search("\d", character) != None and checkingNum == False: #Si el caracter es digito
                checkingNum = True
                numBegMark = index
                numEndMark = index
            elif re.search("\d", character) != None and checkingNum == True:
                numEndMark = index
            
            #Check de punto
            if index < len(txt)-1:             
                if character == "." and checkingNum == True and numHasPoint == False: #Punto mientras encontramos un numero
                    numEndMark = index
                    numType = "Real"
                    numHasPoint = True
                elif character == "." and checkingNum == False:
                    tokenTable.append(['', character, 'Error, punto sin indicar numero', counter])
                    break
                elif character == "." and checkingNum == True and numHasPoint == True:
                    tokenTable.append(['', character, 'Error, dos puntos en un mismo número', counter])
                    break
                elif character == "." and checkingNum == True and re.search("\d|E", txt[index+1]) == None:
                    tokenTable.append(['', character, 'Error, punto seguido de caracter inválido', counter])
                    break

            #Check de exponente
            if index < len(txt)-1:
                if character == "E" and checkingNum == True: #Exponencial mientras encontramos un numero
                    numEndMark = index
                    numType = "Real"
                elif character == "." and checkingNum == False:
                    tokenTable.append(['', character, 'Error, exponencial sin indicar numero', counter])
                    break
                elif character == "E" and checkingNum == False and checkingVar == False:
                    tokenTable.append(['', character, 'Error, E en posición inválida', counter])
                    break
                elif character == "E" and checkingNum == True and re.search("\d|E|[-]", txt[index+1]) == None:
                    tokenTable.append(['', character, 'Error, exponente seguido de caracter inválido', counter])
                    break
            
            #Concatenacion numeros
            if index < len(txt)-1 and checkingNum: #Si no estamos en el ultimo caracter
                if re.search("\d|[.]", character) != None and re.search("\d|[.]|E", txt[index+1]) == None: #Si el caracter actual es digito y el siguiente no
                    if numType == "Real":
                        tokenTable.append(['', txt[numBegMark:numEndMark+1], 'Real', counter])
                        numBegMark = 0
                        numEndMark = 0
                        numType = ''
                        checkingNum = False
                        numHasPoint = False
                    elif numType == "Entero":
                        tokenTable.append(['', txt[numBegMark:numEndMark+1], 'Entero', counter])
                        numBegMark = 0
                        numEndMark = 0
                        numType = ''
                        checkingNum = False
                        numHasPoint = False

            else: #Si estamos en el ultimo caracter
                print("")

                

        #Error falta cerrar parentesis
        if parentesisAbreCounter > parentesisCierraCounter: #Falta cerrar
            tokenTable.append(['','','Falta cerrar paréntesis', counter])


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

#Escribe las listas al CSV
with open('tokenTable.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Expresión","Token","Type","Index"])
    writer.writerows(tokenTable)


"""
To do
Enteros
Reales
Negativos
Not. Cient.
Operadores incl. potencia
"""