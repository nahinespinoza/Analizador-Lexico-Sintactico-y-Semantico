from Analisis_Sintactico import parser, ERRORS, generar_log_sintactico
from Analisis_Lexico import lexer

codigo = """
local a = 10
print(a)
print(20)
print("hola mundo")
"""


ERRORS.clear()

parser.parse(codigo, lexer=lexer)

generar_log_sintactico(codigo)