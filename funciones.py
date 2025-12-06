import numpy as np
from scipy.optimize import brentq
def crear_funcion(expr, var="x"):
    import re
    import numpy as np

    # Normalizar potencias
    expr = expr.replace("^", "**")

    # ============================
    # 🔥 Proteger funciones reales
    # ============================
    funciones = ["sin", "sen", "cos", "tan", "sqrt", "log", "exp", "abs"]

    expr = expr.replace("sen", "sin")  # uniformar

    # Proteger funciones exactas
    for f in funciones:
        expr = re.sub(rf"\b{f}\b", f"{f}_fn_", expr)

    # ============================
    # 🔥 Multiplicación implícita segura
    # ============================
    expr = re.sub(r"(\d)([A-Za-z])", r"\1*\2", expr)        # 4x → 4*x
    expr = re.sub(r"([A-Za-z])(\d)", r"\1*\2", expr)        # x4 → x*4
    expr = re.sub(r"(\d)\(", r"\1*(", expr)                 # 3(x) → 3*(x)
    expr = re.sub(r"([A-Za-z])\(", r"\1*(", expr)           # x(y) → x*(y)
    expr = re.sub(r"\)([A-Za-z])", r")*\1", expr)           # (x)y → (x)*y

    # ============================
    # 🔥 Restaurar funciones
    # ============================
    for f in funciones:
        expr = expr.replace(f"{f}_fn_", f)

    # ============================
    # 🔥 Aplicar sin x → sin(x), sqrt x → sqrt(x)
    # ============================
    expr = re.sub(
        r"\b(sin|cos|tan|sqrt|log|exp|abs)\s+([A-Za-z0-9\(])",
        r"\1(\2)",
        expr
    )
   
    # ============================
    # 🔥 ENTORNO SOLO NUMPY (NO MATH)
    # ============================
    entorno = {
    var: 0,
    "x": 0,
    "y": 0,
    "np": np,
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "sqrt": np.sqrt,
    "log": np.log,
    "exp": np.exp,
    "abs": np.abs,
    "pow": np.power,
    "pi": np.pi,
    "e": np.e,
    }


    # ============================
    # 🔥 Función vectorizada
    # ============================
    def f(v):
        arr = np.asarray(v, dtype=float)
        out = eval(expr, {**entorno, var: arr, "x": arr, "y": arr})
        return np.asarray(out, dtype=float)


    return f

def encontrar_raices(f, g, x_min, x_max, pasos=10000):
    """
    Encuentra las raíces de f(x) - g(x) en el intervalo dado.
    Retorna una lista de valores X donde se cruzan.
    """
    h = lambda x: f(x) - g(x)

    xs = np.linspace(x_min, x_max, pasos)
    hs = h(xs)

    raices = []

    for i in range(len(xs) - 1):
        if np.sign(hs[i]) == 0:
            raices.append(xs[i])
        elif np.sign(hs[i]) != np.sign(hs[i+1]):
            try:
                r = brentq(h, xs[i], xs[i+1])
                raices.append(round(float(r), 6))
            except:
                pass

    # Quitar duplicados cercanos
    if raices:
        filtrado = [raices[0]]
        for r in raices[1:]:
            if abs(r - filtrado[-1]) > 1e-3:
                filtrado.append(r)
        return filtrado

    return []