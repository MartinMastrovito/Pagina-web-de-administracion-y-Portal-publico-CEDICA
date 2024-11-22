from flask import render_template
from dataclasses import dataclass

@dataclass
class Error:
    code: int
    message: str
    description: str 

def not_found_error(e):
    error = Error(404,"Not found","the requested URL was not found on the server.")

    return render_template("error.html",error=error), 404

def internal_server_error(e):
    error = Error(500,"Internal Server Error","The server was unable to complete your request. Please try again later.")
    
    return render_template("error.html", error=error), 500