-- Precedencia: la multiplicacion debe evaluarse antes que la suma
local r = 2 + 3 * 4

-- Precedencia con parentesis y potencia (asocia a la derecha)
local r2 = (2 + 3) * 4 ^ 2

-- Operador unario negativo
local x = -5

-- Estructura WHILE basica
local i = 1
while i do
  i = i + 1
end

-- FOR numerico simple: inicio, fin
for i = 1, 10 do
  local x = i
end

-- FOR numerico con paso explicito
for i = 1, 10, 2 do
  local x = i
end

-- Diccionario / table estilo Lua (clave = valor)
local persona = { nombre = "Ana", edad = 20 }

-- Acceso indexado a una tabla
local edad = persona["edad"]

-- Entrada de datos con io.read()
local nombre = io.read()

-- Concatenacion de strings con ..
local saludo = "hola" .. "mundo"

-- Error esperado: falta el END del while
while x do
  local y = 1

-- Error esperado: falta el nombre de la variable
local = 5

-- Error esperado: al FOR le falta el valor final (coma y expresion)
for i = 1 do
  local x = i
end