def dividir(a,b):
    try:
        return(a / b)
    except ZeroDivisionError:
        return "no se puede dividir por cero"
