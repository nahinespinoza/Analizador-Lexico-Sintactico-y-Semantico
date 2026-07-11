--SIN ERRORES
local edad = 22
local estudiante = true

local edad = 22
local estudiante = true

function evaluar(persona)

    if edad >= 18 and estudiante then
        print("Mayor de edad y estudiante")

    elseif edad >= 18 then
        print("Mayor de edad")

    else
        print("Menor de edad")
    end

    return persona
end

--CON ERROR
local edad = 22
local estudiante = true

function evaluar(persona)

    if edad >= 18 and estudiante then
        print("Mayor de edad y estudiante")

    elseif edad >= 18 then
        print("Mayor de edad")

    else
        print("Menor de edad")

    return persona
end