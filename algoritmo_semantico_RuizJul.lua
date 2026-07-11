-- SISTEMA DE REGISTRO DE USUARIOS
-- Pruebas semánticas - Julian Ruiz

local nombre = "Julian"
local apellido = "Ruiz"
local edad = 22
local activo = true
local puntos = 150

-- Operación válida
local total = edad + puntos

-- Concatenación válida
local nombreCompleto = nombre .. apellido

function mostrarInformacion(usuario)

    if activo and true then
        print("Usuario activo")
    else
        print("Usuario inactivo")
    end

    return usuario
end


-- CON ERRORES

-- Error 1: number + string
local errorSuma = edad + nombre

-- Error 2: boolean + number
local errorBoolean = activo + puntos

-- Error 3: concatenación inválida
local errorConcat = edad .. nombre

-- Error 4: break fuera de ciclo
break