import re

txt = "   n_1234   =400"
splitText = txt.split("=") #Separa el texto en el caracter antes y despues de el operador de asignacion
beginning = splitText[0] #Texto antes del operador de asignacion
end = splitText[1] #Texto despues del operador de asignacion

