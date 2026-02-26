# MNIST Digit Classifier

A graphical application to classify handwritten digits (0-9) using a CNN trained on the MNIST dataset.

<div align="center">
  <img src="https://github.com/user-attachments/assets/52e2c9d9-5892-45a5-a367-8559b4065bb4" width="400" alt="MNIST Classifier Demo"/>
  <p><i>MNIST Digit Classifier Demo</i></p>
</div>

## Features

https://github.com/user-attachments/assets/11e5e20a-d84b-4789-b8c0-d1bd16d2c9df
![MNIST](https://github.com/user-attachments/assets/52e2c9d9-5892-45a5-a367-8559b4065bb4)
![MNIST](https://github.com/user-attachments/assets/52e2c9d9-5892-45a5-a367-8559b4065bb4)



✓ **Interactive drawing canvas** - Draw on a 28x28 pixel grid
✓ **Real-time prediction** - Press PREDICT to classify your digit
✓ **Probability visualization** - Shows the 10 indicators with confidence percentage (softmax)
✓ **Professional interface** - Built with PyQt6
✓ **Automatic GPU/CPU** - Uses GPU if available, otherwise CPU

## Project Structure

```
MNIST-Project/
├── main.py                    ← RUN THIS to start
├── src/
│   ├── ui/
│   │   ├── canvas.py         (28x28 drawing canvas)
│   │   ├── confidence_bar.py  (Probability bars)
│   │   └── main_window.py     (Main window)
│   ├── model/
│   │   └── predictor.py       (Loads model and predicts)
│   └── utils/
│       └── image_processing.py (Preprocessing)
├── models/
│   └── modelo_entrenado.pth   ← YOUR MODEL GOES HERE
├── archive/                   (Original MNIST dataset)
└── requirements.txt
```

## Installation

### 1. Create and activate virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies
```powershell
pip install -r requirements.txt
```

This installs:
- `PyQt6` - Graphical interface
- `torch` - Deep learning framework
- `torchvision` - Vision utilities
- `numpy` - Array processing
- `Pillow` - Image processing

### 3. Place the trained model
Save your trained model in: `models/modelo_entrenado.pth`

**Expected structure:**
```
models/
  └── modelo_entrenado.pth     ← Your model file
```

## How the Model is Trained

The model must be a CNN trained on MNIST with:
- **Input**: 28x28 pixel images (grayscale)
- **Output**: 10 logits (one for each digit 0-9)
- **Save as**: `models/modelo_entrenado.pth` (PyTorch state_dict)

**To learn how the model was trained, visit:**
📚 [MNIST Model Training Tutorial](https://github.com/alejandro99apple/MNIST-PREDICTION-MODEL.git)


