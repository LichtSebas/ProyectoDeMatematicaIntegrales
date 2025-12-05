import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def graficar_dos_funciones_2d(func1, func2, a, b, var="x", eje_val=0):

    vals = np.linspace(a, b, 200)

    # Evaluar func1
    try:
        fvals1 = func1(vals)
        if np.isscalar(fvals1):
            fvals1 = np.full_like(vals, fvals1)
    except:
        fvals1 = np.array([func1(v) for v in vals])

    # Evaluar func2
    if func2 is None:
        fvals2 = np.zeros_like(vals)
    else:
        try:
            fvals2 = func2(vals)
            if np.isscalar(fvals2):
                fvals2 = np.full_like(vals, fvals2)
        except:
            fvals2 = np.array([func2(v) for v in vals])

    # Detectar función superior e inferior
    f_arriba = np.maximum(fvals1, fvals2)
    f_abajo = np.minimum(fvals1, fvals2)

    fig, ax = plt.subplots()
    if var == "x":
        ax.plot(vals, f_arriba, label="Función superior")
        ax.plot(vals, f_abajo, label="Función inferior")
        # Relleno entre funciones respecto al eje de referencia
        ax.fill_between(vals, f_abajo - eje_val, f_arriba - eje_val, alpha=0.3)
        ax.axhline(y=eje_val, color='gray', linestyle='--', label=f"Eje y={eje_val}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    else:
        ax.plot(f_arriba, vals, label="Función superior")
        ax.plot(f_abajo, vals, label="Función inferior")
        ax.fill_betweenx(vals, f_abajo - eje_val, f_arriba - eje_val, alpha=0.3)
        ax.axvline(x=eje_val, color='gray', linestyle='--', label=f"Eje x={eje_val}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")

    ax.set_title("Funciones")
    ax.legend()
    canvas = FigureCanvas(fig)
    return canvas

def graficar_solido_entre_funciones(func1, func2, a, b, var="x", eje="X", eje_val=0):
    n = 50
    vals = np.linspace(a, b, n)
    theta = np.linspace(0, 2*np.pi, n)
    Vals, Theta = np.meshgrid(vals, theta)

    fvals1 = func1(Vals)
    fvals2 = func2(Vals)
    fvals = fvals1 - fvals2  # Diferencia para volumen

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # ================================
    # Aquí aplicamos el desplazamiento del eje
    if eje=="X":
        X = Vals
        Y = (fvals - eje_val) * np.cos(Theta) + eje_val
        Z = (fvals - eje_val) * np.sin(Theta)
    else:
        Y = Vals
        X = (fvals - eje_val) * np.cos(Theta)
        Z = (fvals - eje_val) * np.sin(Theta) + eje_val
    # ================================

    ax.plot_surface(X, Y, Z, alpha=0.6, cmap='viridis')
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(f"Sólido entre funciones eje {eje}={eje_val}")
    canvas = FigureCanvas(fig)
    return canvas
