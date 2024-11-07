def validator_texto(campo):
    """Valida que el campo contenga solo letras, espacios y caracteres especiales permitidos"""
    import re
    patron = r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$'
    return bool(re.match(patron, str(campo)))

def validator_texto_ampliado(campo):
    """Valida que el campo contenga letras, espacios, números y algunos caracteres especiales"""
    import re
    patron = r'^[A-Za-záéíóúÁÉÍÓÚñÑ0-9\s\-\,\.\#]+$'
    return bool(re.match(patron, str(campo)))

def validator_numero(campo):
    """Valida que el campo sea un número positivo"""
    try:
        numero = float(campo)
        return numero >= 0
    except (ValueError, TypeError):
        return False

def validator_dni(campo):
    """Valida que el campo sea un DNI válido (número positivo entre 1000000 y 99999999)"""
    try:
        dni = int(campo)
        return 1000000 <= dni <= 99999999
    except (ValueError, TypeError):
        return False

def validator_edad(campo):
    """Valida que el campo sea una edad válida (entre 18 y 100)"""
    try:
        edad = int(campo)
        return 18 <= edad <= 100
    except (ValueError, TypeError):
        return False

def validator_telefono(campo):
    """Valida que el campo sea un número de teléfono válido (solo números, mínimo 8 dígitos)"""
    try:
        tel = str(campo)
        return tel.isdigit() and len(tel) >= 8
    except (ValueError, TypeError):
        return False

def validator_email(campo):
    """Valida que el campo sea un email válido"""
    import re
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, str(campo)))

def validator_porcentaje(campo):
    """Valida que el campo sea un porcentaje válido (entre 0 y 1)"""
    try:
        porcentaje = float(campo)
        return 0 <= porcentaje <= 1
    except (ValueError, TypeError):
        return False

def validator_fecha(campo):
    """Valida que el campo sea una fecha válida"""
    from datetime import datetime
    try:
        datetime.strptime(str(campo), '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False

def validator_select_bool(campo):
    """Valida que el campo sea un valor booleano válido de select"""
    return campo in [True, False]

def validator_select_opciones(campo, opciones_validas):
    """Valida que el campo esté entre las opciones válidas"""
    return campo in opciones_validas

def validate_jya_form(jya_data):
    """Valida todos los campos del formulario JyA"""
    errores = []
    
    # Validación de campos de texto simple
    campos_texto = [
        ('nombre', 'Nombre'),
        ('apellido', 'Apellido'),
        ('lugar_nacimiento.provincia', 'Provincia de nacimiento'),
        ('domicilio_actual.provincia', 'Provincia actual'),
        ('contacto_emergencia.nombre', 'Nombre del contacto de emergencia'),
        ('institucion_escolar.nombre', 'Nombre de la institución escolar'),
        ('familiar1_nombre', 'Nombre del familiar 1'),
        ('familiar1_apellido', 'Apellido del familiar 1'),
        ('familiar1_parentesco', 'Parentesco del familiar 1'),
        ('familiar2_nombre', 'Nombre del familiar 2'),
        ('familiar2_apellido', 'Apellido del familiar 2'),
        ('familiar2_parentesco', 'Parentesco del familiar 2')
    ]
    
    for campo, nombre in campos_texto:
        if not validator_texto(jya_data.get(campo)):
            errores.append(f"{nombre} contiene caracteres no válidos")

    # Validación de campos numéricos
    if not validator_dni(jya_data.get('dni')):
        errores.append("DNI no válido")
    
    if not validator_edad(jya_data.get('edad')):
        errores.append("Edad debe estar entre 18 y 100 años")
    
    if not validator_telefono(jya_data.get('telefono_actual')):
        errores.append("Teléfono actual no válido")
    
    if not validator_telefono(jya_data.get('contacto_emergencia')["telefono"]):
        errores.append("Teléfono de emergencia no válido")

    # Validación de emails
    if len(jya_data.get("familiares_tutores", [])) > 0:
        if jya_data["familiares_tutores"][0]["email"] and not validator_email(jya_data["familiares_tutores"][0]["email"]):
            errores.append("Email del familiar 1 no válido")

# Verificar si existe un familiar 2 y si su email es válido
    if len(jya_data.get("familiares_tutores", [])) > 1:
        if jya_data["familiares_tutores"][1]["email"] and not validator_email(jya_data["familiares_tutores"][1]["email"]):
            errores.append("Email del familiar 2 no válido")
    
    # Validación de selects booleanos
    campos_bool = ['becado', 'certificado_discapacidad', 'asignacion_familiar', 'pension', 'curatela']
    for campo in campos_bool:
        if not validator_select_bool(jya_data.get(campo)):
            errores.append(f"Campo {campo} debe ser verdadero o falso")

    # Validación de porcentaje de beca
    if jya_data.get('becado') == 'true' and not validator_porcentaje(jya_data.get('porcentaje_beca')):
        errores.append("Porcentaje de beca debe estar entre 0 y 1")

    # Validación de selects con opciones específicas
    if not validator_select_opciones(jya_data.get('tipo_discapacidad'), 
                                   ['Mental', 'Motora', 'Sensorial', 'Visceral', None]):
        errores.append("Tipo de discapacidad no válido")

    if not validator_select_opciones(jya_data.get('sede'), ['CASJ', 'HLP', 'OTRO']):
        errores.append("Sede no válida")

    if not validator_select_opciones(jya_data.get('condicion_trabajo'), ['REGULAR', 'DE BAJA']):
        errores.append("Condición de trabajo no válida")

    # Validación de fecha
    if not validator_fecha(jya_data.get('fecha_nacimiento')):
        errores.append("Fecha de nacimiento no válida")

    return errores