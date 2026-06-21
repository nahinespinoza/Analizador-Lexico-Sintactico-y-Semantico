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
    value : NUMBER
          | STRING
          | TRUE
          | FALSE
          | NIL
          | ID
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
# GENERAR LOGS
# ============================================================
from datetime import datetime
import os

ERRORS = []

def generar_log_sintactico(codigo):
    os.makedirs("logs", exist_ok=True)

    now = datetime.now()
    fecha = now.strftime("%d%m%Y")
    hora = now.strftime("%Hh%M")

    usuario = "RuizJul"  

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