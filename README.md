# MNIST Digit Classifier

Una aplicación gráfica para clasificar dígitos manuscritos (0-9) usando una CNN entrenada en el dataset MNIST.

## Características

✓ **Canvas de dibujo interactivo** - Dibuja en una cuadrícula de 28x28 píxeles
✓ **Predicción en tiempo real** - Presiona PREDICT para clasificar tu dígito
✓ **Visualización de probabilidades** - Muestra los 10 indicadores con el % de confianza (softmax)
✓ **Interfaz profesional** - Desarrollada con PyQt6
✓ **GPU/CPU automático** - Usa GPU si está disponible, sino CPU

## Estructura del Proyecto

```
MNIST-Project/
├── main.py                    ← EJECUTA ESTO para iniciar
├── src/
│   ├── ui/
│   │   ├── canvas.py         (Canvas de dibujo 28x28)
│   │   ├── confidence_bar.py  (Barras de probabilidad)
│   │   └── main_window.py     (Ventana principal)
│   ├── model/
│   │   └── predictor.py       (Carga modelo y predice)
│   └── utils/
│       └── image_processing.py (Preprocesamiento)
├── models/
│   └── modelo_entrenado.pth   ← AQUÍ VA TU MODELO
├── archive/                   (Dataset MNIST original)
└── requirements.txt
```

## Instalación

### 1. Crear y activar envorno virtual
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias
```powershell
pip install -r requirements.txt
```

Esto instala:
- `PyQt6` - Interfaz gráfica
- `torch` - Framework de deep learning
- `torchvision` - Utilitarios de visión
- `numpy` - Procesamiento de arrays
- `Pillow` - Procesamiento de imágenes

### 3. Colocar el modelo entrenado
Guarda tu modelo entrenado en: `models/modelo_entrenado.pth`

**Estructura esperada:**
```
models/
  └── modelo_entrenado.pth     ← Tu archivo de modelo
```

## Cómo se entrena el modelo

El modelo debe ser una CNN entrenada en MNIST con:
- **Input**: Imágenes de 28x28 píxeles (escala de grises)
- **Output**: 10 logits (uno por cada dígito 0-9)
- **Guardar como**: `models/modelo_entrenado.pth` (state_dict de PyTorch)

### Ejemplo de código de entrenamiento:
```python
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Descargar MNIST
train_dataset = datasets.MNIST(root='./archive', train=True, download=True, 
                               transform=transforms.ToTensor())
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

# Tu modelo aquí...
# Entrenar...
# Guardar
torch.save(model.state_dict(), 'models/modelo_entrenado.pth')
```

## Uso de la Aplicación

1. **Ejecutar la aplicación:**
   ```powershell
   python main.py
   ```

2. **Dibujar un dígito**
   - Haz clic y arrastra el ratón en el canvas blanco de la izquierda
   - Puedes dibujar números del 0 al 9

3. **Predecir**
   - Presiona el botón verde **"PREDICT"**
   - La red neuronal clasificará tu dígito
   - Verás las probabilidades en las 10 barras (0-9)

4. **Limpiar**
   - Presiona el botón rojo **"RESET"** para borrar y empezar de nuevo

## Personalizar la Arquitectura del Modelo

Si tu modelo tiene una arquitectura diferente a `SimpleCNN`, modifica en `main.py`:

```python
# En main.py, línea: predictor = Predictor(str(MODEL_PATH), SimpleCNN)
# Reemplaza SimpleCNN con tu clase:

predictor = Predictor(str(MODEL_PATH), TuModeloCNN)
```

Y asegúrate que tu clase tenga el método `forward()` que retorne logits.

## Troubleshooting

### "No se encontró el modelo"
- Verifica que existe: `models/modelo_entrenado.pth`
- Asegúrate que la ruta es correcta

### "Error de CUDA"
- La app automáticamente usa CPU si no hay CUDA disponible
- Actualiza drivers de GPU si quieres usar CUDA

### "ModuleNotFoundError: PyQt6"
- Asegúrate de tener activado el venv: `.\venv\Scripts\Activate.ps1`
- Reinstala: `pip install PyQt6`

## Dependencias Versiones Recomendadas

```
PyQt6>=6.6.0
torch>=2.0.0
torchvision>=0.15.0
numpy>=1.24.0
Pillow>=10.0.0
```

## Notas Técnicas

- **Canvas**: QGraphicsView con dibujo en tiempo real
- **Procesamiento**: Normalización, inversión de colores, centrado
- **Inferencia**: Modo eval del modelo, sin gradientes
- **Salida**: Softmax para probabilidades (0-1)

## Licencia

MIT License

## Autor

Proyecto de clasificación MNIST con PyQt6
