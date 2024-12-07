from datetime import date
import io
import base64
import matplotlib.pyplot as plt
from flask import render_template, request, Blueprint
from src.core.auth.decorators import login_required, check
from src.core import reportes
from src.core.invoices.utiles import filtrar_cobros, get_empleados_con_cobros






bp = Blueprint("reportes", __name__, url_prefix="/reportes")

@bp.get("/")
@login_required
@check("reporte_index")
def menu():
    """
    Renderiza el menú principal de reportes.

    Returns:
        Renderizado de la plantilla menu.html.
    """
    return render_template("reportes/menu.html")

@bp.get("/menu_reportes")
@login_required
@check("reporte_index")
def menu_reportes():
    """
    Renderiza el submenú de reportes.

    Returns:
        Renderizado de la plantilla menu_reportes.html.
    """
    return render_template("reportes/menu_reportes.html")

@bp.get("/menu_graficos")
@login_required
@check("reporte_index")
def menu_graficos():
    """
    Renderiza el submenú de gráficos.

    Returns:
        Renderizado de la plantilla menu_graficos.html.
    """
    return render_template("reportes/menu_graficos.html")

@bp.route("/ranking_propuestas")
@login_required
@check("show_reporte")
def ranking_propuestas():
    """
    Muestra el ranking de propuestas.

    Returns:
        Renderizado de la plantilla ranking_propuestas.html con los datos del ranking.
    """
    ranking = reportes.obtener_ranking_propuestas()
    return render_template("reportes/ranking_propuestas.html", ranking=ranking)

@bp.route('/graficos/becados_grafico')
@login_required
@check("show_reporte")
def grafico_becados():
    """
    Genera un gráfico de becados y no becados.

    Returns:
        Renderizado de la plantilla grafico_becados.html con el gráfico generado.
    """
    becados, no_becados = reportes.torta_becados()
    labels, sizes, colors = [], [], []
    
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
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, wedgeprops={'width': 0.3})
    plt.axis('equal')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("reportes/grafico_becados.html", plot_url=plot_url)

@bp.route('/graficos/discapacidades_totales')
@login_required
@check("show_reporte")
def grafico_discapacidades_totales():
    """
    Genera un gráfico de discapacidades totales.

    Returns:
        Renderizado de la plantilla grafico_discapacidades.html con el gráfico generado.
    """
    discapacitados_count, no_discapacitados_count = reportes.contador_discapacidades()
    labels = ['Discapacitados', 'No Discapacitados']
    values = [discapacitados_count or 0, no_discapacitados_count or 0]
    colors = ['#FF5733', '#33FF57']

    if not any(values):
        labels = ['Sin datos']
        values = [1]
        colors = ['#D3D3D3']

    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.axis('equal')

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("reportes/grafico_discapacidades.html", plot_url=plot_url)

@bp.route('/graficos/tipo_discapacidad')
@login_required
@check("show_reporte")
def grafico_tipo_discapacidad():
    """
    Genera un gráfico de tipos de discapacidad.

    Returns:
        Renderizado de la plantilla grafico_tipo_discapacidad.html con el gráfico generado.
    """
    tipos_discapacidad = reportes.tipo_discapacidad()
    tipos_discapacidad = [tipo for tipo in tipos_discapacidad if tipo[0] is not None]
    
    if not tipos_discapacidad:
        plt.figure(figsize=(10, 6))
        plt.bar(["No hay datos"], [1], color=['#D3D3D3'])
        plt.xlabel('Tipo de Discapacidad')
        plt.ylabel('Cantidad de Registros')
        plt.title('Distribución de Tipos de Discapacidad en JYA')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template("reportes/grafico_tipo_discapacidad.html", plot_url=plot_url)

    labels = [tipo[0] if tipo[0] else "Sin datos" for tipo in tipos_discapacidad]
    sizes = [tipo[1] for tipo in tipos_discapacidad]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, sizes, color=['#FF5733', '#33FF57', '#3357FF', '#FF33A6'][:len(labels)])
    plt.xlabel('Tipo de Discapacidad')
    plt.ylabel('Cantidad de Registros')
    plt.title('Distribución de Tipos de Discapacidad en JYA')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("reportes/grafico_tipo_discapacidad.html", plot_url=plot_url)

@bp.route('/historico_cobros')
@login_required
@check("show_reporte")
def historico_cobros():
    """
    Muestra un informe del histórico de cobros entre dos fechas.

    Returns:
        Renderizado de la plantilla historico_cobros.html con los datos del informe.
    """
    fecha_inicio = request.args.get('fecha_inicio', default="2024-01-01", type=str)
    fecha_fin = request.args.get('fecha_fin', default=str(date.today()), type=str)

    fecha_inicio = date.fromisoformat(fecha_inicio)
    fecha_fin = date.fromisoformat(fecha_fin)
    empleados = get_empleados_con_cobros()
    empleado_id = request.args.get('empleado_id', type=int)
    cobros = filtrar_cobros(empleado_id, fecha_inicio, fecha_fin)
    total_cobros = sum(cobro.amount for cobro in cobros)

    return render_template(
        "reportes/historico_cobros.html",
        cobros=cobros,
        total_cobros=total_cobros,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        empleados=empleados
    )
    
@bp.route('/deudores')
@login_required
@check("show_reporte")
def reporte_deudores():
    """
    Muestra el informe de deudores.

    Returns:
        Renderizado de la plantilla reporte_deudores.html con los datos de deudores.
    """
    deudores = reportes.obtener_deudores()
    return render_template('reportes/reporte_deudores.html', deudores=deudores)
