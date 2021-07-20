# P1AFD
 Actividad de programación. Programando un AFD.

Reglas para el lexer

En general

No puede haber más de un operador de asignación (=)
Todo lo que siga del // es un comentario hasta que acabe la línea


En la variable

Pueden haber n espacios antes y después de la variable pero ninguno dentro de ella
Los caracteres permitidos son letras, números y guión bajo.
Deben empezar con una letra


En la expresión

No pueden haber dos operadores consecutivos (Los comentarios son la excepción, pues usan dos operadores de división //)
Después de un operador solo puede haber letra, numero, paréntesis o n espacios
Cada paréntesis se debe cerrar
Pueden haber n espacios entre números, paréntesis y operadores, pero no dentro del número. Ej: 43+   2 es permitido pero 4  3+2 no lo es
Números reales (de punto flotante):
Pueden ser positivos o negativos
Pueden o no tener parte decimal pero deben contener un punto (ejemplo: 10. o 10.0)
Pueden usar notación exponencial con la letra E, mayúscula o minúscula, pero después de la letra E sólo puede ir un entero positivo o negativo (ejemplo: 2.3E3,  6.345e-5,  -0.001E-3,  0.467E9).

Símbolos del autómata
L = cualquier letra (a - Z)
T = todos los caracteres alfanuméricos
+ = operadores (+, -, *, /, ^)
p = punto
_ = guión bajo
E = Indicador de notación científica
# = cualquier dígito
( = abre paréntesis
) = cierra paréntesis

Notas del autómata
Aunque + incluye varios operadores, cuando un operador es seguido por la / nos lleva a un error, excepto si el primer operador es una diagonal. No válido: +/ Válido: //


Instrucciones de uso

Descargar el repositorio de GitHub
Abra en cualquier IDE compatible con Python (ver 3.8.6)
Poner los casos de prueba en el archivo "P1_pruebas_.txt"
Compilar y correr el programa
Abrir el CSV llamado "tokenTable.csv" para visualizar los resultados