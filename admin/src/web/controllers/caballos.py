#controlador para caballos 

from flask import app 
from flask import request, render_template
from src.core.database import db
from src.core.auth.models import Caballo , TipoJA  

@app.route('/caballos', methods=['GET'])
def listar_caballos():
    # Obtener filtros del request (query params)
    nombre = request.args.get('nombre', default='', type=str)
    tipo_ja = request.args.get('tipo_ja', default='', type=str)

    # Paginación y ordenación
    page = request.args.get('page', 1, type=int)
    per_page = 10
    orden = request.args.get('orden', 'nombre')
    direction = request.args.get('direction', 'asc')

    # Construir la query con filtros
    query = Caballo.query.filter(
        Caballo.nombre.like(f"%{nombre}%"),
        Caballo.tipos_ja.any(TipoJA.nombre.like(f"%{tipo_ja}%"))
    )

    # Aplicar orden ascendente o descendente
    if direction == 'asc':
        query = query.order_by(getattr(Caballo, orden).asc())
    else:
        query = query.order_by(getattr(Caballo, orden).desc())

    # Paginación
    caballos_paginados = query.paginate(page=page, per_page=per_page)

    return render_template('caballos/index.html', caballos=caballos_paginados)

@app.route('/caballos/<int:id>', methods=['GET'])
def mostrar_caballo(id):
    caballo = Caballo.query.get_or_404(id)  # Si no existe, devuelve un 404
    return render_template('caballos/show.html', caballo=caballo)


@app.route('/caballos/nuevo', methods=['GET', 'POST'])
def crear_caballo():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        fecha_nacimiento = request.form['fecha_nacimiento']
        # Otras propiedades...
        caballo = Caballo(nombre=nombre, fecha_nacimiento=fecha_nacimiento)
        db.session.add(caballo)
        db.session.commit()
        return redirect(url_for('listar_caballos'))
    return render_template('caballos/nuevo.html')


@app.route('/caballos/<int:id>/editar', methods=['GET', 'POST'])
def editar_caballo(id):
    caballo = Caballo.query.get_or_404(id)
    if request.method == 'POST':
        caballo.nombre = request.form['nombre']
        caballo.fecha_nacimiento = request.form['fecha_nacimiento']
        # Otras propiedades a actualizar...
        db.session.commit()
        return redirect(url_for('mostrar_caballo', id=caballo.id))
    return render_template('caballos/editar.html', caballo=caballo)


@app.route('/caballos/<int:id>/eliminar', methods=['POST'])
def eliminar_caballo(id):
    caballo = Caballo.query.get_or_404(id)
    db.session.delete(caballo)
    db.session.commit()
    return redirect(url_for('listar_caballos'))
