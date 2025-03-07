import pytesseract
import cv2
import numpy as np
import re

# Dimensiones estándar del documento
IMAGE_WIDTH = 669
IMAGE_HEIGHT = 425

# Coordenadas de la zona de texto en la parte frontal
ZONE_FRONT = (3, 91, 432, 180)

# Coordenadas de las zonas clave en la parte trasera
ZONES_BACK = {
    "Fecha de nacimiento": (416, 43, 210, 39),
    "Sexo": (460, 138, 93, 37),
    "Lugar de expedicion": (346, 190, 147, 35),
}

def resize_image(image: np.ndarray) -> np.ndarray:
    """ Redimensiona la imagen a 669x425 si no tiene ese tamaño. """
    h, w = image.shape[:2]
    if w != IMAGE_WIDTH or h != IMAGE_HEIGHT:
        print(f"🔄 Redimensionando imagen de {w}x{h} a {IMAGE_WIDTH}x{IMAGE_HEIGHT}...")
        image = cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT), interpolation=cv2.INTER_AREA)
    return image

def show_image(title: str, image: np.ndarray):
    """ Muestra una imagen recortada con un título específico y espera una tecla antes de cerrarla. """
    cv2.imshow(title, image)
    print(f"🖼️ Mostrando imagen: {title} (presiona cualquier tecla para continuar)")
    cv2.waitKey(0)  # Espera indefinidamente hasta que el usuario presione una tecla
    cv2.destroyAllWindows()

def clean_text(text: str, only_numbers=False, only_letters=False) -> str:
    """ Filtra caracteres no deseados, permitiendo solo letras o números según el caso. """
    text = text.strip()
    text = re.sub(r"[^a-zA-Z0-9ÁÉÍÓÚÑáéíóúñ\s.-]", "", text)

    if only_numbers:
        text = re.sub(r"[^0-9]", "", text)
    elif only_letters:
        text = re.sub(r"[^a-zA-ZÁÉÍÓÚÑáéíóúñ\s]", "", text)

    return text

def clean_document_number(text):
    """
    Limpia el número de documento eliminando caracteres no numéricos,
    asegurando que el primer dígito no se pierda.
    """
    # Mantener solo los números y eliminar cualquier otro carácter
    cleaned_text = re.sub(r"[^\d]", "", text)
    
    # Aplicar la corrección solo si tiene 10 o más dígitos
    if len(cleaned_text) >= 10:
        if cleaned_text[0] != "1":
            cleaned_text = "1" + cleaned_text[1:]  # Reemplaza el primer dígito por 1


    # Si el primer dígito es "0", eliminarlo para evitar errores en la interpretación
    cleaned_text = cleaned_text.lstrip("0")

    return cleaned_text

def extract_front_zone(image: np.ndarray) -> dict:
    """ Extrae texto de la parte frontal y muestra la zona recortada. """
    image = resize_image(image)
    x, y, w, h = ZONE_FRONT
    zone = image[y:y+h, x:x+w]

    text = pytesseract.image_to_string(zone, lang="spa", config="--psm 6").strip()
    print(f"🔍 Texto detectado en la parte frontal:\n{text}\n")
    

    return parse_front_text(text)

def parse_front_text(text: str) -> dict:
    """ Analiza el texto detectado y extrae dinámicamente el número de documento, apellidos y nombres. """
    lines = text.split("\n")
    lines = [line.strip() for line in lines if line.strip()]

    numero_doc = "No detectado"
    apellidos = "No detectado"
    nombres = "No detectado"

    # 🚫 Lista de palabras/frases que NO deben estar en Apellidos o Nombres
    palabras_invalidas = [
    # Variaciones de "REPÚBLICA DE COLOMBIA"
    "REPÚBLICA DE COLOMBIA",
    "REPUBLICA DE COLOMBIA",
    "REPUBLICA DE COLOMB1A",  # OCR puede confundir I con 1
    "REPUBLIÇA DE COLOMBIA",  # OCR puede cambiar C por Ç

    # Variaciones de "IDENTIFICACIÓN PERSONAL"
    "IDENTIFICACION PERSONAL",
    "IDENTIFICACIÓN PERSONAL",
    "IDENTIFICAC10N PERSONAL",  # OCR puede confundir I con 1
    "IDENTIFICAC10N PERS0NAL",  # OCR puede confundir O con 0

    # Variaciones de "CÉDULA DE CIUDADANÍA"
    "CÉDULA DE CIUDADANIA",
    "CÉDULA DE CIUDADANÍA",
    "CEDULA DE CIUDADANIA",
    "CEDULA DE CIUDADANÍA",
    "C3DULA DE CIUDADANIA",  # OCR puede confundir E con 3
    "C3DULA DE CIUDADANÍA",
    "CÉDULA D3 CIUDADANIA",  # OCR puede confundir E con 3
    "CÉDULA DE CIUDADAN1A",  # OCR puede confundir I con 1
    "CÉDULA DE CIUD4DANIA",  # OCR puede confundir A con 4

    # Variaciones de "NÚMERO"
    "NUMERO",
    "NÚMERO",
    "NÚM3RO",  # OCR puede confundir E con 3
    "NUM3RO",

    # Variaciones de "NOMBRES"
    "NOMBRES",
    "N0MBRES",  # OCR puede confundir O con 0
    "NOMBR3S",  # OCR puede confundir E con 3
    "NOMBRES.",
    "NOMRES",   # OCR puede omitir letras
   

    # Otras palabras clave que pueden aparecer erróneamente
    "FECHA",
    "EXPEDICIÓN",
    "EXPEDICION",
    "EXP3DICIÓN",  # OCR puede confundir E con 3
    "EXP3DICION",
    "LUGAR DE NACIMIENTO",
    "LUGAR DE EXPEDICION",
    "LUGAR DE EXPEDICIÓN",
    "ESTATURA",
    "SEXO"
]


    for line in lines:
        # 🔍 Detectar número de documento
        if numero_doc == "No detectado":
            line = clean_document_number(line)

        match = re.search(r"[\d.]{6,15}", line)
        if match and numero_doc == "No detectado":
            numero_doc = match.group().replace(",", ".")
            numero_doc = match.group().lstrip("0")
 
        
        # 🔍 Detectar apellidos
        elif any(word in line.upper() for word in palabras_invalidas):
            continue  # Si la línea contiene palabras prohibidas, la ignoramos
        elif apellidos == "No detectado" or apellidos == "":
            apellidos = line.upper()
            continue

        # 🔍 Detectar nombres
        elif nombres == "No detectado":
            nombres = line.upper()

    apellidos == clean_text(apellidos)
    nombres == clean_text(nombres)

    return {
        "Número de Documento": numero_doc,
        "Apellidos": apellidos,
        "Nombres": nombres
    }


def extract_zones(image: np.ndarray, zones: dict) -> dict:
    """ Extrae texto de la parte trasera, muestra cada zona recortada y aplica validación. """
    image = resize_image(image)

    extracted_data = {}
    for key, (x, y, w, h) in zones.items():
        zone = image[y:y+h, x:x+w]


        text = pytesseract.image_to_string(zone, lang="spa", config="--psm 6").strip()
        text = clean_text(text)

        # Guardar solo la primera línea detectada en "Sexo" y "Lugar de expedición"
        if key in ["Sexo", "Lugar de expedicion"]:
            text_lines = text.split("\n")
            text = text_lines[0] if text_lines else "No detectado"

        print(f"🔍 Texto detectado en {key}: {text}")  # Depuración
        extracted_data[key] = text

    return validate_fields(extracted_data)


def validate_fields(data: dict) -> dict:
    """ Verifica que los campos tengan valores válidos y corrige errores. """
    valid_sex_values = ["M", "m", "F", "f", "T", "t", "NB"]

    # Validar el campo "Sexo"
    if "Sexo" in data:
        detected_sex = data["Sexo"].upper().strip()
        if detected_sex not in valid_sex_values:
            print(f"⚠️ Valor de 'Sexo' incorrecto detectado: {detected_sex}. Se eliminará.")
            data["Sexo"] = "No detectado"

    # Validar el campo "Lugar de expedición" (solo letras)
    if "Lugar de expedicion" in data:
        data["Lugar de expedicion"] = clean_text(data["Lugar de expedicion"], only_letters=True)
        if not data["Lugar de expedicion"]:
            print("⚠️ 'Lugar de expedición' detectado como vacío o incorrecto. Se eliminará.")
            data["Lugar de expedicion"] = "No detectado"

    return data

def process_document(front_image_path: str, back_image_path: str) -> dict:
    """ Procesa ambas partes del documento y extrae la información. """

    try:
        # 🔄 Asegurar que las imágenes se carguen correctamente con OpenCV
        front_image = cv2.imread(front_image_path)
        back_image = cv2.imread(back_image_path)

        if front_image is None or back_image is None:
            raise Exception("No se pudo cargar una de las imágenes. Verifica que las rutas sean correctas.")

        front_data = extract_front_zone(front_image)
        back_data = extract_zones(back_image, ZONES_BACK)

        return {"Parte Frontal": front_data, "Parte Trasera": back_data}

    except Exception as e:
        raise Exception(f"Error al procesar el documento: {str(e)}")
    
    