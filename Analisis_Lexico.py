# ============================================================
# ANALIZADOR LÉXICO - PROYECTO LUA
# Integrante : Nahin Espinoza
# GitHub     : nahinespinoza
# Aporte     : Números, Strings y Operadores
# Integrante : Julian Ruiz 
# GitHub     : RuizJul
# Aporte     : palabras reservadas e identificadores
# ============================================================

import ply.lex as lex
from datetime import datetime
import os

# ============================================================
# INICIO APORTE: NAHIN ESPINOZA
# ============================================================

# ==================== TOKENS ====================
tokens = (
    'NUMBER',   # Números enteros, flotantes, hex y científicos
    'STRING',   # Cadenas de texto con comillas dobles o simples
    'PLUS',     # +
    'MINUS',    # -
    'TIMES',    # *
    'DIVIDE',   # /
    'MOD',      # %
    'POWER',    # ^
    'EQ',       # ==
    'NE',       # ~=
    'LT',       # <
    'GT',       # >
    'LE',       # <=
    'GE',       # >=
    'AND',      # and
    'OR',       # or
    'NOT',      # not
    'CONCAT',   # ..
    'BREAK',
    # Auxiliares mínimos para procesar el algoritmo1.lua
    'ID',
    'ASSIGN',
    'LPAREN',
    'RPAREN',
    'DOT',
     # Tokens nuevos Nahin Espinoza: While / Diccionarios (Tables) / Entrada de datos
    'LBRACE',   # {
    'RBRACE',   # }
    'LBRACKET', # [
    'RBRACKET', # ]
    # Tokens Julian Ruiz
    'IF',
    'THEN',
    'ELSE',
    'ELSEIF',
    'WHILE',
    'DO',
    'FOR',
    'FUNCTION',
    'LOCAL',
    'RETURN',
    'END',
    'TRUE',
    'FALSE',
    'NIL',
    'COMMA',
)

tokens = tuple(dict.fromkeys(tokens))  # Eliminar duplicados

# ------ NÚMEROS ------
# Reconoce: enteros (42), flotantes (3.14),
# hexadecimales (0xFF) y notación científica (2.5e3)
def t_NUMBER(t):
    r'0[xX][0-9a-fA-F]+|\d+\.\d*(?:[eE][+-]?\d+)?|\d+[eE][+-]?\d+|\d+'
    raw = t.value
    if raw.startswith(('0x', '0X')):
        t.value = int(raw, 16)
    elif '.' in raw or 'e' in raw.lower():
        t.value = float(raw)
    else:
        t.value = int(raw)
    return t

# ------ STRINGS ------
# Reconoce cadenas con comillas dobles o simples
# e incluye secuencias de escape como \" \' \n \t \\
def t_STRING(t):
    r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''
    t.value = t.value[1:-1]  # Quitar comillas externas
    return t

# ------ OPERADORES RELACIONALES (2 caracteres antes que 1) ------
# Deben ser funciones y definirse antes que LT, GT y ASSIGN
# para que PLY no tokenice '==' como '='+'=' ni '<=' como '<'+'='
def t_EQ(t):
    r'=='
    return t

def t_NE(t):
    r'~='
    return t

def t_LE(t):
    r'<='
    return t

def t_GE(t):
    r'>='
    return t

def t_LT(t):
    r'<'
    return t

def t_GT(t):
    r'>'
    return t

# ------ CONCATENACIÓN (antes que DOT) ------
# '..' debe reconocerse antes que '.' para no dividirse en dos tokens
def t_CONCAT(t):
    r'\.\.'
    return t

# ------ OPERADORES ARITMÉTICOS ------
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_MOD    = r'%'
t_POWER  = r'\^'

# ------ LLAVES Y CORCHETES (Diccionarios / Tables y acceso indexado) ------
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# ============================================================
# FIN APORTE: NAHIN ESPINOZA
# ============================================================

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    msg = f"[ERROR LÉXICO] Línea {t.lexer.lineno}: Carácter ilegal '{t.value[0]}'"
    print(msg)
    t.lexer.error_list.append(msg)
    t.lexer.skip(1)

# ==================== GENERACIÓN DE LOG ====================
def generate_log(all_tokens, errors, source_filename):
    os.makedirs("logs", exist_ok=True)
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y-%Hh%M")
    log_path = f"logs/lexico-NahinEspinoza-{timestamp}.txt"

    mis_tokens = {
        'NUMBER', 'STRING',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD', 'POWER',
        'EQ', 'NE', 'LT', 'GT', 'LE', 'GE',
        'AND', 'OR', 'NOT', 'CONCAT',
        'COMMA',
    }

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("  LOG DE ANÁLISIS LÉXICO - PROYECTO LUA\n")
        f.write(f"  Integrante : Nahin Espinoza (nahinespinoza)\n")
        f.write(f"  Aporte     : Números, Strings y Operadores\n")
        f.write(f"  Archivo    : {source_filename}\n")
        f.write(f"  Fecha/Hora : {now.strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")

        f.write(">>> TOKENS RECONOCIDOS\n")
        f.write(f"{'N°':<5} {'TIPO':<14} {'VALOR':<30} {'LÍNEA'}\n")
        f.write("-" * 58 + "\n")
        for i, tok in enumerate(all_tokens, 1):
            valor = f'"{tok.value}"' if tok.type == 'STRING' else str(tok.value)
            f.write(f"{i:<5} {tok.type:<14} {valor:<30} {tok.lineno}\n")

        f.write(f"\nTotal de tokens: {len(all_tokens)}\n\n")

        f.write(">>> RESUMEN - APORTE NAHIN ESPINOZA\n")
        f.write("    Números, Strings y Operadores\n")
        f.write("-" * 40 + "\n")
        conteo = {}
        for tok in all_tokens:
            if tok.type in mis_tokens:
                conteo[tok.type] = conteo.get(tok.type, 0) + 1
        for tipo, cantidad in sorted(conteo.items()):
            f.write(f"  {tipo:<14}: {cantidad}\n")

        f.write("\n>>> ERRORES ENCONTRADOS\n")
        f.write("-" * 40 + "\n")
        if errors:
            for err in errors:
                f.write(f"  {err}\n")
        else:
            f.write("  Sin errores léxicos.\n")

        f.write("\n" + "=" * 60 + "\n")
        f.write("  FIN DEL ANÁLISIS\n")
        f.write("=" * 60 + "\n")

    print(f"\n ----- Log generado: {log_path}")
    return log_path

# ==================== ANÁLISIS ====================
def analizar(codigo, source_filename):
    lexer = lex.lex()
    lexer.error_list = []
    lexer.input(codigo)

    all_tokens = []
    mis_tokens = {
        'NUMBER', 'STRING',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD', 'POWER',
        'EQ', 'NE', 'LT', 'GT', 'LE', 'GE',
        'AND', 'OR', 'NOT', 'CONCAT',
        'COMMA',
    }

    print("=" * 60)
    print("  APORTE: NAHIN ESPINOZA — Números, Strings y Operadores")
    print("=" * 60)
    print(f"  {'TIPO':<14} {'VALOR':<30} {'LÍNEA'}")
    print("-" * 58)

    while True:
        tok = lexer.token()
        if not tok:
            break
        all_tokens.append(tok)
        if tok.type in mis_tokens:
            valor = f'"{tok.value}"' if tok.type == 'STRING' else str(tok.value)
            print(f"  {tok.type:<14} {valor:<30} {tok.lineno}")

    print("-" * 58)
    print(f"  Tokens de mi aporte : {sum(1 for t in all_tokens if t.type in mis_tokens)}")
    print(f"  Tokens en total     : {len(all_tokens)}")

    generate_log(all_tokens, lexer.error_list, source_filename)

# ============================================================
# INICIO APORTE: JULIAN RUIZ
# ============================================================

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'elseif': 'ELSEIF',
    'while': 'WHILE',
    'do': 'DO',
    'for': 'FOR',
    'function': 'FUNCTION',
    'local': 'LOCAL',
    'return': 'RETURN',
    'end': 'END',
    'true': 'TRUE',
    'false': 'FALSE',
    'nil': 'NIL',
    'and': 'AND',
    'or':  'OR',
    'not': 'NOT',
    'break': 'BREAK',
}

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_COMMENT_SINGLE(t):
    r'--[^\n]*'
    pass  # Ignorar comentarios

t_ASSIGN   = r'='
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_DOT      = r'\.'
t_ignore   = ' \t\r'
t_COMMA = r','


# ==================== GENERACIÓN DE LOG ====================
def generate_log_reservadas(all_tokens, errors, source_filename):
    os.makedirs("logs", exist_ok=True)

    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y-%Hh%M")
    log_path = f"logs/lexico-JulianRuiz-{timestamp}.txt"

    mis_tokens = {
        'ID',
        'IF', 'THEN', 'ELSE', 'ELSEIF',
        'WHILE', 'DO', 'FOR',
        'FUNCTION', 'LOCAL',
        'RETURN', 'END',
        'TRUE', 'FALSE', 'NIL',
        'AND', 'OR', 'NOT',
        'COMMA'
    }

    with open(log_path, "w", encoding="utf-8") as f:

        f.write("=" * 60 + "\n")
        f.write("  LOG DE ANÁLISIS LÉXICO - PROYECTO LUA\n")
        f.write(f"  Integrante : Julian Ruiz\n")
        f.write(f"  Aporte     : Identificadores y Palabras Reservadas\n")
        f.write(f"  Archivo    : {source_filename}\n")
        f.write(f"  Fecha/Hora : {now.strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")

        f.write(">>> TOKENS RECONOCIDOS\n")
        f.write(f"{'N°':<5} {'TIPO':<15} {'VALOR':<30} {'LÍNEA'}\n")
        f.write("-" * 60 + "\n")

        tokens_julian = [tok for tok in all_tokens if tok.type in mis_tokens]

        for i, tok in enumerate(tokens_julian, 1):
            f.write(
                f"{i:<5} "
                f"{tok.type:<15} "
                f"{str(tok.value):<30} "
                f"{tok.lineno}\n"
            )

        f.write(f"\nTotal de tokens: {len(tokens_julian)}\n\n")

        f.write(">>> RESUMEN - APORTE JULIAN RUIZ\n")
        f.write("    Identificadores y Palabras Reservadas\n")
        f.write("-" * 40 + "\n")

        conteo = {}

        for tok in all_tokens:
            if tok.type in mis_tokens:
                conteo[tok.type] = conteo.get(tok.type, 0) + 1

        for tipo, cantidad in sorted(conteo.items()):
            f.write(f"  {tipo:<15}: {cantidad}\n")

        f.write("\n>>> ERRORES ENCONTRADOS\n")
        f.write("-" * 40 + "\n")

        if errors:
            for err in errors:
                f.write(f"  {err}\n")
        else:
            f.write("  Sin errores léxicos.\n")

        f.write("\n" + "=" * 60 + "\n")
        f.write("  FIN DEL ANÁLISIS\n")
        f.write("=" * 60 + "\n")

    print(f"\n----- Log generado: {log_path}")

    return log_path

# ==================== ANÁLISIS ====================
def analizar_reservadas(codigo, source_filename):

    lexer = lex.lex()
    lexer.error_list = []

    lexer.input(codigo)

    all_tokens = []

    mis_tokens = {
        'ID',
        'IF', 'THEN', 'ELSE', 'ELSEIF',
        'WHILE', 'DO', 'FOR',
        'FUNCTION', 'LOCAL',
        'RETURN', 'END',
        'TRUE', 'FALSE', 'NIL',
        'AND', 'OR', 'NOT',
        'COMMA'
    }

    print("=" * 60)
    print(" APORTE: JULIAN RUIZ — Identificadores y Palabras Reservadas")
    print("=" * 60)
    print(f"{'TIPO':<15} {'VALOR':<30} {'LÍNEA'}")
    print("-" * 60)

    while True:

        tok = lexer.token()

        if not tok:
            break

        all_tokens.append(tok)

        if tok.type in mis_tokens:
            print(
                f"{tok.type:<15} "
                f"{str(tok.value):<30} "
                f"{tok.lineno}"
            )

    print("-" * 60)

    print(
        f"Tokens de mi aporte : "
        f"{sum(1 for t in all_tokens if t.type in mis_tokens)}"
    )

    print(f"Tokens en total     : {len(all_tokens)}")

    generate_log_reservadas(
        all_tokens,
        lexer.error_list,
        source_filename
    )


# ============================================================
# FIN APORTE:Julian Ruiz
# ============================================================

# ==================== MAIN ====================
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    archivo1 = os.path.join(script_dir, "algoritmo1.lua")
    archivo2 = os.path.join(script_dir, "algoritmo2.lua")

    # APORTE NAHIN
    if os.path.exists(archivo1):
        with open(archivo1, "r", encoding="utf-8") as f:
            codigo = f.read()
        print("\n===== APORTE NAHIN ESPINOZA =====\n")
        analizar(codigo, archivo1)
    else:
        print("No se encontró algoritmo1.lua")
    
    # APORTE JULIAN
    
    if os.path.exists(archivo2):
        with open(archivo2, "r", encoding="utf-8") as f:
            codigo = f.read()
        print("\n===== APORTE JULIAN RUIZ =====\n")
        analizar_reservadas(codigo, archivo2)
    else:
        print("No se encontró algoritmo2.lua")
        


lexer = lex.lex()