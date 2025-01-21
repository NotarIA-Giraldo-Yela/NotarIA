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
    Extrae datos de las zonas específicas de la parte frontal del documento.

    Args:
        image_path (str): Ruta de la imagen de la parte frontal.

    Returns:
        dict: Datos extraídos de la parte frontal.
    """
    zones = {
        "Numero de doc": (100, 100, 300, 50),
        "Apellidos": (100, 200, 300, 50),
        "Nombres": (100, 300, 300, 50),
    }
    return extract_zones_from_image(image_path, zones)

def extract_zones_back(image_path: str) -> dict:
    """
    Extrae datos de las zonas específicas de la parte trasera del documento.

    Args:
        image_path (str): Ruta de la imagen de la parte trasera.

    Returns:
        dict: Datos extraídos de la parte trasera.
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
    Extrae datos de las zonas especificadas en una imagen.

    Args:
        image_path (str): Ruta de la imagen a procesar.
        zones (dict): Coordenadas de las zonas (x, y, ancho, alto).

    Returns:
        dict: Datos extraídos de la imagen.
    """
    try:
        # Cargar y preprocesar la imagen
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"No se pudo cargar la imagen desde {image_path}")
        image = preprocess_image(image)

        # Extraer texto de cada zona
        extracted_data = {}
        for key, (x, y, w, h) in zones.items():
            zone = image[y:y + h, x:x + w]
            text = pytesseract.image_to_string(zone, lang="spa").strip()
            validated_text = validate_text(key, text)
            extracted_data[key] = validated_text

        return extracted_data
    except Exception as e:
        raise Exception(f"Error al procesar la imagen: {str(e)}")

def validate_text(field: str, text: str) -> str:
    """
    Valida y limpia el texto extraído de una zona específica.

    Args:
        field (str): Campo al que pertenece el texto.
        text (str): Texto extraído.

    Returns:
        str: Texto validado y limpio.
    """
    if field in ["Numero de doc", "Estatura"]:
        # Validar solo números
        return re.sub(r"[^0-9]", "", text)
    elif field in ["RH"]:
        # Validar RH (e.g., O+, A-)
        match = re.match(r"[ABO][+-]", text)
        return match.group() if match else ""
    elif field in ["Apellidos", "Nombres", "Lugar de nacimiento", "Lugar de expedicion"]:
        # Validar texto alfabético con espacios
        return re.sub(r"[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]", "", text)
    elif field in ["Fecha de nacimiento", "Fecha de expedicion"]:
        # Validar fechas en formato dd/mm/yyyy o similar
        match = re.match(r"\d{2}/\d{2}/\d{4}", text)
        return match.group() if match else ""
    elif field in ["Sexo"]:
        # Validar sexo (M o F)
        return text.strip().upper() if text.strip().upper() in ["M", "F"] else ""
    return text

def process_document(front_image: str, back_image: str) -> dict:
    """
    Procesa las partes frontal y trasera del documento.

    Args:
        front_image (str): Ruta de la imagen de la parte frontal.
        back_image (str): Ruta de la imagen de la parte trasera.

    Returns:
        dict: Datos extraídos de ambas partes.
    """
    try:
        front_data = extract_zones_front(front_image)
        back_data = extract_zones_back(back_image)
        return {"Parte Frontal": front_data, "Parte Trasera": back_data}
    except Exception as e:
        raise Exception(f"Error al procesar el documento: {str(e)}")
