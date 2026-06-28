from Analisis_Sintactico import parser, ERRORS, generar_log_sintactico
from Analisis_Lexico import lexer
import Analisis_Semantico as sem

codigo = """
local resultado = 2 + 3 * 4
local r = (2 + 3) * 4 ^ 2
 
local persona = { nombre = "Ana", edad = 20 }
edadActual = persona["edad"]
 
local entrada = io.read()
 
local saludo = "hola" .. " mundo"
 
function saludar(nombre)
    mensaje = "hola"
end
 
function suma(a, b)
    return a + b
end
 
local contador = 1
while contador < 5 do
    contador = contador + 1
end
 
for i = 1, 10, 2 do
    local doble = i * 2
end
"""
 
ERRORS.clear()
sem.reset_semantico()

parser.parse(codigo, lexer=lexer)

#generar_log_sintactico(codigo, usuario="nahinespinoza")
sem.generar_log_semantico(codigo, usuario="nahinespinoza")



# ============================================================
# CÓDIGO DE PRUEBA - ERRORES SEMÁNTICOS A PROPÓSITO
# ============================================================
# Este segundo bloque NO es parte del programa original; se incluye
# únicamente para verificar que las reglas semánticas (Nahin Espinoza)
# detectan correctamente los errores que deben detectar:
#
#   1) Variable no declarada  -> usar 'zzz' sin haberla declarado antes
#   2) Función duplicada      -> declarar 'saludar' dos veces
# ============================================================
 
codigo_con_errores = """
local x = 1
y = zzz
 
function saludar(nombre)
    mensaje = "hola"
end
 
function saludar(otro)
    mensaje = "hola otra vez"
end
"""
 
ERRORS.clear()
sem.reset_semantico()
 
parser.parse(codigo_con_errores, lexer=lexer)
 
generar_log_sintactico(codigo_con_errores, usuario="nahinespinoza-test-errores")
sem.generar_log_semantico(codigo_con_errores, usuario="nahinespinoza-test-errores")
 
print("\n=== RESUMEN PRUEBA DE ERRORES SEMÁNTICOS ===")
print(f"Errores semánticos detectados: {len(sem.SEMANTIC_ERRORS)}")
for e in sem.SEMANTIC_ERRORS:
    print(" -", e)