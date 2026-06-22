import ply.yacc as yacc
from Analisis_Lexico import tokens , lexer

# ============================================================
# INICIO APORTE: JULIAN RUIZ
# ============================================================

start = 'program'

def p_program(p):
    '''
    program : program statement
            | statement
    '''
    pass

# ASIGNACIONES

def p_statement_local(p):
    '''
    statement : LOCAL ID ASSIGN value
    '''
    print("Declaracion local valida:", p[2])

def p_statement_global(p):
    '''
    statement : ID ASSIGN value
    '''
    print("Asignacion global valida:", p[1])

def p_value(p):
    '''
    value : NIL
    '''
    p[0] = p[1]


# BLOQUES IF

def p_expression_compare(p):
    '''
    expression : expression GT expression
               | expression LT expression
               | expression GE expression
               | expression LE expression
               | expression EQ expression
               | expression NE expression
    '''
    p[0] = True

def p_statement_if(p):
    '''
    statement : IF expression THEN program elseif_list else_part END
    '''
    print("IF válido")

def p_else_part(p):
    '''
    else_part : ELSE program
              | empty
    '''
    pass

def p_elseif_list(p):
    '''
    elseif_list : elseif_list elseif_clause
                | empty
    '''
    pass

def p_elseif_clause(p):
    '''
    elseif_clause : ELSEIF expression THEN program
    '''
    pass

def p_expression_value(p):
    '''
    expression : NUMBER
               | STRING
               | TRUE
               | FALSE
               | ID
    '''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

#FUNCIONES SIN RETORNO
def p_statement_function(p):
    '''
    statement : FUNCTION ID LPAREN param_list RPAREN program END
    '''
    print("Función válida:", p[2])

#FUNCIONES CON RETORNO => Nahin Espinoza 

def p_statement_function_return(p):
    '''
    statement : FUNCTION ID LPAREN param_list RPAREN program RETURN expression END
              | FUNCTION ID LPAREN param_list RPAREN empty RETURN expression END
    '''
    print(f"Función con retorno válida: {p[2]} -> retorna {p[8]}")



def p_param_list(p):
    '''
    param_list : param_list COMMA ID
               | ID
               | empty
    '''
    pass

#IMPRIMIR

def p_statement_print(p):
    '''
    statement : ID LPAREN print_args RPAREN
    '''
    if p[1] == "print":
        print("PRINT válido")

def p_print_args(p):
    '''
    print_args : print_args COMMA value
               | value
               | empty
    '''
    pass

# Arreglos (Tables Indexadas)

def p_statement_array(p):
    '''
    statement : ID ASSIGN LBRACE value_list RBRACE
    '''
    print("Arreglo válido:", p[1])

def p_value_list(p):
    '''
    value_list : value_list COMMA value
               | value
               | empty
    '''
    pass

def p_array_access(p):
    '''
    array_access : ID LBRACKET value RBRACKET
    '''
    pass

def p_value_array_access(p):
    '''
    value : array_access
    '''
    p[0] = p[1]

# EXPRESIONES LOGICAS
def p_expression_logic(p):
    '''
    expression : expression AND expression
               | expression OR expression
    '''
    pass

def p_expression_not(p):
    '''
    expression : NOT expression
    '''
    pass

# ERRORES
def p_error(p):
    if p:
        msg = f"Línea {p.lineno}: token inesperado '{p.value}'"
        print("Error sintáctico:", msg)
        ERRORS.append(msg)
    else:
        msg = "Error sintáctico al final del archivo"
        print(msg)
        ERRORS.append(msg)
# ============================================================
# FIN APORTE: JULIAN RUIZ
# ============================================================


# ============================================================
# INICIO APORTE: NAHIN ESPINOZA
# Temas: Expresiones Aritméticas y Precedencia de Operadores,
#        Estructura While, Diccionarios (Tables clave-valor),
#        Función sin Retorno (uso dentro del while),
#        Entrada de Datos (io.read())
# ============================================================
 
# ------------------------------------------------------------
# 1) PRECEDENCIA DE OPERADORES ARITMÉTICOS
# ------------------------------------------------------------
# De menor a mayor precedencia, igual que en Lua:
#   or
#   and
#   relacionales (<  >  <=  >=  ~=  ==)
#   ..  (concatenación)
#   +  -          (binarios)
#   *  /  %       
#   unario - (not, # no se implementan aquí)
#   ^             (potencia, asocia a la derecha)
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'GT', 'LT', 'GE', 'LE', 'EQ', 'NE'),
    ('left', 'CONCAT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'POWER'),
    ('right', 'UMINUS'),
)
 
# ------------------------------------------------------------
# CONEXIÓN value -> expression
# ------------------------------------------------------------
# Esto permite que una asignación (local x = ... / x = ...)
# acepte expresiones aritméticas completas, no solo valores sueltos.
# Ejemplo: resultado = 2 + 3 * 4   /   r = (2 + 3) * 4 ^ 2
def p_value_expression(p):
    '''
    value : expression
    '''
    p[0] = p[1]
 
 
# ------------------------------------------------------------
# EXPRESIONES ARITMÉTICAS
# ------------------------------------------------------------
def p_expression_binop(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | expression MOD expression
               | expression POWER expression
    '''
    izq, op, der = p[1], p[2], p[3]
 
    if op == '+':
        p[0] = izq + der if isinstance(izq, (int, float)) and isinstance(der, (int, float)) else True
    elif op == '-':
        p[0] = izq - der if isinstance(izq, (int, float)) and isinstance(der, (int, float)) else True
    elif op == '*':
        p[0] = izq * der if isinstance(izq, (int, float)) and isinstance(der, (int, float)) else True
    elif op == '/':
        p[0] = izq / der if isinstance(izq, (int, float)) and isinstance(der, (int, float)) and der != 0 else True
    elif op == '%':
        p[0] = izq % der if isinstance(izq, (int, float)) and isinstance(der, (int, float)) and der != 0 else True
    elif op == '^':
        p[0] = izq ** der if isinstance(izq, (int, float)) and isinstance(der, (int, float)) else True
 
    print(f"Expresión aritmética válida: {izq} {op} {der} -> {p[0]}")
 
 
def p_expression_uminus(p):
    '''
    expression : MINUS expression %prec UMINUS
    '''
    p[0] = -p[2] if isinstance(p[2], (int, float)) else True
    print("Expresión unaria válida (negativo):", p[0])
 
 
def p_expression_group(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = p[2]
    print("Expresión agrupada (paréntesis) válida")
 
# ------------------------------------------------------------
# CONCATENACIÓN DE STRINGS (..)
# ------------------------------------------------------------
def p_expression_concat(p):
    '''
    expression : expression CONCAT expression
    '''
    izq, der = p[1], p[3]
    p[0] = f"{izq}{der}"
    print(f"Concatenación válida: {izq} .. {der} -> {p[0]}") 

# ------------------------------------------------------------
# 1) ESTRUCTURA WHILE
# ------------------------------------------------------------
def p_statement_while(p):
    '''
    statement : WHILE expression DO program END
    '''
    print("WHILE válido")

# ------------------------------------------------------------
# 2)    ESTRUCTURA FOR (numérico): for i = inicio, fin [, paso] do ... end
# ------------------------------------------------------------
def p_statement_for(p):
    '''
    statement : FOR ID ASSIGN expression COMMA expression DO program END
              | FOR ID ASSIGN expression COMMA expression COMMA expression DO program END
    '''
    print(f"FOR válido: variable de control '{p[2]}'") 
 
# ------------------------------------------------------------
# 3) DICCIONARIOS / TABLES (clave = valor), estilo Lua
#    Ejemplo:  local persona = { nombre = "Ana", edad = 20 }
# ------------------------------------------------------------
def p_value_table(p):
    '''
    value : LBRACE table_fields RBRACE
    '''
    p[0] = p[2]
    print("Tabla (diccionario) válida:", p[2])
 
 
def p_table_fields(p):
    '''
    table_fields : table_fields COMMA table_field
                 | table_field
                 | empty
    '''
    if len(p) == 4:
        p[1].update(p[3])
        p[0] = p[1]
    elif len(p) == 2 and p[1] not in (None,) and isinstance(p[1], dict):
        p[0] = p[1]
    else:
        p[0] = {}
 
 
def p_table_field(p):
    '''
    table_field : ID ASSIGN value
    '''
    p[0] = {p[1]: p[3]}
    print(f"  -> clave '{p[1]}' asignada con valor '{p[3]}'")
 
 
# Acceso indexado a tabla: persona["edad"]  ó  persona[1]
def p_expression_table_access(p):
    '''
    expression : ID LBRACKET value RBRACKET
    '''
    p[0] = True
    print(f"Acceso a tabla válido: {p[1]}[{p[3]}]")
 
 
# ------------------------------------------------------------
# 4) ENTRADA DE DATOS: io.read()
#    Se usa como value para poder asignarse, ej:
#    local nombre = io.read()
# ------------------------------------------------------------
def p_value_io_read(p):
    '''
    value : ID DOT ID LPAREN RPAREN
    '''
    if p[1] == "io" and p[3] == "read":
        p[0] = "ENTRADA_DATOS"
        print("Entrada de datos válida: io.read()")
    else:
        p[0] = None
 
 
# ============================================================
# FIN APORTE: NAHIN ESPINOZA
# ============================================================





# ============================================================
# GENERAR LOGS
# ============================================================
from datetime import datetime
import os

ERRORS = []

def generar_log_sintactico(codigo, usuario="RuizJul"):
    os.makedirs("logs", exist_ok=True)
 
    now = datetime.now()
    fecha = now.strftime("%d%m%Y")
    hora = now.strftime("%Hh%M")
 
    filename = f"logs/sintactico-{usuario}-{fecha}-{hora}.txt"
 
    with open(filename, "w", encoding="utf-8") as f:
        f.write("LOG DE ANÁLISIS SINTÁCTICO\n")
        f.write("=" * 40 + "\n\n")
 
        f.write("CÓDIGO ANALIZADO:\n")
        f.write(codigo + "\n\n")
 
        f.write("ERRORES ENCONTRADOS:\n")
 
        if ERRORS:
            for e in ERRORS:
                f.write("- " + e + "\n")
        else:
            f.write("Sin errores sintácticos.\n")
 
    print(f"\n📄 Log generado: {filename}")



parser = yacc.yacc()
