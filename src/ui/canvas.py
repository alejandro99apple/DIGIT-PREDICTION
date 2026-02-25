"""
MÓDULO: canvas.py
PROPÓSITO: Crea el área de dibujo (canvas) de 28x28 píxeles donde el usuario dibuja el dígito

FUNCIÓN PRINCIPAL:
- Proporciona un widget QGraphicsView donde el usuario puede dibujar con el ratón
- Captura los movimientos del ratón y dibuja líneas en tiempo real
- Almacena la imagen dibujada para procesarla posteriormente
"""

from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPixmap, QPen, QColor, QImage
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
import numpy as np


class DrawingCanvas(QGraphicsView):
    """
    Widget personalizado que permite dibujar en una cuadrícula de 28x28
    
    ATRIBUTOS:
    - pixmap: La imagen actual dibujada en el canvas
    - drawing: Flag que indica si el usuario está dibujando en este momento
    - last_point: Última posición del ratón (para dibujar líneas conectadas)
    """
    
    # Señal que se emite cuando el usuario dibuja algo
    canvas_updated = pyqtSignal()
    
    def __init__(self):
        """Inicializa el canvas con tamaño 28x28 y lo configura para dibujar"""
        super().__init__()
        
        # Tamaño en píxeles del canvas (28x28 para MNIST)
        self.canvas_size = 28
        # Escala visual para que se vea más grande en pantalla (28*20 = 560 píxeles)
        self.scale_factor = 20
        
        # Crea la escena donde se dibuja
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Desactiva las barras de scroll horizontal y vertical
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Configura el tamaño del widget
        display_size = self.canvas_size * self.scale_factor
        self.setFixedSize(display_size, display_size)
        
        # Crea imagen en blanco (fondo blanco es 255)
        self.pixmap = QPixmap(display_size, display_size)
        self.pixmap.fill(Qt.GlobalColor.white)
        self.scene.addPixmap(self.pixmap)
        
        # Variables de estado
        self.drawing = False  # Flag: ¿está el usuario dibujando?
        self.last_point = QPoint()  # Última posición del ratón
        
        # Configura el pen (lápiz) para dibujar
        self.pen = QPen()
        self.pen.setColor(QColor(0, 0, 0))  # Color negro
        self.pen.setWidth(30)  # Grosor del trazo
    
    def mousePressEvent(self, event):
        """
        Se ejecuta cuando el usuario PRESIONA el botón del ratón
        PARÁMETRO: event - Evento del ratón
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True  # Comenzar a dibujar
            # Guardar el punto inicial
            self.last_point = event.pos()
    
    def mouseMoveEvent(self, event):
        """
        Se ejecuta cuando el usuario MUEVE el ratón (mientras dibuja)
        PARÁMETRO: event - Evento del ratón
        """
        if event.buttons() & Qt.MouseButton.LeftButton and self.drawing:
            # Crear un "pintor" para dibujar en el pixmap
            from PyQt6.QtGui import QPainter
            painter = QPainter(self.pixmap)
            painter.setPen(self.pen)
            
            # Dibujar línea conectada desde último punto hasta punto actual
            painter.drawLine(self.last_point, event.pos())
            painter.end()
            
            # Actualizar el punto actual
            self.last_point = event.pos()
            
            # Refrescar la escena visual
            self.scene.clear()
            self.scene.addPixmap(self.pixmap)
            
            # Emitir señal indicando que el canvas se actualizó
            self.canvas_updated.emit()
    
    def mouseReleaseEvent(self, event):
        """
        Se ejecuta cuando el usuario SUELTA el botón del ratón
        PARÁMETRO: event - Evento del ratón
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False  # Dejar de dibujar
    
    def reset(self):
        """
        Limpia el canvas - borra todo lo dibujado
        Se usa cuando el usuario presiona el botón RESET
        """
        # Crear imagen en blanco nuevamente
        self.pixmap.fill(Qt.GlobalColor.white)
        
        # Refrescar la escena
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)
        
        # Emitir señal indicando que el canvas cambió
        self.canvas_updated.emit()
    
    def get_image_array(self):
        """
        RETORNA: Array numpy de 28x28 con los valores de píxeles (0-255)
        
        USO: Esta imagen se preprocesa y se envía al modelo CNN para predicción
        NOTAS:
        - Convierte el QPixmap en un array numpy
        - Escala de 280x280 a 28x28 (dividiendo por 10)
        - La imagen es en escala de grises (valores 0-255)
        """
        # Convertir QPixmap a QImage
        image = self.pixmap.toImage()
        
        # Convertir QImage a array numpy
        width = image.width()
        height = image.height()
        
        # Extrae los datos de píxeles
        ptr = image.bits()
        ptr.setsize(image.sizeInBytes())
        arr = np.array(ptr).reshape(height, width, 4)  # RGBA
        
        # Convertir a escala de grises (usar canal rojo, ya que es blanco/negro)
        gray = arr[:, :, 0]
        
        # Escalar de 280x280 a 28x28
        # Cada píxel de 28x28 corresponde a un bloque de 10x10 en la imagen visual
        scaled = np.zeros((self.canvas_size, self.canvas_size), dtype=np.uint8)
        
        for i in range(self.canvas_size):
            for j in range(self.canvas_size):
                # Extraer el bloque 10x10
                block = gray[i*self.scale_factor:(i+1)*self.scale_factor,
                            j*self.scale_factor:(j+1)*self.scale_factor]
                # Usar el valor promedio del bloque
                scaled[i, j] = int(np.mean(block))
        
        return scaled
