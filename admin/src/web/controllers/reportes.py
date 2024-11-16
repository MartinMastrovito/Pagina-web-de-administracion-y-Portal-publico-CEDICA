from flask import render_template, request, redirect, flash, Blueprint
from src.core import reportes
from src.core.invoices.utiles import filtrar_cobros, get_empleados_con_cobros
from src.core.auth.decorators import login_required, check
import matplotlib.pyplot as plt
import io
import base64
from datetime import date

bp = Blueprint("reportes", __name__, url_prefix="/reportes")

@bp.get("/")
@login_required
#@check("reporte_index")
def menu():
    return render_template("reportes/menu.html")

@bp.get("/menu_reportes")
@login_required
#@check("reporte_index")
def menu_reportes():
    return render_template("reportes/menu_reportes.html")

@bp.get("/menu_graficos")
@login_required
#@check("reporte_index")
def menu_graficos():
    return render_template("reportes/menu_graficos.html")

@bp.route("/ranking_propuestas")
@login_required
#@check("show_reporte")
def ranking_propuestas():
    ranking = reportes.obtener_ranking_propuestas()
    return render_template("reportes/ranking_propuestas.html", ranking=ranking)

@bp.route('/graficos/becados_grafico')
@login_required
#@check("show_reporte")
def grafico_becados():
    becados, no_becados = reportes.torta_becados()

    labels = []
    sizes = []
    colors = []
    
    if becados:
        labels.append('Becados')
        sizes.append(becados)
        colors.append('#4CAF50')
        
    if no_becados:
        labels.append('No Becados')
        sizes.append(no_becados)
        colors.append('#FFC107')
    
    if not sizes:
        labels = ["Sin datos de becas"]
        sizes = [1]
        colors = ['#D3D3D3']

    plt.figure(figsize=(7, 7))
    # Crear el gráfico de dona con un ancho de dona especificado por 'width'
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, wedgeprops={'width': 0.3})
    plt.axis('equal')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("reportes/grafico_becados.html", plot_url=plot_url)

@bp.route('/graficos/discapacidades_totales')
@login_required
#@check("show_reporte")
def grafico_discapacidades_totales():
    discapacitados_count, no_discapacitados_count = reportes.contador_discapacidades()

    labels = ['Discapacitados', 'No Discapacitados']
    values = [discapacitados_count or 0, no_discapacitados_count or 0]
    colors = ['#FF5733', '#33FF57']

    if not any(values):
        labels = ['Sin datos']
        values = [1]
        colors = ['#D3D3D3']

    plt.figure(figsize=(7, 7))
    # Usamos plt.pie() para crear un gráfico de torta
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.axis('equal')  # Para asegurarnos que el gráfico se vea circular

    # Guardar gráfico como imagen en base64
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("reportes/grafico_discapacidades.html", plot_url=plot_url)

@bp.route('/graficos/tipo_discapacidad')
@login_required
#@check("show_reporte")
def grafico_tipo_discapacidad():
    tipos_discapacidad = reportes.tipo_discapacidad()

    # Filtrar los tipos de discapacidad vacíos para evitar mostrar "Sin datos"
    tipos_discapacidad = [tipo for tipo in tipos_discapacidad if tipo[0] is not None]

    # Si no hay datos después de filtrar, asignamos una lista vacía
    if not tipos_discapacidad:
        return render_template("reportes/grafico_tipo_discapacidad.html", plot_url=None)

    # Separar los datos en etiquetas (tipos de discapacidad) y tamaños (conteos)
    labels = [tipo[0] if tipo[0] else "Sin datos" for tipo in tipos_discapacidad]
    sizes = [tipo[1] for tipo in tipos_discapacidad]

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(labels, sizes, color=['#FF5733', '#33FF57', '#3357FF', '#FF33A6'][:len(labels)])

    # Añadir etiquetas y título
    plt.xlabel('Tipo de Discapacidad')
    plt.ylabel('Cantidad de Registros')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Ajustar el gráfico para que no se solapen las etiquetas
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Guardar el gráfico como imagen y convertirlo a base64
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Renderizar la plantilla y pasar el gráfico
    return render_template("reportes/grafico_tipo_discapacidad.html", plot_url=plot_url)

@bp.route('/historico_cobros')
@login_required
#@check("show_reporte")
def historico_cobros():
    fecha_inicio = request.args.get('fecha_inicio', default="2024-01-01", type=str)
    fecha_fin = request.args.get('fecha_fin', default=str(date.today()), type=str)

    fecha_inicio = date.fromisoformat(fecha_inicio)
    fecha_fin = date.fromisoformat(fecha_fin)

    empleados = get_empleados_con_cobros()

    empleado_id = request.args.get('empleado_id', type=int)
    
    cobros = filtrar_cobros(empleado_id, fecha_inicio, fecha_fin)

    total_cobros = sum(cobro.amount for cobro in cobros)

    return render_template("reportes/historico_cobros.html", cobros=cobros, total_cobros=total_cobros, 
                           fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, empleados=empleados)
    
@bp.route('/deudores')
@login_required
#@check("show_reporte")
def reporte_deudores():
    deudores = reportes.obtener_deudores()
    return render_template('reportes/reporte_deudores.html', deudores=deudores)
