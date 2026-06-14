-- ============================================
-- algoritmo1.lua
-- Algoritmo de prueba - Nahin Espinoza
-- Aporte: Números, Strings y Operadores
-- ============================================

-- 1. NÚMEROS: enteros, flotantes, hex, científicos
entero      = 42
flotante    = 3.14
hexadecimal = 0xFF
cientifico  = 2.5e3
cien        = 100

-- 2. STRINGS: comillas dobles y simples con escapes
nombre  = "Nahin Espinoza"
carrera = 'Computacion'
frase   = "El valor es \"especial\""
ruta    = 'C:\Users\nahin'

-- 3. OPERADORES ARITMÉTICOS
suma      = entero + cien
resta     = cien - entero
producto  = flotante * 2
division  = cien / 4
modulo    = cien % 3
potencia  = 2 ^ 8

-- 4. OPERADORES RELACIONALES
r1 = entero == 42
r2 = entero ~= 100
r3 = flotante < 10
r4 = flotante > 2
r5 = cien <= 100
r6 = cien >= 50

-- 5. OPERADORES LÓGICOS
adulto = entero >= 18 and cien <= 200
alt    = entero < 0 or cien > 50
inv    = not adulto
combo  = entero > 0 and not (flotante == 0)

-- 6. CONCATENACIÓN
presentacion = "Hola, soy " .. nombre .. " y el valor es " .. entero