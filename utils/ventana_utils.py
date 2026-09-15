import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap

def _pantalla_disponible():
    return QGuiApplication.primaryScreen().availableGeometry()


def centrar_ventana(ventana: QWidget, referencia: QWidget = None):
    """
    Centra `ventana` en la pantalla, o dentro de `referencia` si se indica
    (útil para centrar el login sobre la ventana de fondo).
    """
    if referencia is not None:
        area = referencia.geometry()
    else:
        area = _pantalla_disponible()

    x = area.x() + (area.width() - ventana.width()) // 2
    y = area.y() + (area.height() - ventana.height()) // 2
    ventana.move(x, y)


def aplicar_tamano(ventana: QWidget, modo: str = "centrado", ancho_pct: float = 0.7, alto_pct: float = 0.85, referencia: QWidget = None):
    """
    Modo global para dimensionar cualquier ventana. Se llama UNA vez,
    típicamente en el __init__ de cada ventana, antes de mostrarla.

    modo="completo"  -> usa el estado "maximizado" nativo de Qt: se adapta
                         automáticamente a cualquier pantalla/dispositivo,
                         sin calcular píxeles a mano (para la ventana de fondo).
    modo="centrado"  -> toma un porcentaje de la pantalla y se centra
                         (para diálogos como el login).
    """
    if modo == "completo":
        # Qt calcula el tamaño correcto según el monitor real al mostrarla;
        # no hace falta pasarle ningún ancho/alto.
        ventana.setWindowState(Qt.WindowMaximized)

    elif modo == "centrado":
        pantalla = _pantalla_disponible()
        ancho = int(pantalla.width() * ancho_pct)
        alto = int(pantalla.height() * alto_pct)
        ventana.resize(ancho, alto)
        centrar_ventana(ventana, referencia)

    else:
        raise ValueError(f"Modo de tamaño no reconocido: {modo}")
    
def _icono_pixmap(_ruta_icono, nombre_archivo, tamano):
    """Carga un ícono desde RUTA_ICONOS ya escalado; None si no existe."""
    ruta = _ruta_icono(nombre_archivo)
    if not os.path.isfile(ruta):
        return None
    pixmap = QPixmap(ruta)
    if pixmap.isNull():
        return None

    return pixmap.scaledToWidth(
        tamano,
        Qt.SmoothTransformation
    )
    #return pixmap.scaled(tamano, tamano, Qt.KeepAspectRatio, Qt.SmoothTransformation)