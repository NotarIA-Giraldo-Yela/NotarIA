import pytesseract
import cv2
import re

def extract_zones(image_path: str) -> dict:
    """
    Extrae datos de zonas específicas en un documento.

    Args:
        image_path (str): Ruta de la imagen procesada.

    Returns:
        dict: Datos extraídos de las zonas específicas.
    """
    try:
        # Leer la imagen procesada
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"No se pudo cargar la imagen desde {image_path}")

        # Definir las coordenadas de las zonas (x, y, ancho, alto)
        zones = {
            "Numero de doc": (94, 109, 165, 36),  # Ajustar según tu imagen
            "Apellidos": (33, 136, 221, 36),     # Ajustar según tu imagen
            "Nombres": (34, 183, 221, 36),       # Ajustar según tu imagen
        }

        # Inicializar el resultado
        extracted_data = {}

        for key, (x, y, w, h) in zones.items():
            # Recortar la zona de interés
            zone = image[y:y + h, x:x + w]

            # Aplicar OCR a la zona
            text = pytesseract.image_to_string(zone, lang="spa")
            # Validar el texto extraído según el campo
            if key == "Numero de doc":
                # Solo números (0-9)
                validated_text = re.sub(r"[^0-9]", "", text)  # Elimina cualquier carácter que no sea un dígito
            else:
                # Solo letras (A-Z, a-z, espacios)
                validated_text = re.sub(r"[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]", "", text)  # Elimina caracteres no alfabéticos

            # Almacenar el texto validado
            extracted_data[key] = validated_text.strip()

        return extracted_data
    except Exception as e:
        raise Exception(f"Error al extraer datos de las zonas: {str(e)}")