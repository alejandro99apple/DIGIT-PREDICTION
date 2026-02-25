"""
MÓDULO: main_window.py
PROPÓSITO: Crea la ventana principal de la aplicación que organiza todos los componentes

ESTRUCTURA:
- Canvas de dibujo (28x28) a la izquierda
- Panel derecho con botones y barras de confianza
- Botones: PREDICT (predicción), RESET (limpiar)
- 10 indicadores de confianza (softmax)

FUNCIÓN PRINCIPAL:
- Orquestar la interfaz gráfica
- Conectar eventos de botones con funciones de predicción
- Mostrar resultados
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from .canvas import DrawingCanvas
from .confidence_bar import ConfidenceBar
from PyQt6.QtGui import QIcon
import numpy as np


class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación MNIST Classifier
    
    COMPONENTES:
    - drawing_canvas: Canvas de 28x28 para que el usuario dibuje
    - confidence_display: Widget que muestra las 10 barras de confianza
    - predict_btn: Botón para predecir
    - reset_btn: Botón para limpiar
    
    SEÑALES:
    - predict_signal: Se emite cuando el usuario presiona PREDICT
    """
    
    # Señal que se emite cuando el usuario quiere hacer una predicción
    predict_signal = pyqtSignal(object)  # Emite la imagen como numpy array
    
    def __init__(self):
        """Inicializa la ventana principal"""
        super().__init__()
        self.live_mode = True
        self.awaiting_first_draw = True
        self.resetting = False
        self.prediction_timer = QTimer(self)
        self.prediction_timer.setInterval(150)
        self.prediction_timer.timeout.connect(self.emit_live_prediction)
        self.initUI()
    
    def initUI(self):
        """Configura la interfaz gráfica"""
        # Título de la ventana
        self.setWindowTitle("MNIST Digit Classifier")

        # Asignar icono a la ventana
        self.setWindowIcon(QIcon("icon.ico"))
        
        # Tamaño de la ventana (no redimensionable) y posición
        self.setGeometry(100, 100, 800, 400)
        
        # Widget central que contendrá todo
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal (horizontal: izquierda canvas, derecha controles)
        main_layout = QHBoxLayout()
        
        # ============ LADO IZQUIERDO: CANVAS DE DIBUJO ============
        left_layout = QVBoxLayout()
        left_layout.addStretch()
        
        # Etiqueta "Draw Digit"
        draw_label = QLabel("Draw Digit (28x28)")
        draw_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        draw_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(draw_label)
        
        # Canvas de dibujo
        self.drawing_canvas = DrawingCanvas()
        self.drawing_canvas.setEnabled(True)
        self.drawing_canvas.canvas_updated.connect(self.on_canvas_updated)
        left_layout.addWidget(self.drawing_canvas, alignment=Qt.AlignmentFlag.AlignCenter)
        
        left_layout.addStretch()
        
        # Añadir layout izquierdo al layout principal
        main_layout.addLayout(left_layout, stretch=1)
        
        # ============ LADO DERECHO: BOTONES Y CONFIANZA ============
        right_layout = QVBoxLayout()
        right_layout.addStretch()
        
        # BOTÓN RESET
        self.reset_btn = QPushButton("RESET")
        self.reset_btn.setFixedHeight(50)
        self.reset_btn.setFixedWidth(150)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                font-size: 14px;
                background-color: #f44336;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #ba0000;
            }
        """)
        # Conectar el botón con la función de reinicio
        self.reset_btn.clicked.connect(self.on_reset_clicked)
        right_layout.addWidget(self.reset_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Separador visual
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setMaximumWidth(150)
        right_layout.addWidget(separator, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Agregar espacio flexible antes del panel de probabilidades
        right_layout.addStretch()
        
        # Etiqueta de "Probabilities"
        prob_label = QLabel("Digit Probabilities:")
        prob_label.setStyleSheet("font-weight: bold; font-size: 12px; margin-top: 10px;")
        prob_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(prob_label)
        
        # Widget con las barras de confianza
        self.confidence_display = ConfidenceBar()
        right_layout.addWidget(self.confidence_display, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Añadir espacio flexible al final
        right_layout.addStretch()
        
        # Añadir layout derecho al layout principal
        main_layout.addLayout(right_layout, stretch=1)
        
        # Establecer el layout principal
        central_widget.setLayout(main_layout)
    
    def on_reset_clicked(self):
        """
        Función que se ejecuta cuando el usuario presiona el botón RESET
        
        PASOS:
        1. Limpiar el canvas (borra el dibujo)
        2. Reiniciar las barras de confianza a 0%
        """
        self.resetting = True
        self.stop_live_prediction()

        # Limpiar canvas
        self.drawing_canvas.reset()
        
        # Limpiar barras de confianza
        self.confidence_display.reset()

        self.drawing_canvas.setEnabled(True)
        self.live_mode = True
        self.awaiting_first_draw = True
        self.resetting = False
    
    def update_prediction_results(self, confidences):
        """
        Actualiza el display con los resultados de la predicción
        
        PARÁMETRO:
        - confidences: Array con 10 valores (0-1) de la salida softmax del modelo
        
        USO:
        - Se llama desde main.py después de que el modelo hace la predicción
        - Actualiza las barras de confianza con los nuevos valores
        """
        self.confidence_display.update_confidences(confidences)

    def on_canvas_updated(self):
        if self.resetting or not self.live_mode or not self.awaiting_first_draw:
            return

        image = self.drawing_canvas.get_image_array()
        if np.any(image < 255):
            self.awaiting_first_draw = False
            self.prediction_timer.start()

    def emit_live_prediction(self):
        if not self.live_mode:
            return

        image = self.drawing_canvas.get_image_array()
        self.predict_signal.emit(image)

    def stop_live_prediction(self):
        if self.prediction_timer.isActive():
            self.prediction_timer.stop()
