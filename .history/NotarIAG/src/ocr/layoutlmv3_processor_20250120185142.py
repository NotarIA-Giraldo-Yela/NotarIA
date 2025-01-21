import pytesseract
import cv2
import re

def preprocess_image(image):
    """
    Preprocesa la imagen para mejorar la precisión del OCR.
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.medianBlur(image, 3)
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return image

def extract_zones_front(image_path: str) -> dict:
    """
    Extrae datos de la parte frontal del documento.
    """
    zones = {
        "Numero de doc": (100, 100, 300, 50),
        "Apellidos": (100, 200, 300, 50),
        "Nombres": (100, 300, 300, 50),
    }
    return extract_zones_from_image(image_path, zones)

def extract_zones_back(image_path: str) -> dict:
    """
    Extrae datos de la parte trasera del documento.
    """
    zones = {
        "Fecha de nacimiento": (50, 50, 250, 30),
        "Lugar de nacimiento": (50, 100, 400, 30),
        "Estatura": (50, 150, 200, 30),
        "RH": (50, 200, 200, 30),
        "Sexo": (50, 250, 100, 30),
        "Fecha de expedicion": (50, 300, 250, 30),
        "Lugar de expedicion": (50, 350, 400, 30),
    }
    return extract_zones_from_image(image_path, zones)

def extract_zones_from_image(image_path: str, zones: dict) -> dict:
    """
    Extrae texto de las zonas especificadas en una imagen.
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"No se pudo cargar la imagen desde {image_path}")
        image = preprocess_image(image)

        extracted_data = {}
        for key, (x, y, w, h) in zones.items():
            zone = image[y:y + h, x:x + w]
            text = pytesseract.image_to_string(zone, lang="spa").strip()
            extracted_data[key] = text
        return extracted_data
    except Exception as e:
        raise Exception(f"Error al procesar la imagen: {str(e)}")
