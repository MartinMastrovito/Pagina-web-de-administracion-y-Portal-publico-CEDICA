from flask import render_template
from dataclasses import dataclass

@dataclass
class Error:
    code: int
    message: str
    description: str 

def not_found_error(e):
    """
    Maneja errores 404 (Not Found) y genera una respuesta personalizada.

    Args:
        e : La excepción generada por Flask al no encontrar un recurso.

    Returns:
        tuple: Una tupla con el contenido renderizado del error y el código HTTP 404.
    """
    error = Error(404,"Not found","the requested URL was not found on the server.")

    return render_template("error.html",error=error), 404

def internal_server_error(e):
    """
    Maneja errores 500 (Internal Server Error) y genera una respuesta personalizada.

    Args:
        e : La excepción generada por Flask al ocurrir un error interno del servidor.

    Returns:
        tuple: Una tupla con el contenido renderizado del error y el código HTTP 500.
    """
    error = Error(500,"Internal Server Error","The server was unable to complete your request. Please try again later.")
    
    return render_template("error.html", error=error), 500