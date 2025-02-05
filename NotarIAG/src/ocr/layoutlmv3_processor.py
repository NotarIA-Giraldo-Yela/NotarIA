import pytesseract
import cv2
import numpy as np
import re

# Dimensiones fijas de la imagen
IMAGE_WIDTH = 669
IMAGE_HEIGHT = 425

# Coordenadas fijas de las zonas a extraer (x, y, ancho, alto)
ZONES_FRONT = {
    "Numero de doc": (120, 131, 327, 38),
    "Apellidos": (30, 166, 394, 38),
    "Nombres": (23, 219, 422, 56),
}

ZONES_BACK = {
    "Fecha de nacimiento": (416, 43, 210, 39),
    "Lugar de nacimiento (ciudad)": (239, 70, 328, 32),
    "Lugar de nacimiento (departamento)": (232, 98, 265, 21),
    "Sexo": (460, 138, 93, 31),
    "Fecha de expedicion": (231, 196, 121, 21),
    "Lugar de expedicion": (346, 190, 147, 27),
}

def resize_image(image: np.ndarray) -> np.ndarray:
    """
    Redimensiona la imagen a 669x425 si tiene un tamaño diferente.

    Args:
        image (np.ndarray): Imagen original.

    Returns:
        np.ndarray: Imagen redimensionada a 669x425 píxeles.
    """
    try:
        height, width = image.shape[:2]
        if width != IMAGE_WIDTH or height != IMAGE_HEIGHT:
            print(f"🔄 Redimensionando imagen de {width}x{height} a {IMAGE_WIDTH}x{IMAGE_HEIGHT}...")
            image = cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT), interpolation=cv2.INTER_AREA)
        return image
    except Exception as e:
        raise Exception(f"Error al redimensionar la imagen: {str(e)}")


def validate_text(field: str, text: str) -> str:
    """
    Valida y filtra el texto extraído según el tipo de dato esperado.

    Args:
        field (str): Nombre del campo a validar.
        text (str): Texto extraído del OCR.

    Returns:
        str: Texto validado y filtrado.
    """
    if field == "Numero de doc":
        return re.sub(r"[^0-9]", "", text)  # Solo números

    elif field in ["Apellidos", "Nombres", "Lugar de nacimiento (ciudad)", "Lugar de nacimiento (departamento)", "Lugar de expedicion"]:
        return re.sub(r"[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]", "", text)  # Solo letras y espacios
  
    elif field == "Sexo":
        text = text.strip().upper()
        return text if text in ["M", "F"] else ""  # Solo M o F

    return text  # Si el campo no tiene validación específica, lo devuelve como está.

def extract_zones(image: np.ndarray, zones: dict) -> dict:
    """
    Extrae texto de las zonas fijas en la imagen y aplica validaciones.

    Args:
        image (np.ndarray): Imagen de 669x425 píxeles.
        zones (dict): Diccionario con coordenadas fijas de las zonas.

    Returns:
        dict: Texto extraído y validado de cada zona.
    """
    try:
        extracted_data = {}

        for key, (x, y, w, h) in zones.items():
            # Recortar la zona fija
            zone = image[y:y+h, x:x+w]

            # Aplicar OCR a la zona con configuración optimizada
            text = pytesseract.image_to_string(zone, lang="spa", config="--psm 6").strip()

            # Validar y limpiar el texto extraído
            extracted_data[key] = validate_text(key, text)

        return extracted_data
    except Exception as e:
        raise Exception(f"Error al extraer texto de la imagen: {str(e)}")

def process_document(front_image: np.ndarray, back_image: np.ndarray) -> dict:
    """
    Procesa las partes frontal y trasera del documento para extraer información validada.

    Args:
        front_image (np.ndarray): Imagen de la parte frontal.
        back_image (np.ndarray): Imagen de la parte trasera.

    Returns:
        dict: Datos extraídos y validados de ambas partes.
    """
    try:
        front_data = extract_zones(front_image, ZONES_FRONT)
        back_data = extract_zones(back_image, ZONES_BACK)

        return {"Parte Frontal": front_data, "Parte Trasera": back_data}
    except Exception as e:
        raise Exception(f"Error al procesar el documento: {str(e)}")
