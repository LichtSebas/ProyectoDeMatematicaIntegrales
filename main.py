import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox, QDoubleSpinBox
from funciones import crear_funcion
from calculos import integral_entre_funciones, volumen_entre_funciones, longitud_curva, longitud_dos_curvas
from graficos import graficar_dos_funciones_2d, graficar_solido_entre_funciones

class CalculadoraGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Avanzada de Integrales y Volumen entre Funciones")
        self.setGeometry(100, 100, 1000, 700)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.initUI()

    def initUI(self):
        # Función 1
        self.func1_input = QLineEdit()
        self.func1_input.setPlaceholderText("f(x) o f(y)")
        self.layout.addWidget(QLabel("Función 1:"))
        self.layout.addWidget(self.func1_input)

        self.btn_agregar_func2 = QPushButton("Agregar función 2")
        self.btn_agregar_func2.clicked.connect(self.mostrar_func2)
        self.layout.addWidget(self.btn_agregar_func2)

        # Función 2
        self.func2_input = QLineEdit()
        self.func2_input.setPlaceholderText("g(x) o g(y)")
        self.func2_input.hide()  # Oculto al inicio
        self.layout.addWidget(QLabel("Función 2:"))
        self.layout.addWidget(self.func2_input)


        # Variable independiente
        self.combo_var = QComboBox()
        self.combo_var.addItems(["x","y"])
        self.layout.addWidget(QLabel("Variable independiente:"))
        self.layout.addWidget(self.combo_var)

        # Límites
        limites_layout = QHBoxLayout()
        self.limite_a = QDoubleSpinBox()
        self.limite_a.setRange(-1000,1000)
        self.limite_a.setValue(0)
        self.limite_b = QDoubleSpinBox()
        self.limite_b.setRange(-1000,1000)
        self.limite_b.setValue(2)
        limites_layout.addWidget(QLabel("Límite a:"))
        limites_layout.addWidget(self.limite_a)
        limites_layout.addWidget(QLabel("Límite b:"))
        limites_layout.addWidget(self.limite_b)
        self.layout.addLayout(limites_layout)

        # Tipo de cálculo
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems([
            "Integral de función",
            "Integral entre funciones",
            "Volumen de función",
            "Volumen entre funciones",
            "Longitud de curva",
            "Longitud de 2 funciones"
        ])
        self.layout.addWidget(QLabel("Tipo de cálculo:"))
        self.layout.addWidget(self.combo_tipo)

        # Eje para sólido
        self.combo_eje = QComboBox()
        self.combo_eje.addItems(["X","Y"])
        self.layout.addWidget(QLabel("Eje de revolución (solo sólido):"))
        self.layout.addWidget(self.combo_eje)

        # Eje de referencia (desplazado)
        self.eje_referencia = QDoubleSpinBox()
        self.eje_referencia.setRange(-1000,1000)
        self.eje_referencia.setValue(0)
        self.layout.addWidget(QLabel("Valor del eje de referencia:"))
        self.layout.addWidget(self.eje_referencia)


        # Botón calcular
        self.btn_calcular = QPushButton("Calcular")
        self.btn_calcular.clicked.connect(self.calcular)
        self.layout.addWidget(self.btn_calcular)

        # Resultado
        self.resultado_label = QLabel("")
        self.layout.addWidget(self.resultado_label)

        # Layout gráfico
        self.grafico_layout = QVBoxLayout()
        self.layout.addLayout(self.grafico_layout)

    def calcular(self):
        # Limpiar gráfico anterior
        for i in reversed(range(self.grafico_layout.count())):
            self.grafico_layout.itemAt(i).widget().setParent(None)

        expr1 = self.func1_input.text()
        var = self.combo_var.currentText()

        func1 = crear_funcion(expr1, var)
        func2 = None
        if self.func2_input.isVisible():
            expr2 = self.func2_input.text()
            func2 = crear_funcion(expr2, var)
            if func2 is None:
                self.resultado_label.setText("Función 2 inválida")
                return

        if func1 is None:
            self.resultado_label.setText("Función 1 inválida")
            return

        a = self.limite_a.value()
        b = self.limite_b.value()
        tipo = self.combo_tipo.currentText()
        eje = self.combo_eje.currentText()

        eje_val = self.eje_referencia.value()
        n = 200  # Número de subdivisiones para integración
        # ======================
        # Detección de función superior e inferior
        vals = np.linspace(a, b, 200)
        f1_vals = func1(vals)
        if func2 and tipo in ["Integral entre funciones", "Volumen entre funciones", "Longitud entre funciones"]:
            f_arriba = lambda x: np.maximum(func1(x), func2(x)) - eje_val
            f_abajo = lambda x: np.minimum(func1(x), func2(x)) - eje_val
            usar_func2 = True
        else:
            f_arriba = lambda x: func1(x) - eje_val
            f_abajo = None  # No hay segunda función
            usar_func2 = False

        # ======================

        if tipo=="Integral de función":
            res = integral_entre_funciones(f_arriba, f_abajo, a, b, n=n)
            self.resultado_label.setText(f"Integral de función: {res:.4f}")
            canvas = graficar_dos_funciones_2d(f_arriba, f_abajo, a, b, var, eje_val=eje_val)

        elif tipo=="Integral entre funciones" and func2:
            res = integral_entre_funciones(f_arriba, f_abajo, a, b, n=n)
            self.resultado_label.setText(f"Integral entre funciones: {res:.4f}")
            canvas = graficar_dos_funciones_2d(f_arriba, f_abajo, a, b, var, eje_val=eje_val)

        elif tipo=="Volumen de función":
            res = volumen_entre_funciones(f_arriba, f_abajo, a, b, eje, eje_val)
            self.resultado_label.setText(f"Volumen de función: {res:.4f}")
            canvas = graficar_solido_entre_funciones(f_arriba, f_abajo, a, b, var, eje, eje_val)

        elif tipo=="Volumen entre funciones" and func2:
            res = volumen_entre_funciones(f_arriba, f_abajo, a, b, eje, eje_val)
            self.resultado_label.setText(f"Volumen entre funciones: {res:.4f}")
            canvas = graficar_solido_entre_funciones(f_arriba, f_abajo, a, b, var, eje, eje_val)
        elif tipo=="Longitud de curva":
            res = longitud_curva(f_arriba, a, b)
            self.resultado_label.setText(f"Longitud de curva: {res:.4f}")
            canvas = graficar_dos_funciones_2d(f_arriba, None, a, b, var, eje_val=eje_val)

        elif tipo=="Longitud entre funciones" and func2:
            L1, L2 = longitud_dos_curvas(f_arriba, f_abajo, a, b)
            self.resultado_label.setText(f"Longitud f_arriba: {L1:.4f}, Longitud f_abajo: {L2:.4f}")
            canvas = graficar_dos_funciones_2d(f_arriba, f_abajo, a, b, var, eje_val=eje_val)

        self.grafico_layout.addWidget(canvas)

    def mostrar_func2(self):
        self.func2_input.show()
        self.combo_tipo.clear()
        self.combo_tipo.addItems([
            "Integral de función",
            "Integral entre funciones",
            "Volumen de función",
            "Volumen entre funciones"
        ])

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = CalculadoraGUI()
    window.show()
    sys.exit(app.exec_())
