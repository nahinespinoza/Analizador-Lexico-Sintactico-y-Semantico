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
    # Auxiliares mínimos para procesar el algoritmo1.lua
    'ID',
    'ASSIGN',
    'LPAREN',
    'RPAREN',
    'DOT',
)

# and/or/not coinciden con el patrón de identificador,
# se resuelven dentro de t_ID con este diccionario
reserved = {
    'and': 'AND',
    'or':  'OR',
    'not': 'NOT',
}

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

# ============================================================
# FIN APORTE: NAHIN ESPINOZA
# ============================================================

# ==================== TOKENS AUXILIARES ====================
# Solo lo mínimo para procesar identificadores y símbolos del algoritmo1.lua

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID') 
    # and/or/not comparten el mismo patrón que un identificador,
    # se distinguen aquí consultando el diccionario reserved
    return t

def t_COMMENT_SINGLE(t):
    r'--[^\n]*'
    pass  # Ignorar comentarios

t_ASSIGN   = r'='
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_DOT      = r'\.'
t_ignore   = ' \t\r'

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

# ==================== MAIN ====================
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_file = os.path.join(script_dir, "algoritmo1.lua")

    if os.path.exists(source_file):
        with open(source_file, "r", encoding="utf-8") as f:
            codigo = f.read()
        print(f"Archivo: {source_file}\n")
        analizar(codigo, source_file)
    else:
        print("---- X No se encontró algoritmo1.lua en la misma carpeta. X ---- ")