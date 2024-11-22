from src.core.auth.models.model_empleado import Empleados

def get_empleados():
    return Empleados.query.all()

def listar_empleados_activos():
    return Empleados.query.filter_by(activo=True).all()