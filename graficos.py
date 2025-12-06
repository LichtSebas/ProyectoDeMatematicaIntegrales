import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def graficar_dos_funciones_2d(func1, func2, a, b, var="x", eje_val=0):

    vals = np.linspace(a, b, 3000)

    # Evaluar func1
    try:
        f1 = func1(vals)
    except:
        f1 = np.array([func1(v) for v in vals])
    if np.isscalar(f1):
        f1 = np.full_like(vals, f1)

    # Evaluar func2
    if func2 is None:
        f2 = np.zeros_like(vals)
    else:
        try:
            f2 = func2(vals)
        except:
            f2 = np.array([func2(v) for v in vals])
        if np.isscalar(f2):
            f2 = np.full_like(vals, f2)

    # Superior e inferior
    arriba = np.maximum(f1, f2)
    abajo  = np.minimum(f1, f2)

    fig, ax = plt.subplots()

    # ============================================
    # VAR = X  →  y = f(x)
    # ============================================
    if var.lower() == "x":

        ax.plot(vals, f1, label="Función 1")
        ax.plot(vals, f2, label="Función 2")

        # Relleno real (sin desplazar nada)
        ax.fill_between(vals, abajo, arriba, alpha=0.3)

        ax.axhline(eje_val, color="gray", linestyle="--", label=f"Eje y={eje_val}")

        ax.set_xlabel("x")
        ax.set_ylabel("y")

    # ============================================
    # VAR = Y  →  x = f(y)
    # ============================================
    else:

        ax.plot(f1, vals, label="Función 1")
        ax.plot(f2, vals, label="Función 2")

        # Relleno real (sin desplazar nada)
        ax.fill_betweenx(vals, abajo, arriba, alpha=0.3)

        ax.axvline(eje_val, color="gray", linestyle="--", label=f"Eje x={eje_val}")

        ax.set_xlabel("x")
        ax.set_ylabel("y")

    ax.legend()
    ax.set_title("Funciones")

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
