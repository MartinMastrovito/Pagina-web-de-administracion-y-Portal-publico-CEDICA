import re
from datetime import datetime

# Validador de texto (solo letras, espacios y caracteres especiales permitidos)
def validator_texto(campo):
    patron = r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$'
    return bool(re.match(patron, str(campo)))

# Validador de texto ampliado (letras, números y algunos caracteres especiales)
def validator_texto_ampliado(campo):
    patron = r'^[A-Za-záéíóúÁÉÍÓÚñÑ0-9\s\-\,\.\#]+$'
    return bool(re.match(patron, str(campo)))

# Validador de número positivo
def validator_numero(campo):
    try:
        numero = float(campo)
        return numero >= 0
    except (ValueError, TypeError):
        return False

# Validador de DNI (número entre 1000000 y 99999999)
def validator_dni(campo):
    try:
        dni = int(campo)
        return 1000000 <= dni <= 99999999
    except (ValueError, TypeError):
        return False


# Validador de teléfono (mínimo 8 dígitos)
def validator_telefono(campo):
    try:
        tel = str(campo)
        return tel.isdigit() and len(tel) >= 8
    except (ValueError, TypeError):
        return False

# Validador de email
def validator_email(campo):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, str(campo)))


# Validador de opciones booleanas
def validator_select_bool(campo):
    return campo in [True, False]

# Validador de opciones dentro de un conjunto válido
def validator_select_opciones(campo, opciones_validas):
    return campo in opciones_validas

# Validación del formulario de empleados
def validate_empleado_form(empleado_data):
    errores = []

    # Validación de campos de texto
    campos_texto = [
        ('nombre', 'Nombre'),
        ('apellido', 'Apellido'),
    ]
    
    for campo, nombre in campos_texto:
        if not validator_texto(empleado_data.get(campo)):
            errores.append(f"{nombre} contiene caracteres no válidos")

    # Validación de DNI
    if not validator_dni(empleado_data.get('dni')):
        errores.append("DNI no válido")

     # Validación de domicilio
    if not validator_texto_ampliado(empleado_data.get('domicilio', "")):
        errores.append("Domicilio contiene caracteres no válidos")
    
    # Validación de teléfono
    if not validator_telefono(empleado_data.get('telefono')):
        errores.append("Teléfono no válido")
    
     # Validación de campo activo
    activo = empleado_data.get('activo')
    if not validator_select_bool(activo):
        errores.append("Activo debe ser verdadero o falso")

    # Validación de email
    if not empleado_data.get('email'):
        errores.append("Email no puede estar vacío")
    elif not validator_email(empleado_data.get('email',"")):
        errores.append("Email no valido")

     # Validación de obra social
    if empleado_data.get("obra_social") and not validator_texto(empleado_data["obra_social"]):
        errores.append("Obra social contiene caracteres no válidos")

    

    
    
    return errores
