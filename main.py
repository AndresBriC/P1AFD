#19/07/21 Andrés Briseño A01352283, Gabriel Dichi A01027301, Python 3.8.6

import re
import csv
import html

tokenTable = [] #Contiene la tabla con los caracteres y tipos
tok = ""
counter = 0

#Para linkear HTML al CSS
tok += '<head> <link rel="stylesheet" type="text/css" href="colores_css.css"> </head>'

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
    global tok

    for index, character in enumerate(txt): #Enumerate() se usa para poder tener el indice y el caracter
        counter += 1

        #Para caracteres antes del ultimo
        if index < len(txt)-1:
            #Checa comentarios
            if character == "/" and txt[index+1] == "/": #Si detecta un comentario, deja de analizar el resto
                tokenTable.append(['', '//','Comentario',counter])
                #HTML para englobar expresiones en div
                tok += '<div>'
                tok+='<p class = "comentario">' + str(txt[index:len(txt)-1]) + '</p>'
                tok += '</div>'
                break

            #Checa espacios
            if character == " " and begSpace == True and (txt[index+1] == " " or txt[index+1] == "="): #Si el actual es espacio y el sig. es espacio o igual
                continue
            elif character == " " and begSpace == True and varSpace == False and (txt[index+1] != " " or txt[index+1] != "="):
                tokenTable.append(['', character, 'Error, espacio dentro de la variable o variable sin asignación', counter])
                varSpace = True


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
                if character == '=': #Si no es letra, numero o _, pero es =, lo agrega y termina el análisis
                    varConcat = txt[varBegMark:varEndMark+1] #Hace el subtring de la variable sola (sin espacios)
                    tokenTable.append(['', varConcat, 'Variable', counter])
                    tok += '<div>'
                    tok+='<p class = "variable">' + varConcat + "</p>"
                    tok += '</div>'
                    tokenTable.append(['', character, 'Asignación',counter]) #Agrega la asignacion
                    tok += '<div>'
                    tok+='<p class = "asignacion">' + character + "</p>"
                    tok += '</div>'
                else:
                    tokenTable.append(['', character, 'Error, caracter no valido para variable', counter])



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
    numHasExp = False
    checkingVar = False
    varBegMark = 0
    varEndMark = 0
    isNegative = False
    global tokenTable
    global counter
    global tok

    if len(txt) == 0: #Si le pasan "end" vacio
        tokenTable.append(['','','Error, no hay operador de asignacion', counter])
        print("No hay operador de asignacion")
    else: #Si el end no esta vacio
        for index, character in enumerate(txt): #Enumerate() se usa para poder tener el indice y el caracter
            counter += 1
            
            #Analisis de asigacion
            if character == "=":
                tokenTable.append(['', '=','Error, más de un operador de asignación',counter])
                break

            #Analisis de comentarios
            if index < len(txt)-1:
                if character == "/" and txt[index+1] == "/": #Si detecta un comentario, deja de analizar el resto
                    tokenTable.append(['', '//','Comentario',counter])
                    tok += '<div>'
                    tok+='<p class = "comentario">' + str(txt[index:len(txt)-1]) + "</p>"
                    tok += '</div>'
                    break

            #Analisis de siguiente del parentesis
            if index < len(txt)-1:
                if character == "(" and re.search("\d|[a-zA-Z]|[-]", txt[index+1]) == None:
                    tokenTable.append(['', txt[index+1],'Error, Caracter inválido después de paréntesis',counter])
                    break

            #Analisis de espacios
            if index < len(txt)-1:
                if re.search("\s", character) != None and checkingNum == True and (txt[index+1] != "+" or txt[index+1] != "-" or txt[index+1] != "*" or txt[index+1] != "/" or chatxt[index+1] != "^"):
                    tokenTable.append(['', txt[index+1],'Error, número separado por otro número',counter])
                    break
                elif re.search("\s", character) != None and checkingNum == True and re.search("\s", txt[index+1]) != None:
                    continue

            #Analisis de operadores
            if index < len(txt)-1:
                #No detiene reales negativos
                if character == "-" and re.search("\d", txt[index+1]) != None and afterOp == False and checkingNum == False:
                    checkingNum = True
                    isNegative = True
                    numBegMark = index

                if (character == "+" or character == "-" or character == "*" or character == "/" or character == "^") and afterOp == False:
                    afterOp = True
                    if character == '+':
                        tokenTable.append(['',character, 'Suma', counter])
                        tok += '<div>'
                        tok+='<p class = "operador">' + character + "</p>"
                        tok += '</div>'
                    if character == '-' and numHasExp == False and checkingNum == False:
                        tokenTable.append(['',character, 'Resta', counter])
                        tok += '<div>'
                        tok+='<p class = "operador">' + character + "</p>"
                        tok += '</div>'
                    if character == '/':
                        tokenTable.append(['',character, 'División', counter])
                        tok += '<div>'
                        tok+='<p class = "operador">' + character + "</p>"
                        tok += '</div>'
                    if character == '*':
                        tokenTable.append(['',character, 'Multiplicación', counter])
                        tok += '<div>'
                        tok+='<p class = "operador">' + character + "</p>"
                        tok += '</div>'
                    if character == '^':
                        tokenTable.append(['',character, 'Potencia', counter])
                        tok += '<div>'
                        tok+='<p class = "operador">' + character + "</p>"
                        tok += '</div>'
                elif (character == "+" or character == "-" or character == "*" or character == "/" or character == "^") and afterOp == True:
                    tokenTable.append(['',character, 'Error, operadores consecutivos', counter])
                    break
            if index == len(txt)-1 and (character == "+" or character == "-" or character == "*" or character == "/" or character == "^" or character == "E"):
                tokenTable.append(['',character, 'Error, No se puede terminar con un operador', counter])
                
            #Analisis de parentesis
            if parentesisCierraCounter > parentesisAbreCounter:
                tokenTable.append(['',')','Error de paréntesis, cierra pero no abre', counter])
                break
            if character == '(':
                afterOp = False
                parentesisAbreCounter += 1
                tokenTable.append(['',character, 'Abre paréntesis', counter])
                tok += '<div>'
                tok+='<p class = "parentesis">' + character + "</p>"
                tok += '</div>'
            elif character == ')':
                afterOp = False
                parentesisCierraCounter += 1
                tokenTable.append(['',character, 'Cierra paréntesis', counter])
                tok += '<div>'
                tok+='<p class = "parentesis">' + character + "</p>"
                tok += '</div>'
            
            #Analisis de variables
            if re.search("[a-zA-Z]", character) != None and checkingVar == False and checkingNum == False: #Si es una letra
                checkingVar = True
                varBegMark = index #Marca el inicio de la concatenacion
                varEndMark = index

            if character == "_" and checkingVar == False:
                tokenTable.append(['',character, 'Error, carácter de variable inválido', counter])

            if re.search("\w", character) != None and checkingVar == False and checkingNum == False: #Si es una letra, numero o _
                checkingVar == True
                if varBegMark == varEndMark:
                    varEndMark = index
                elif character == "E" and numHasExp == True:
                    continue
                else:
                    varEndMark = index #Marca el posible final de la concatenacion



            #Analisis de numeros
            if index < len(txt)-1 and checkingVar == False:
                if re.search("\d", character) != None and checkingNum == True and re.search("\d", txt[index+1]) == None and numType != "Real": #Si el caracter actual es numero pero el siguiente no
                    numType = "Entero"
                if re.search("\d", character) != None and checkingNum == True and re.search("[a-zA-Z]", txt[index+1]) != None: #Si el caracter actual es numero pero el siguiente una letra
                    if numHasExp == False and txt[index+1] != "E":
                        tokenTable.append(['',txt[index+1], 'Error, variable no válida', counter])
                        break
            if checkingVar == False:
                if re.search("\d", character) != None and checkingNum == False and numType != "Real" and isNegative == False: #Si el caracter es digito
                    numType = "Entero"
                    checkingNum = True
                    afterOp = False
                    numBegMark = index
                    numEndMark = index
                elif re.search("\d", character) != None and checkingNum == True and numType != "Real":
                    numType = "Entero"
                    afterOp = False
                    numEndMark = index
                elif re.search("\d", character) != None and checkingNum == False and numType == "Real" and isNegative == False: #Si el caracter es digito
                    checkingNum = True
                    afterOp = False
                    numBegMark = index
                    numEndMark = index
                elif re.search("\d", character) != None and checkingNum == True and numType == "Real":
                    afterOp = False
                    numEndMark = index
            
            #Check de punto
            if index < len(txt)-1:             
                if character == "." and checkingNum == True and numHasPoint == False: #Punto mientras encontramos un numero
                    numEndMark = index
                    numType = "Real"
                    numHasPoint = True
                    afterOp = False
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
                if character == "E" and checkingNum == True and numHasExp == False: #Exponencial mientras encontramos un numero
                    numEndMark = index
                    numType = "Real"
                    numHasExp = True
                    afterOp = False
                elif character == "E" and checkingNum == True and numHasExp == True:
                    tokenTable.append(['', character, 'Error, dos exponenciales en un número', counter])
                    break
                elif character == "E" and checkingNum == False:
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
                        tokenTable.append(['', str(txt[numBegMark:numEndMark+1]), 'Real', counter])
                        tok += '<div>'
                        tok+='<p class = "real">' + str(txt[numBegMark:numEndMark+1]) + "</p>"
                        tok += '</div>'
                        numBegMark = 0
                        numEndMark = 0
                        numType = ''
                        checkingNum = False
                        numHasPoint = False
                        numHasExp = False
                        afterOp = False
                        isNegative = False
                    elif numType == "Entero":
                        tokenTable.append(['', str(txt[numBegMark:numEndMark+1]), 'Entero', counter])
                        tok += '<div>'
                        tok+='<p class = "entero">' + txt[numBegMark:numEndMark+1] + "</p>"
                        tok += '</div>'
                        numBegMark = 0
                        numEndMark = 0
                        numType = ''
                        checkingNum = False
                        numHasExp = False
                        numHasPoint = False
                        afterOp = False
                        isNegative = False
            
            #Concatenacion de variables
            if index < len(txt)-1 and checkingVar: #Si no estamos en el ultimo caracter
                if re.search("\w", character) != None and re.search("\w", txt[index+1]) == None: #Si el caracter actual es variable y el siguiente no
                    tokenTable.append(['', txt[varBegMark:varEndMark+1], 'Variable', counter])
                    tok += '<div>'
                    tok+='<p class = "variable">' + txt[varBegMark:varEndMark+1] + "</p>"
                    tok += '</div>'
                    varBegMark = 0
                    varEndMark = 0
                    checkingVar = False
                    afterOp = False

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
    #HTML para encasillar todo en el div class row
    tok += '<div class="row">'
    lexerAritmeticoBeginning(beginning)
    lexerAritmeticoEnd(end)
    tok += "</div>"

    print("______________________________________________________________________________________\n")

testsFile.close()

#Escribe las listas al CSV
with open('tokenTable.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Expresión","Token","Type","Index"])
    writer.writerows(tokenTable)

#Escribe al archivo HTML
f = open('colores.html','w') # w if you want to write override or a if you want to write and append
f.write(tok)
f.close()  