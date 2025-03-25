import easyocr
import re
import unicodedata
import openai 
import os
from openai import OpenAI  # Importar la clase cliente

# Inicializar el lector de EasyOCR
reader = easyocr.Reader(['es'], gpu=True)  # Usar GPU

def normalize_text(text: str) -> str:
    """
    Normaliza el texto eliminando tildes y convirtiendo a mayúsculas.
    """
    # Normaliza el texto (NFKD descompone los caracteres acentuados en su base y su acento)
    normalized_text = unicodedata.normalize("NFKD", text)
    # Elimina los caracteres de acentuación
    normalized_text = "".join([c for c in normalized_text if not unicodedata.combining(c)])
    # Convierte a mayúsculas para consistencia
    normalized_text = normalized_text.upper()
    return normalized_text


def extract_text_from_image(image_path):
    """
    Extrae texto de una imagen usando EasyOCR.
    """
    try:
        # Leer texto de la imagen
        result = reader.readtext(image_path)

        # Extraer solo el texto (ignorar las coordenadas)
        text = " ".join([detection[1] for detection in result])
        return text
    except Exception as e:
        raise Exception(f"Error al extraer texto: {str(e)}")

def extract_front_data(text: str) -> dict:
    """
    Extrae datos específicos de la parte frontal: número de documento, apellidos y nombres.
    """
    data = {
        "Número de Documento": "No detectado",
        "Apellidos": "No detectado",
        "Nombres": "No detectado"
    }
    
    text = normalize_text(text)

    # Buscar los apellidos antes de la palabra "APELLIDOS"
    apellidos_match = re.search(r"([A-ZÁÉÍÓÚÑ\s]+)\s+APELLIDOS", text)
    if apellidos_match:
        data["Apellidos"] = apellidos_match.group(1).strip()

    # Buscar los nombres antes de la palabra "NOMBRES"
    nombres_match = re.search(r"APELLIDOS\s+([A-ZÁÉÍÓÚÑ\s]+)\s+NOMBRES", text)
    if nombres_match:
        data["Nombres"] = nombres_match.group(1).strip()

    # Buscar el número de documento después de "NUMERO" y antes de "APELLIDOS"
    numero_match = re.search(r"NUMERO\s+([\d\.\-\s]+)\s" + data["Apellidos"], text)
    if numero_match:
        data["Número de Documento"] = numero_match.group(1).strip()
    

    return data

def extract_back_data(text: str) -> dict:
    """
    Extrae datos específicos de la parte trasera: sexo, fecha de nacimiento, fecha y lugar de expedición.
    """
    data = {
        "Sexo": "No detectado",
        "Fecha de Nacimiento": "No detectado",
        "Fecha de Expedicion": "No detectado",
        "Lugar de Expedicion": "No detectado"
    }

    text = normalize_text(text)

    # Expresiones regulares para extraer los datos
    sexo_match = re.search(r"SEXO\s+([MF])", text)
    if sexo_match:
        data["Sexo"] = sexo_match.group(1)

    fecha_nacimiento_match = re.search(r"FECHA DE NACIMIENTO\s+(\d{2}-[A-Z]{3}-\d{4})", text)
    if fecha_nacimiento_match:
        data["Fecha de Nacimiento"] = fecha_nacimiento_match.group(1)

    # Buscar la fecha y lugar de expedición antes de "FECHA Y LUGAR DE EXPEDICION"
    fecha_expedicion_match = re.search(r"(\d{2}-[A-Z]{3}-\d{4})\s+([A-ZÁÉÍÓÚÑ\s\(\)\.\-]+)\s+FECHA Y LUGAR DE EXPEDICION", text)
    if fecha_expedicion_match:
        data["Fecha de Expedicion"] = fecha_expedicion_match.group(1)
        data["Lugar de Expedicion"] = fecha_expedicion_match.group(2).strip()

    return data


def analizar_cedula_con_ia(texto_frontal, texto_trasero, api_key):
    # Combina ambos textos para dar contexto completo a la IA
    texto_completo = f"""
    TEXTO FRONTAL: {texto_frontal}
    TEXTO TRASERO: {texto_trasero}
    """

    # Instrucciones claras para la IA
    prompt = f"""
    Extrae los siguientes datos de este texto de una cédula colombiana escaneada:
    - Número de documento (elimina puntos si los tiene)
    - Nombres completos
    - Apellidos completos
    - Fecha de nacimiento (formato: DD-MMM-AAAA)
    - Lugar de nacimiento
    - Fecha de expedición (formato: DD-MMM-AAAA)
    - Lugar de expedición

    Devuelve SOLO un diccionario JSON válido, sin explicaciones. Ejemplo:
    {{
        "numero_documento": "1010119190",
        "nombres": "BRAYAN ESTIBEN",
        "apellidos": "GIRALDO LOPEZ",
        "fecha_nacimiento": "19-FEB-2000",
        "lugar_nacimiento": "BOGOTA D.C",
        "fecha_expedicion": "06-ABR-2018",
        "lugar_expedicion": "BOGOTA D.C"
    }}

    Texto a analizar:
    {texto_completo}
    """

    # Inicializa el cliente con tu API key
    client = OpenAI(api_key=api_key)
    
    # Llama a la API de OpenAI (nueva sintaxis)
    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}  # Para asegurar respuesta en JSON
    )

    # Extrae y devuelve el JSON
    try:
        import json
        datos = json.loads(respuesta.choices[0].message.content)
        return datos
    except Exception as e:
        print(f"Error al procesar la respuesta de la IA: {e}")
        return None

def process_document(front_image_path: str, back_image_path: str) -> dict:
    """
    Procesa ambas partes del documento y extrae la información.
    """
    try:
        # Extraer texto de las imágenes
        front_text = extract_text_from_image(front_image_path)
        back_text = extract_text_from_image(back_image_path)

        # Depurar el texto extraído
        print("Texto frontal extraído:", front_text)
        print("Texto trasero extraído:", back_text)

        api_key = os.getenv("OPENAI_API_KEY")

        AI_data = analizar_cedula_con_ia(front_text, back_text, api_key)
        datos = {
            "Parte Frontal": {
                "Número de Documento": AI_data.get('numero_documento', 'No detectado'),
                "Apellidos": AI_data.get('apellidos', 'No detectado'),
                "Nombres": AI_data.get('nombres', 'No detectado')
            },
            "Parte Trasera": {
                "Lugar de Expedicion": AI_data.get('lugar_expedicion', 'No detectado'),
                "Fecha de Expedicion": AI_data.get('fecha_expedicion', 'No detectado')
            }
        }

        print(datos)

        # Extraer datos específicos del texto
        #front_data = extract_front_data(front_text)
        #back_data = extract_back_data(back_text)

        return datos
    
    except Exception as e:
        raise Exception(f"Error al procesar el documento: {str(e)}")

# Ejemplo de uso
if __name__ == "__main__":
    # Procesar el documento
    result = process_document("scanned_front_comprador.png", "scanned_back_comprador.png")

    # Mostrar los resultados
    print("Parte Frontal:", result["Parte Frontal"])
    print("Parte Trasera:", result["Parte Trasera"])