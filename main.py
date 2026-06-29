from Analisis_Sintactico import parser, ERRORS, generar_log_sintactico
from Analisis_Lexico import lexer
import Analisis_Semantico as sem



codigo = """
local a = 10
local b = 5
local c = a + b

function suma(x, y)
    local z = x + y
    return z
end

for i = 1, 10 do
    local k = i
    break
end

local d = a + "hola"
"""
 
ERRORS.clear()
#sem.reset_semantico()

parser.parse(codigo, lexer=lexer)

#generar_log_sintactico(codigo, usuario="nahinespinoza")
sem.generar_log_semantico(codigo, usuario="RuizJul")



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
 
codigo_con_errores =  """
break
"""
 
ERRORS.clear()
sem.reset_semantico()
 
parser.parse(codigo_con_errores, lexer=lexer)
 
#generar_log_sintactico(codigo_con_errores, usuario="RuizJul-test-errores")
sem.generar_log_semantico(codigo_con_errores, usuario="RuizJul-test-errores")
 
print("\n=== RESUMEN PRUEBA DE ERRORES SEMÁNTICOS ===")
print(f"Errores semánticos detectados: {len(sem.SEMANTIC_ERRORS)}")
for e in sem.SEMANTIC_ERRORS:
    print(" -", e)


