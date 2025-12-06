import numpy as np
from scipy.integrate import simpson
import math

def integral_entre_funciones(func1, func2=None, a=0, b=1, n=100, var="X"):
    n = int(n)
    if n % 2 != 0:
        n += 1

    vals = np.linspace(a, b, n+1)

    # Si la variable es Y, debemos llamar func(Y), no func(X)
    if var == "Y":
        x = vals  # pero ahora representa y
    else:
        x = vals

    f1_vals = func1(x)

    if func2 is not None:
        f2_vals = func2(x)
    else:
        f2_vals = np.zeros_like(f1_vals)

    area = np.abs(f1_vals - f2_vals)
    return simpson(area, x)


def volumen_entre_funciones(func1, func2, a, b, var="X", eje="X", eje_val=0, n=100):
    n = int(n)
    if n % 2 != 0:
        n += 1

    vals = np.linspace(a, b, n+1)

    # ────────────────────────────────────────────────
    # VAR = X → integrar en dx
    # VAR = Y → integrar en dy
    # ────────────────────────────────────────────────
    if var == "Y":
        variable = vals     # vals ahora representa Y
    else:
        variable = vals     # vals representa X

    # ────────────────────────────────────────────────
    # RADIO SEGÚN EL EJE DE ROTACIÓN
    # ────────────────────────────────────────────────

    # f_arriba - eje
    R1 = func1(variable) - eje_val
    # f_abajo - eje
    R2 = func2(variable) - eje_val

    integrando = np.pi * (R1**2 - R2**2)

    return simpson(integrando, variable)


def longitud_curva(func, a, b, n=1000):
    """Longitud de arco de f entre a y b (f debe aceptar arrays y devolver arrays)."""
    n = max(3, int(n))
    x = np.linspace(a, b, n)

    y = np.asarray(func(x), dtype=float)   # obligación: array flotante

    dx = x[1] - x[0]
    dy = np.gradient(y, dx)

    integrando = np.sqrt(1.0 + dy**2)

    return simpson(integrando, x)


def longitud_dos_curvas(func1, func2, a, b, n=1000):
    L1 = longitud_curva(func1, a, b, n)
    L2 = longitud_curva(func2, a, b, n)
    return L1, L2
