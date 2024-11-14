from flask import render_template, request, redirect, flash, Blueprint
from src.core import reportes
from src.core.empleados import get_empleados
from src.core.invoices.utiles import filtrar_cobros
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

    labels = ['Becados', 'No Becados']
    sizes = [becados, no_becados]
    colors = ['#4CAF50', '#FFC107']
    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.axis('equal')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    legend = {'Becados': '#4CAF50', 'No Becados': '#FFC107'}

    return render_template("reportes/grafico_becados.html", plot_url=plot_url, legend=legend)

@bp.route('/graficos/discapacidades_totales')
@login_required
#@check("show_reporte")
def grafico_discapacidades_totales():
    discapacitados_count, no_discapacitados_count = reportes.contador_discapacidades()

    labels = ['Discapacitados', 'No Discapacitados']
    sizes = [discapacitados_count, no_discapacitados_count]
    colors = ['#FF5733', '#33FF57']

    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.axis('equal')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    legend = {'Discapacitados': '#FF5733', 'No Discapacitados': '#33FF57'}

    return render_template("reportes/grafico_discapacidades.html", plot_url=plot_url, legend=legend)

@bp.route('/graficos/tipo_discapacidad')
@login_required
#@check("show_reporte")
def grafico_tipo_discapacidad():
    tipo_discapacidad_counts = reportes.tipo_discapacidad()
    
    if tipo_discapacidad_counts:
        labels = [discapacidad[0] for discapacidad in tipo_discapacidad_counts]
        sizes = [discapacidad[1] for discapacidad in tipo_discapacidad_counts]

        colores = ['#FF5733', '#33FF57', '#3357FF', '#FF33A6']

        plt.figure(figsize=(7, 7))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colores)
        plt.axis('equal')

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        hay_datos = True
        data = [hay_datos, plot_url]
    else:
        hay_datos = False
        data = [hay_datos]

    return render_template("reportes/grafico_tipo_discapacidad.html", data=data)

@bp.route('/historico_cobros')
@login_required
#@check("show_reporte")
def historico_cobros():
    fecha_inicio = request.args.get('fecha_inicio', default="2024-01-01", type=str)
    fecha_fin = request.args.get('fecha_fin', default=str(date.today()), type=str)

    fecha_inicio = date.fromisoformat(fecha_inicio)
    fecha_fin = date.fromisoformat(fecha_fin)

    empleados = get_empleados()

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
