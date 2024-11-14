from sqlalchemy import func
from src.core.database import db
from src.core.auth.models.model_JyA import JYA

def obtener_ranking_propuestas():
    ranking = (
        db.session.query(JYA.propuesta_trabajo, func.count(JYA.propuesta_trabajo).label("cantidad"))
        .group_by(JYA.propuesta_trabajo)
        .order_by(func.count(JYA.propuesta_trabajo).desc())
        .all()
    )
    return ranking

def torta_becados():
    becados = db.session.query(func.count()).filter(JYA.becado == True).scalar()
    no_becados = db.session.query(func.count()).filter(JYA.becado == False).scalar()
    
    return becados, no_becados

def contador_discapacidades():
    discapacitados = db.session.query(db.func.count(JYA.id)).filter(JYA.certificado_discapacidad == True).scalar()
    no_discapacitados = db.session.query(db.func.count(JYA.id)).filter(JYA.certificado_discapacidad == False).scalar()
    
    return discapacitados, no_discapacitados

def tipo_discapacidad():
    return db.session.query(JYA.tipo_discapacidad, db.func.count(JYA.id)).\
        filter(JYA.certificado_discapacidad == True).\
        group_by(JYA.tipo_discapacidad).all()
        
def obtener_deudores():
    return JYA.query.filter_by(debts=True).all()