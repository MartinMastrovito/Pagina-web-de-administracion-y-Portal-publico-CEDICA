from sqlalchemy import func
from src.core.database import db
from src.core.auth.models.model_JyA import JYA

def obtener_ranking_propuestas():
    """
    Obtiene el ranking de propuestas de trabajo agrupadas por frecuencia.

    Returns:
        list: Una lista de tuplas donde cada tupla contiene la propuesta de trabajo y 
              la cantidad de veces que aparece, ordenada de mayor a menor.
    """
    ranking = (
        db.session.query(
            JYA.propuesta_trabajo, 
            func.count(JYA.propuesta_trabajo).label("cantidad")
        )
        .group_by(JYA.propuesta_trabajo)
        .order_by(func.count(JYA.propuesta_trabajo).desc()).filter_by(eliminado=False)
        .all()
    )
    return ranking

def torta_becados():
    """
    Calcula la cantidad de becados y no becados en el sistema.

    Returns:
        tuple: Una tupla con dos valores:
               - becados: La cantidad de personas becadas.
               - no_becados: La cantidad de personas no becadas.
    """
    becados = db.session.query(func.count()).filter(JYA.eliminado == False, JYA.becado == True).scalar()
    no_becados = db.session.query(func.count()).filter(JYA.eliminado == False, JYA.becado == False).scalar()
    
    return becados, no_becados

def contador_discapacidades():
    """
    Cuenta la cantidad de personas con y sin certificado de discapacidad.

    Returns:
        tuple: Una tupla con dos valores:
               - discapacitados: La cantidad de personas con certificado de discapacidad.
               - no_discapacitados: La cantidad de personas sin certificado de discapacidad.
    """
    discapacitados = db.session.query(
        func.count(JYA.id)
    ).filter(JYA.eliminado == False, JYA.certificado_discapacidad == True).scalar()
    
    no_discapacitados = db.session.query(
        func.count(JYA.id)
    ).filter(JYA.eliminado == False, JYA.certificado_discapacidad == False).scalar()
    
    return discapacitados, no_discapacitados

def tipo_discapacidad():
    """
    Obtiene la cantidad de personas agrupadas por tipo de discapacidad.

    Returns:
        list: Una lista de tuplas donde cada tupla contiene:
              - tipo_discapacidad: El tipo de discapacidad.
              - cantidad: La cantidad de personas con ese tipo de discapacidad.
    """
    tipos = db.session.query(
        JYA.tipo_discapacidad, 
        func.count(JYA.id)
    ).filter(JYA.eliminado == False, JYA.tipo_discapacidad.isnot(None)) \
     .group_by(JYA.tipo_discapacidad) \
     .all()
    
    return tipos

def obtener_deudores():
    """
    Obtiene una lista de personas que tienen deudas.

    Returns:
        list: Una lista de instancias de `JYA` que representan a los deudores.
    """
    return JYA.query.filter_by(eliminado=False, debts=True).all()