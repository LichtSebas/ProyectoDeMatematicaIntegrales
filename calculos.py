import numpy as np
from scipy.integrate import simpson
import math

def integral_entre_funciones(func1, func2=None, a=0, b=1, n=100, eje_val=0):
    if n % 2 != 0:
        n += 1
    x = np.linspace(a, b, n+1)
    f1_vals = func1(x)
    if func2:
        f2_vals = func2(x) if func2 is not None else np.zeros_like(f1_vals)
    else:
        f2_vals = np.zeros_like(f1_vals)
    
    y_diff = np.abs(f1_vals - f2_vals)
    return simpson(y_diff, x)

def volumen_entre_funciones(func1, func2, a, b, eje="X", eje_val=0, n=100):
    # Asegurarnos que n sea entero par
    n = int(n)
    if n % 2 != 0:
        n += 1
    
    vals = np.linspace(a, b, n+1)
    
    fvals1 = func1(vals) - eje_val
    fvals2 = func2(vals) - eje_val
    
    # Volumen: pi*(superior^2 - inferior^2)
    integrando = np.pi * (fvals1**2 - fvals2**2)
    
    return simpson(integrando, vals)


def longitud_curva(func, a, b, n=1000):
    """Calcula la longitud de la curva de f(x) entre a y b"""
    x = np.linspace(a, b, n)
    
    # Aproximamos la derivada con diferencia finita
    dx = x[1] - x[0]
    dy = np.gradient(func(x), dx)
    
    integrando = np.sqrt(1 + dy**2)
    L = simpson(integrando, x)
    return L
def longitud_dos_curvas(func1, func2, a, b, n=1000):
    """Calcula la longitud de dos curvas entre a y b"""
    L1 = longitud_curva(func1, a, b, n)
    L2 = longitud_curva(func2, a, b, n)
    return L1, L2
