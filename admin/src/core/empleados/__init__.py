from src.core.auth.models.model_empleado import Empleados

def get_empleados():
    return Empleados.query.all()