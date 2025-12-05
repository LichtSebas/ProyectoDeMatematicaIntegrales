def crear_funcion(expr, var="x"):
    """
    Convierte un string en una función lambda segura usando la variable var.
    """
    try:
        import math
        return lambda v: eval(expr, {var: v, "math": math})
    except Exception as e:
        print("Error al crear función:", e)
        return None
