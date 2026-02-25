"""
═══════════════════════════════════════════════════════════════════════════════
ARCHIVO PRINCIPAL: main.py

PROPÓSITO:
Este es el archivo principal que EJECUTAS para iniciar la aplicación.

ESTRUCTURA DEL PROYECTO:
═══════════════════════════════════════════════════════════════════════════════

MINST-Project/
├── main.py                          ← TÚ ESTÁS AQUÍ (punto de entrada)
├── src/
│   ├── ui/
│   │   ├── canvas.py               → Canvas de 28x28 para dibujar
│   │   ├── confidence_bar.py        → Barras de probabilidad (0-9)
│   │   └── main_window.py           → Ventana principal que organiza todo
│   ├── model/
│   │   └── predictor.py            → (Por completar)
│   └── utils/
│       └── image_processing.py      → (Por completar)
├── models/
│   └── modelo_entrenado.pth        ← Aquí va tu modelo después
└── archive/                        (datos MNIST)

═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import os
import tensorflow as tf
from PyQt6.QtWidgets import QApplication

# Importar interfaz gráfica
from src.ui.main_window import MainWindow
# Importar el predictor
from src.model.predictor import Predictor


def main():
    """
    FUNCIÓN PRINCIPAL - Punto de entrada de la aplicación
    
    PASOS:
    1. Crear aplicación PyQt6
    2. Cargar el modelo
    3. Crear la interfaz gráfica
    4. Conectar modelo con interfaz
    5. Mostrar ventana
    6. Ejecutar loop de eventos
    """
    
    print("═" * 70)
    print("MNIST DIGIT CLASSIFIER - Aplicación iniciada")
    print("═" * 70)
    
    # PASO 1: Crear aplicación PyQt6
    app = QApplication(sys.argv)
    
    # PASO 2: Cargar el modelo
    model_path = os.path.join("models", "mnist_cnn_model.keras")
    print("[MAIN] Cargando modelo...")
    predictor = Predictor(model_path)
    
    if not predictor.is_loaded:
        print("[MAIN] ⚠ Advertencia: La aplicación se ejecutará sin modelo")
    
    # PASO 3: Crear interfaz gráfica
    print("[MAIN] Creando interfaz gráfica...")
    window = MainWindow()
    
    # PASO 4: Conectar la predicción con la interfaz
    def handle_prediction(image_array):
        """Función que maneja la predicción cuando el usuario dibuja"""
        predicted_digit, confidences = predictor.predict(image_array)
        if confidences is not None:
            window.update_prediction_results(confidences)
    
    # Conectar la señal del botón PREDICT con el predictor
    window.predict_signal.connect(handle_prediction)
    
    # PASO 5: Mostrar ventana
    window.show()
    print("[MAIN] ✓ Interfaz gráfica mostrada")
    print("[MAIN] Aplicación lista. Dibuja algo y presiona PREDICT...")
    print("═" * 70)
    
    # PASO 6: Ejecutar loop de eventos
    return app.exec()


# ============ PUNTO DE ENTRADA ============
if __name__ == "__main__":
    """
    Cómo ejecutar:
    - Terminal: python main.py
    """
    exit_code = main()
    sys.exit(exit_code)
