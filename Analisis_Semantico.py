# ============================================================
# ANALIZADOR SEMÁNTICO - PROYECTO LUA
# ============================================================
#
# APORTE NAHIN ESPINOZA:
#  1.- Declaración de variables
#  4.- Funciones declaradas
#
# ============================================================

# ------------------------------------------------------------
# ESTRUCTURAS DE DATOS
# ------------------------------------------------------------

# Tabla de símbolos de variables.
# clave   -> nombre de la variable
# valor   -> dict con tipo (local/global) y la linea donde se declaro
tabla_variables = {}

# Tabla de símbolos de funciones.
# clave   -> nombre de la función
# valor   -> dict con: linea, num_parametros, tiene_retorno
tabla_funciones = {}

# Lista de errores semánticos encontrados 
SEMANTIC_ERRORS = []


def reset_semantico():
    # limpia todo para que no se mezclen los resultados si se
    # corre el analizador varias veces en la misma ejecucion
    tabla_variables.clear()
    tabla_funciones.clear()
    SEMANTIC_ERRORS.clear()

def error(t1, t2, op, linea):
    msg = f"Línea {linea}: operación inválida {t1} {op} {t2}"
    print("⚠️", msg)
    SEMANTIC_ERRORS.append(msg)


# ===========================
# Aporte Nahin Espinoza 
# ===========================
#
# Regla 1: declaracion de variables
# Una variable solo se puede usar si ya fue declarada antes
# (con local o porque ya se le habia asignado algo como global).
# Si no esta en la tabla, es un error.

def regla_variable_no_declarada(nombre, linea):
    # revisa si la variable ya existe en la tabla antes de usarla

    if nombre not in tabla_variables:
        msg = (f"Línea {linea}: Error semántico - la variable "
               f"'{nombre}' se usa pero nunca fue declarada.")
        print("⚠️", msg)
        SEMANTIC_ERRORS.append(msg)
        return False
    return True


def registrar_variable_local(nombre, linea):
    """
    Registra una variable declarada con LOCAL en la tabla de símbolos.
    Alimenta la tabla para que regla_variable_no_declarada funcione.
    """
    tabla_variables[nombre] = {'tipo': 'local', 'linea': linea}


def registrar_variable_global(nombre, linea):


    if nombre not in tabla_variables:
        tabla_variables[nombre] = {'tipo': 'global', 'linea': linea}


# REGLA SEMÁNTICA #2 Funciones declaradas
# -----------------------------------------------------
# No pueden existir dos funciones declaradas con el mismo nombre en el programa
#  

def regla_funcion_duplicada(nombre, linea, num_parametros, tiene_retorno):
    """
    Verifica que la función 'nombre' no haya sido declarada antes.
    Si no existe, la registra en la tabla de funciones.
    """
    if nombre in tabla_funciones:
        msg = (f"Línea {linea}: Error semántico - la función "
               f"'{nombre}' ya había sido declarada en la línea "
               f"{tabla_funciones[nombre]['linea']} (función duplicada).")
        print("!!!", msg)
        SEMANTIC_ERRORS.append(msg)
        return False

    tabla_funciones[nombre] = {
        'linea': linea,
        'num_parametros': num_parametros,
        'tiene_retorno': tiene_retorno,
    }
    return True

# ============================================================
# FIN APORTE SEMÁNTICO: NAHIN ESPINOZA
# ============================================================

# ===========================
# INICIO APORTE JULIAN RUIZ
# ===========================

def registrar_tipo_variable(nombre, tipo_dato):
    if nombre not in tabla_variables:
        return

    tabla_variables[nombre]["tipo_dato"] = tipo_dato
    print(f"SEMANTICO -> {nombre} : {tipo_dato}")


def obtener_tipo_variable(nombre):
    return tabla_variables.get(nombre, {}).get("tipo_dato")



def validar_tipos_operacion(n1, n2, linea):
    t1 = obtener_tipo_variable(n1)
    t2 = obtener_tipo_variable(n2)

    if t1 is None or t2 is None:
        error(f"Línea {linea}: variable sin tipo definido ({n1}, {n2})")
        return None, None

    return t1, t2


def regla_operacion(tipo_izq, tipo_der, operador, linea):

    # -------------------------
    # ARITMÉTICAS
    # -------------------------
    if operador in ["+", "-", "*", "/", "%", "^"]:
        if tipo_izq == "any" or tipo_der == "any":
            return True
        if tipo_izq != "number" or tipo_der != "number":
            error(tipo_izq, tipo_der, operador, linea)
            return False
        return True

    # -------------------------
    # CONCATENACIÓN LUA
    # -------------------------
    if operador == "..":
        if tipo_izq == "any" or tipo_der == "any":
            return True
        if tipo_izq != "string" or tipo_der != "string":
            error(f"Línea {linea}: concatenación inválida {tipo_izq} .. {tipo_der}")
            return False
        return True

    # -------------------------
    # COMPARACIONES
    # -------------------------
    if operador in ["==", "~=", "<", ">", "<=", ">="]:
        return True

    # -------------------------
    # LÓGICOS
    # -------------------------
    if operador in ["and", "or"]:
        return True

    error(f"Línea {linea}: operador desconocido '{operador}'")
    return False

loop_stack = []

def regla_break(linea):
    if len(loop_stack) == 0:
        msg = f"Línea {linea}: 'break' fuera de un bucle"
        print("⚠️", msg)
        SEMANTIC_ERRORS.append(msg)
        return False

    return True


# ============================================================
# FIN APORTE JULIAN RUIZ
# ============================================================

# ============================================================
# GENERACIÓN DE LOG SEMÁNTICO
# ============================================================
from datetime import datetime
import os


def generar_log_semantico(codigo, usuario="usuarioGit"):
    """
    Genera el log de análisis semántico con el formato:
        logs/semantico-usuarioGit-DDMMYYYY-HHhMM.txt
    """
    os.makedirs("logs", exist_ok=True)

    now = datetime.now()
    fecha = now.strftime("%d%m%Y")
    hora = now.strftime("%Hh%M")

    filename = f"logs/semantico-{usuario}-{fecha}-{hora}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("LOG DE ANÁLISIS SEMÁNTICO\n")
        f.write("=" * 50 + "\n\n")

        f.write("CÓDIGO ANALIZADO:\n")
        f.write(codigo + "\n\n")

        f.write("TABLA DE SÍMBOLOS - VARIABLES\n")
        f.write("-" * 50 + "\n")
        if tabla_variables:
            f.write(f"{'NOMBRE':<20}{'TIPO':<12}{'LÍNEA'}\n")
            for nombre, info in tabla_variables.items():
                f.write(f"{nombre:<20}{info['tipo']:<12}{info['linea']}\n")
        else:
            f.write("No se registraron variables.\n")
        f.write("\n")

        f.write("TABLA DE SÍMBOLOS - FUNCIONES\n")
        f.write("-" * 50 + "\n")
        if tabla_funciones:
            f.write(f"{'NOMBRE':<20}{'PARÁMETROS':<14}{'RETORNO':<10}{'LÍNEA'}\n")
            for nombre, info in tabla_funciones.items():
                retorno = "Sí" if info['tiene_retorno'] else "No"
                f.write(
                    f"{nombre:<20}{info['num_parametros']:<14}{retorno:<10}{info['linea']}\n"
                )
        else:
            f.write("No se registraron funciones.\n")
        f.write("\n")

        f.write("ERRORES SEMÁNTICOS ENCONTRADOS:\n")
        f.write("-" * 50 + "\n")
        if SEMANTIC_ERRORS:
            for e in SEMANTIC_ERRORS:
                f.write("- " + e + "\n")
        else:
            f.write("Sin errores semánticos.\n")

    print(f"\n Log semántico generado: {filename}")
    return filename