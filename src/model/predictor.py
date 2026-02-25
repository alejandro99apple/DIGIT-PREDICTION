"""
MÓDULO: predictor.py
PROPÓSITO: Carga el modelo CNN entrenado y realiza predicciones en las imágenes dibujadas

FUNCIÓN PRINCIPAL:
- Cargar el modelo guardado (modelo Keras .keras)
- Preprocesar la imagen (normalización, reshape)
- Hacer predicción con el modelo
- Extraer las probabilidades usando softmax

ARQUITECTURA DEL MODELO:
- Conv2D(32, kernel_size=(3,3), activation='relu', input_shape=(28,28,1))
- MaxPooling2D(pool_size=(2,2))
- Dropout(0.25)
- Conv2D(64, kernel_size=(3,3), activation='relu')
- MaxPooling2D(pool_size=(2,2))
- Dropout(0.25)
- Flatten()
- Dense(128, activation='relu')
- Dropout(0.5)
- Dense(10, activation='softmax')  <- Output para 10 dígitos
"""

import sys

import numpy as np


class Predictor:
    """
    Clase que gestiona el modelo CNN y realiza predicciones
    
    ATRIBUTOS:
    - model: El modelo CNN cargado (Keras Sequential)
    - is_loaded: Flag indicando si el modelo está cargado correctamente
    """
    
    def __init__(self, model_path):
        """
        Carga el modelo de Keras desde el archivo .keras
        
        PARÁMETRO:
        - model_path: Ruta al archivo .keras del modelo (ej: "models/mnist_model.keras")
        """
        self.model_path = model_path
        self.model = None
        self.is_loaded = False
        self.error_message = None
        
        print(f"[PREDICTOR] Inicializando predictor...")
        print(f"[PREDICTOR] Ruta del modelo: {model_path}")
        
        # Importar Keras
        try:
            import sys
            print("PYTHON EJECUTANDO:", sys.executable)
            print("VERSION:", sys.version)
            print("[PREDICTOR] Importando TensorFlow/Keras...")
            from tensorflow import keras
            print("[PREDICTOR] ✓ TensorFlow importado correctamente")
        except ImportError as e:
            self.error_message = f"Error al importar TensorFlow: {e}"
            print(f"[PREDICTOR] ✗ {self.error_message}")
            return
        
        # Cargar el modelo
        try:
            print(f"[PREDICTOR] Cargando modelo desde: {model_path}")
            self.model = keras.models.load_model(model_path)
            self.is_loaded = True
            print("[PREDICTOR] ✓ Modelo cargado exitosamente")
        except FileNotFoundError:
            self.error_message = f"Archivo no encontrado: {model_path}"
            print(f"[PREDICTOR] ✗ {self.error_message}")
            self.is_loaded = False
        except Exception as e:
            self.error_message = f"Error al cargar el modelo: {str(e)[:150]}"
            print(f"[PREDICTOR] ✗ {self.error_message}")
            self.is_loaded = False
    
    def predict(self, image_array):
        """
        Realiza predicción sobre una imagen
        
        PARÁMETRO:
        - image_array: Array numpy 28x28 con valores 0-255 (fondo blanco, trazo negro)
        
        RETORNA:
        - predicted_digit: Dígito predicho (0-9)
        - confidences: Array con 10 probabilidades (salida softmax)
        """
        if not self.is_loaded:
            if self.error_message:
                print(f"[PREDICTOR] ✗ No se puede predecir: {self.error_message}")
            else:
                print("[PREDICTOR] ✗ Modelo no está cargado")
            return None, None
        
        try:
            # Preprocesar: normalizar y agregar dimensiones
            # Convertir de blanco=fondo a negro=fondo (invertir)
            image = (255 - image_array) / 255.0
            
            # Reshape para el modelo: (1, 28, 28, 1)
            image = image.reshape(1, 28, 28, 1).astype('float32')
            
            # Realizar predicción
            predictions = self.model.predict(image, verbose=0)
            
            # Obtener las probabilidades (ya vienen con softmax)
            confidences = predictions[0]
            
            # Obtener el dígito predicho
            predicted_digit = np.argmax(confidences)
            
            
            return predicted_digit, confidences
            
        except Exception as e:
            print(f"[PREDICTOR] ✗ Error al predecir: {e}")
            return None, None
