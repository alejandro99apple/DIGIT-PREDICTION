"""
MÓDULO: confidence_bar.py
PROPÓSITO: Crea widgets visuales para mostrar el porcentaje de confianza (probabilidad)
          de cada dígito (0-9) en forma de barras de progreso

FUNCIÓN PRINCIPAL:
- Mostrar un indicador visual para cada una de las 10 clases de dígitos
- Cada barra representa el porcentaje de confianza (salida softmax de la CNN)
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt


class ConfidenceBar(QWidget):
    """
    Widget que muestra las 10 barras de confianza (una por cada dígito 0-9)
    
    ESTRUCTURA:
    [Dígito] [████████░░] [Porcentaje%]
    
    ATRIBUTOS:
    - confidence_bars: Lista de 10 QProgressBar (uno por cada dígito)
    - confidence_labels: Lista de 10 QLabel (para mostrar porcentaje)
    """
    
    def __init__(self):
        """Inicializa el widget con 10 barras de confianza (una por cada dígito)"""
        super().__init__()
        self.initUI()
    
    def initUI(self):
        """Configura la interfaz gráfica"""
        # Layout principal (vertical) que contendrá las 10 barras
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)  # Espacio entre barras
        
        # Listas para almacenar referencias a las barras y etiquetas
        self.confidence_bars = []
        self.confidence_labels = []
        
        # Crear 10 barras (una por cada dígito 0-9)
        for digit in range(10):
            # Layout horizontal para una fila (dígito + barra + porcentaje)
            row_layout = QHBoxLayout()
            
            # Etiqueta del dígito (0, 1, 2, ..., 9)
            digit_label = QLabel(f"{digit}:")
            digit_label.setFixedWidth(30)  # Ancho fijo para alineación
            
            # Barra de progreso
            progress_bar = QProgressBar()
            progress_bar.setValue(0)  # Valor inicial 0%
            progress_bar.setMaximum(100)  # Máximo 100%
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #cfcfcf;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #4CAF50;
                }
            """)
            
            # Etiqueta de porcentaje
            percent_label = QLabel("0%")
            percent_label.setFixedWidth(40)  # Ancho fijo para "100%"
            
            # Añadir elementos a la fila
            row_layout.addWidget(digit_label)
            row_layout.addWidget(progress_bar)
            row_layout.addWidget(percent_label)
            
            # Guardar referencias
            self.confidence_bars.append(progress_bar)
            self.confidence_labels.append(percent_label)
            
            # Añadir fila al layout principal
            main_layout.addLayout(row_layout)
        
        # Establecer el layout
        self.setLayout(main_layout)
    
    def update_confidences(self, confidences):
        """
        Actualiza las barras con nuevos valores de confianza
        
        PARÁMETRO:
        - confidences: Array/lista con 10 valores entre 0 y 1
                      (salida softmax del modelo CNN)
        
        EJEMPLO:
        confidences = [0.01, 0.85, 0.05, 0.02, 0.01, 0.02, 0.01, 0.01, 0.01, 0.01]
        # El 1 tiene 85% de confianza
        """
        # Recorrer cada dígito (0-9)
        for digit in range(10):
            # Obtener el valor de confianza (entre 0 y 1)
            confidence = confidences[digit]
            
            # Convertir a porcentaje (0-100)
            percentage = int(confidence * 100)
            
            # Actualizar la barra de progreso
            self.confidence_bars[digit].setValue(percentage)
            
            # Actualizar la etiqueta de porcentaje
            self.confidence_labels[digit].setText(f"{percentage}%")
    
    def reset(self):
        """
        Reinicia todas las barras a 0%
        Se usa cuando el usuario presiona RESET o dibuja algo nuevo
        """
        for i in range(10):
            self.confidence_bars[i].setValue(0)
            self.confidence_labels[i].setText("0%")
