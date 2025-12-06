import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel,
    QComboBox, QDoubleSpinBox, QGroupBox, QTextEdit
)
from funciones import crear_funcion, encontrar_raices
from calculos import integral_entre_funciones, volumen_entre_funciones, longitud_curva, longitud_dos_curvas
from graficos import graficar_dos_funciones_2d, graficar_solido_entre_funciones


class CalculadoraGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💠 Calculadora Avanzada de Funciones — Licht")
        self.setGeometry(100, 100, 1100, 750)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.initUI()

    def initUI(self):

        # ================================
        # 🔵 SECCIÓN 1: FUNCIONES
        # ================================
        group_funciones = QGroupBox("Funciones")
        layout_fun = QVBoxLayout()
        group_funciones.setLayout(layout_fun)

        self.func1_input = QLineEdit()
        self.func1_input.setPlaceholderText("INGRESA TU PRIMERA FUNCION")
        layout_fun.addWidget(QLabel("Función 1:"))
        layout_fun.addWidget(self.func1_input)

        self.btn_agregar_func2 = QPushButton("Agregar función 2")
        self.btn_agregar_func2.clicked.connect(self.mostrar_func2)
        layout_fun.addWidget(self.btn_agregar_func2)

        self.func2_input = QLineEdit()
        self.func2_input.setPlaceholderText("INGRESA TU SEGUNDA FUNCION")
        self.func2_input.hide()
        layout_fun.addWidget(QLabel("Función 2:"))
        layout_fun.addWidget(self.func2_input)

        self.layout.addWidget(group_funciones)

        # ================================
        # 🔵 SECCIÓN 2: PARÁMETROS
        # ================================
        group_params = QGroupBox("Parámetros")
        layout_params = QVBoxLayout()
        group_params.setLayout(layout_params)

        # Variable independiente
        self.combo_var = QComboBox()
        self.combo_var.addItems(["x", "y"])
        layout_params.addWidget(QLabel("Variable independiente:"))
        layout_params.addWidget(self.combo_var)

        # Límites
        lim_layout = QHBoxLayout()
        self.limite_a = QDoubleSpinBox()
        self.limite_a.setRange(-1000, 1000)
        self.limite_a.setValue(0)

        self.limite_b = QDoubleSpinBox()
        self.limite_b.setRange(-1000, 1000)
        self.limite_b.setValue(2)

        lim_layout.addWidget(QLabel("Límite a:"))
        lim_layout.addWidget(self.limite_a)
        lim_layout.addWidget(QLabel("Límite b:"))
        lim_layout.addWidget(self.limite_b)
        layout_params.addLayout(lim_layout)

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
        layout_params.addWidget(QLabel("Tipo de cálculo:"))
        layout_params.addWidget(self.combo_tipo)

        # Eje sólido
        self.combo_eje = QComboBox()
        self.combo_eje.addItems(["X", "Y"])
        layout_params.addWidget(QLabel("Eje de revolución:"))
        layout_params.addWidget(self.combo_eje)

        self.eje_referencia = QDoubleSpinBox()
        self.eje_referencia.setRange(-1000, 1000)
        layout_params.addWidget(QLabel("Eje de referencia:"))
        layout_params.addWidget(self.eje_referencia)

        self.layout.addWidget(group_params)

        # ================================
        # 🔵 SECCIÓN 3: BOTONES
        # ================================
        botones_layout = QHBoxLayout()

        self.btn_calcular = QPushButton("Calcular")
        self.btn_calcular.clicked.connect(self.calcular)

        self.btn_calcular_puntos = QPushButton("Calcular puntos")
        self.btn_calcular_puntos.clicked.connect(self.calcular_puntos)

        botones_layout.addWidget(self.btn_calcular)
        botones_layout.addWidget(self.btn_calcular_puntos)

        self.layout.addLayout(botones_layout)

        # ================================
        # 🔵 SECCIÓN 4: RESULTADOS
        # ================================
        group_res = QGroupBox("Resultado")
        res_layout = QVBoxLayout()
        group_res.setLayout(res_layout)

        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        res_layout.addWidget(self.resultado_text)

        self.layout.addWidget(group_res)

        # ================================
        # 🔵 SECCIÓN 5: GRÁFICO
        # ================================
        group_graph = QGroupBox("Gráfico")
        self.grafico_layout = QVBoxLayout()
        group_graph.setLayout(self.grafico_layout)

        self.layout.addWidget(group_graph)

    # ==========================================================
    #  MÉTODOS EXACTAMENTE IGUALES A LOS TUYOS (salvo prints)
    # ==========================================================
    def calcular(self):
        # Limpiar gráfico anterior
        for i in reversed(range(self.grafico_layout.count())):
            self.grafico_layout.itemAt(i).widget().setParent(None)

        expr1 = self.func1_input.text()
        var = self.combo_var.currentText()

        func1 = crear_funcion(expr1, var)

        expr2 = self.func2_input.text().strip()
        func2_exists = self.func2_input.isVisible() and expr2 != ""

        func2 = crear_funcion(expr2, var) if func2_exists else None


        a = self.limite_a.value()
        b = self.limite_b.value()

        tipo = self.combo_tipo.currentText()
        eje = self.combo_eje.currentText()
        eje_val = self.eje_referencia.value()

        # =============================
        #  FUNCIONES PARA CÁLCULOS
        # =============================
        if func2_exists:
            f_calc_arriba = lambda x: np.maximum(func1(x), func2(x)) - eje_val
            f_calc_abajo  = lambda x: np.minimum(func1(x), func2(x)) - eje_val
        else:
            f_calc_arriba = lambda x: func1(x) - eje_val
            f_calc_abajo  = lambda x: 0   # se usa solo cuando el tipo lo requiere


        # =============================
        #  FUNCIONES PARA GRAFICAR
        #  (NO RESTAMOS NADA AQUÍ)
        # =============================
        f_grafica1 = func1
        f_grafica2 = func2

        # ===== TIPOS DE CÁLCULO =====
        if tipo == "Integral de función":
            res = integral_entre_funciones(f_calc_arriba, f_calc_abajo, a, b)
            self.resultado_text.setText(f"Integral de función:\n{res:.4f}")
            canvas = graficar_dos_funciones_2d(f_grafica1, None, a, b, var, eje_val)

        elif tipo == "Integral entre funciones" and func2:
            res = integral_entre_funciones(f_calc_arriba, f_calc_abajo, a, b)
            self.resultado_text.setText(f"Integral entre funciones:\n{res:.4f}")
            canvas = graficar_dos_funciones_2d(f_grafica1, f_grafica2, a, b, var, eje_val)

        elif tipo == "Volumen de función":
            res = volumen_entre_funciones(f_calc_arriba, lambda x:0, a, b, eje, eje_val)
            self.resultado_text.setText(f"Volumen de función:\n{res:.4f}")
            canvas = graficar_solido_entre_funciones(f_grafica1, lambda x:0, a, b, var, eje, eje_val)

        elif tipo == "Volumen entre funciones" and func2:
            res = volumen_entre_funciones(f_calc_arriba, f_calc_abajo, a, b, eje, eje_val)
            self.resultado_text.setText(f"Volumen entre funciones:\n{res:.4f}")
            canvas = graficar_solido_entre_funciones(f_grafica1, f_grafica2, a, b, var, eje, eje_val)

        elif tipo == "Longitud de curva":
            res = longitud_curva(f_calc_arriba, a, b)
            self.resultado_text.setText(f"Longitud de curva:\n{res:.4f}")
            canvas = graficar_dos_funciones_2d(f_grafica1, None, a, b, var, eje_val)

        elif tipo == "Longitud de 2 funciones":
            L1, L2 = longitud_dos_curvas(f_calc_arriba, f_calc_abajo, a, b)
            self.resultado_text.setText(f"L1: {L1:.4f}\nL2: {L2:.4f}\nSuma = {L1+L2:.4f}")
            canvas = graficar_dos_funciones_2d(f_grafica1, f_grafica2, a, b, var, eje_val)

        self.grafico_layout.addWidget(canvas)


    def calcular_puntos(self):
        expr1 = self.func1_input.text().strip()
        expr2 = self.func2_input.text().strip()

        if expr1 == "" or expr2 == "":
            self.resultado_text.setText("Debes ingresar ambas funciones.")
            return

        var = self.combo_var.currentText()
        f1 = crear_funcion(expr1, var)
        f2 = crear_funcion(expr2, var)

        puntos = encontrar_raices(f1, f2, -1000, 1000)

        if puntos:
            msg = "Puntos de intersección:\n" + "\n".join([f"x = {p}" for p in puntos])
        else:
            msg = "No se encontraron intersecciones."

        self.resultado_text.setText(msg)

    def mostrar_func2(self):
        self.func2_input.show()
        self.combo_tipo.clear()
        self.combo_tipo.addItems([
            "Integral entre funciones",
            "Volumen entre funciones",
            "Longitud de 2 funciones",
            "Integral de función",
            "Volumen de función"
        ])


if __name__=="__main__":
    app = QApplication(sys.argv)
    window = CalculadoraGUI()
    window.show()
    sys.exit(app.exec_())
