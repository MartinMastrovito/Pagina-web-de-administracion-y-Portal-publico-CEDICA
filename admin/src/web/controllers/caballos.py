from flask import request, render_template, redirect, url_for, flash
from src.core.database import db
from src.core.auth.models import Caballo, TipoJA, MiembroEquipo


@app.route('/caballos', methods=['GET'])
def listar_caballos():
    # Filtros
    nombre = request.args.get('nombre', '', type=str)
    tipo_ja = request.args.get('tipo_ja', '', type=str)

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

    # Ordenar resultados
    if direction == 'asc':
        query = query.order_by(getattr(Caballo, orden).asc())
    else:
        query = query.order_by(getattr(Caballo, orden).desc())

    # Paginación
    caballos_paginados = query.paginate(page=page, per_page=per_page)

    return render_template('caballos/index.html', caballos=caballos_paginados, search=nombre)


@app.route('/caballos/<int:id>', methods=['GET'])
def mostrar_caballo(id):
    caballo = Caballo.query.get_or_404(id)
    return render_template('caballos/show.html', caballo=caballo)


@app.route('/caballos/nuevo', methods=['GET', 'POST'])
def crear_caballo():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        fecha_nacimiento = request.form['fecha_nacimiento']
        sexo = request.form['sexo']
        raza = request.form['raza']
        pelaje = request.form['pelaje']
        tipo_ingreso = request.form['tipo_ingreso']
        fecha_ingreso = request.form['fecha_ingreso']
        sede_asignada = request.form['sede_asignada']

        # Crear nuevo registro de caballo
        nuevo_caballo = Caballo(
            nombre=nombre,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            raza=raza,
            pelaje=pelaje,
            tipo_ingreso=tipo_ingreso,
            fecha_ingreso=fecha_ingreso,
            sede_asignada=sede_asignada
        )

        db.session.add(nuevo_caballo)
        db.session.commit()
        flash('Caballo creado exitosamente.', 'success')
        return redirect(url_for('listar_caballos'))

    # Obtener entrenadores y tipos de J&A
    entrenadores = MiembroEquipo.query.all()
    tipos_ja = TipoJA.query.all()

    return render_template('caballos/nuevo.html', entrenadores=entrenadores, tipos_ja=tipos_ja)


@app.route('/caballos/<int:id>/editar', methods=['GET', 'POST'])
def editar_caballo(id):
    caballo = Caballo.query.get_or_404(id)
    if request.method == 'POST':
        caballo.nombre = request.form['nombre']
        caballo.fecha_nacimiento = request.form['fecha_nacimiento']
        caballo.sexo = request.form['sexo']
        caballo.raza = request.form['raza']
        caballo.pelaje = request.form['pelaje']
        caballo.tipo_ingreso = request.form['tipo_ingreso']
        caballo.fecha_ingreso = request.form['fecha_ingreso']
        caballo.sede_asignada = request.form['sede_asignada']

        # Actualizar entrenadores y tipos de J&A
        entrenadores_ids = request.form.getlist('entrenadores')
        tipos_ja_ids = request.form.getlist('tipos_ja')

        caballo.entrenadores = MiembroEquipo.query.filter(MiembroEquipo.id.in_(entrenadores_ids)).all()
        caballo.tipos_ja = TipoJA.query.filter(TipoJA.id.in_(tipos_ja_ids)).all()

        db.session.commit()
        flash('Caballo actualizado exitosamente.', 'success')
        return redirect(url_for('mostrar_caballo', id=caballo.id))

    entrenadores = MiembroEquipo.query.all()
    tipos_ja = TipoJA.query.all()
    return render_template('caballos/editar.html', caballo=caballo, entrenadores=entrenadores, tipos_ja=tipos_ja)


@app.route('/caballos/<int:id>/eliminar', methods=['POST'])
def eliminar_caballo(id):
    caballo = Caballo.query.get_or_404(id)
    db.session.delete(caballo)
    db.session.commit()
    flash('Caballo eliminado exitosamente.', 'success')
    return redirect(url_for('listar_caballos'))
