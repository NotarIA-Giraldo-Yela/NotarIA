import win32com.client
import cv2
import os
import uuid
import numpy as np
from src.image_processor import crop_document

def scan_document(output_path_front: str, output_path_back: str) -> None:
    """
    Escanea automáticamente ambas caras del documento y guarda las imágenes como PNG.
    Maneja errores si el escáner no está en línea.
    """
    try:
        WIA_DEVICE_TYPE_SCANNER = 1  
        WIA_FORMAT_BMP = "{B96B3CAB-0728-11D3-9D7B-0000F81EF32E}"

        # Detectar escáner disponible
        device_manager = win32com.client.Dispatch("WIA.DeviceManager")
        scanners = [device for device in device_manager.DeviceInfos]

        if not scanners:
            raise Exception("⚠️ No se encontró ningún escáner. Verifica la conexión.")

        # Conectar al primer escáner disponible
        device = scanners[0].Connect()

        # Configurar resolución automática
        for prop in device.Items[0].Properties:
            if prop.Name == "Horizontal Resolution":
                prop.Value = 600
            if prop.Name == "Vertical Resolution":
                prop.Value = 600

        wia_dialog = win32com.client.Dispatch("WIA.CommonDialog")

        # Intentar escanear
        try:
            print("📄 Escaneando parte frontal...")
            temp_bmp_front = f"temp_front_{uuid.uuid4().hex}.bmp"
            image_front = wia_dialog.ShowAcquireImage(WIA_DEVICE_TYPE_SCANNER, WIA_FORMAT_BMP, 4)
            image_front.SaveFile(temp_bmp_front)

            print("📄 Escaneando parte trasera...")
            temp_bmp_back = f"temp_back_{uuid.uuid4().hex}.bmp"
            image_back = wia_dialog.ShowAcquireImage(WIA_DEVICE_TYPE_SCANNER, WIA_FORMAT_BMP, 4)
            image_back.SaveFile(temp_bmp_back)

        except Exception as scan_error:
            raise Exception("⚠️ Error al escanear. Verifica que el escáner esté en línea y configurado correctamente.")

        # Convertir BMP a PNG
        bmp_image_front = cv2.imread(temp_bmp_front)
        bmp_image_back = cv2.imread(temp_bmp_back)

        if bmp_image_front is None or bmp_image_back is None:
            raise Exception("❌ No se pudieron cargar las imágenes escaneadas.")

        # Guardar imágenes finales
        cv2.imwrite(output_path_front, bmp_image_front)
        cv2.imwrite(output_path_back, bmp_image_back)
        print(f"✅ Imágenes guardadas: {output_path_front}, {output_path_back}")

        os.remove(temp_bmp_front)
        os.remove(temp_bmp_back)

    except Exception as e:
        raise Exception(f"❌ Error al escanear el documento: {str(e)}")
