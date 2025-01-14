import sys
import os

# Añadir la carpeta raíz del proyecto al sistema de búsqueda de módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scanner.scanner import list_scanners, scan_document

def test_scan_document():
    """
    Prueba para escanear un documento y guardarlo como PNG.
    """
    output_path = "data/scanned_document.png"  # Ruta para guardar la imagen
    try:
        print("Iniciando escaneo...")
        scan_document(output_path)
        print(f"El documento ha sido escaneado y guardado como PNG en: {output_path}")
    except Exception as e:
        print(f"Error durante la prueba de escaneo: {str(e)}")

if __name__ == "__main__":
    test_scan_document()
