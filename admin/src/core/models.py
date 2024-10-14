from core.database import db
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

class Empleados(db.Model):
    __tablename__ = "Empleados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    dni = Column(String, unique=True, index=True)
    domicilio = Column(String)
    email = Column(String, unique=True, index=True)
    localidad = Column(String)
    telefono = Column(String)
    profesion = Column(String)
    puesto = Column(String)
    fecha_inicio = Column(Date)
    fecha_cese = Column(Date, nullable=True)
    contacto_emergencia = Column(String)
    obra_social = Column(String, nullable=True)
    numero_afiliado = Column(String, nullable=True)
    condicion = Column(String)
    activo = Column(bool, default=True)


class Pago(db.Model):
    __tablename__ = 'Pagos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    beneficiario_id = Column(Integer, ForeignKey('empleados.id'), nullable=True) # empleado dado de alta en el sistema si es pago de honorarios, si aplica
    monto = Column(Float, nullable=False)
    tipo_pago = Column(String, nullable=False)  #puede ser tipo: honorarios, proveedor o gastos varios
    description = Column(String, nullable=True)
    
    beneficiary = relationship("Empleados", backref="Pagos")



