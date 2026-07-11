-- =============================================
-- PRUEBA ESPECÍFICA ANALIZADOR SEMÁNTICO (CON ERRORES ACTIVADOS)
-- =============================================
local edad = 20
local nombre = "Nahin"
local activo = true

-- Regla Semántica 1: Variable no declarada (debe dar error)
print(z)          -- Error: variable 'z' no declarada

-- Regla Semántica 2: Función duplicada (debe dar error)
function saludar()
    return "Hola"
end

function saludar()   -- Error: función duplicada
    return "Adios"
end

-- Operaciones de tipo correcto
local suma = edad + 5
local texto = nombre .. " Espinoza"

-- Break dentro de bucle (correcto)
local contador = 0
for contador = 1, 3 do
    if contador == 2 then
        break
    end
end

-- Break fuera de bucle (debe dar error semántico)
break

-- Operación inválida de tipos (debe detectar error)
local error_tipo = nombre + 10   -- string + number

print("=== Prueba Semántica completada ===")