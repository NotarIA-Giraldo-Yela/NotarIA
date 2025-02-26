import win32com.client
import cv2
import os
import uuid
import numpy as np
from src.image_processor import crop_document

def scan_document(output_path_front: str, output_path_back: str) -> None:
    """
    Escanea automáticamente las partes frontal y trasera de un documento a 600 ppp,
    recorta el documento y guarda las imágenes como PNG sin intervención del usuario.

    Args:
        output_path_front (str): Ruta para guardar la parte frontal como PNG.
        output_path_back (str): Ruta para guardar la parte trasera como PNG.
    """
    try:
        WIA_DEVICE_TYPE_SCANNER = 1  # Escáner
        WIA_FORMAT_BMP = "{B96B3CAB-0728-11D3-9D7B-0000F81EF32E}"  # Formato BMP

        # Detectar automáticamente el escáner sin que el usuario tenga que seleccionarlo
        device_manager = win32com.client.Dispatch("WIA.DeviceManager")
        scanners = [device for device in device_manager.DeviceInfos]

        if not scanners:
            raise Exception("⚠️ No se encontró ningún escáner.")

        # Seleccionar el primer escáner disponible (generalmente el único)
        device = scanners[0].Connect()

        # Configurar automáticamente la calidad de imagen a 600 ppp sin intervención del usuario
        for prop in device.Items[0].Properties:
            if prop.Name == "Horizontal Resolution":
                prop.Value = 600
            if prop.Name == "Vertical Resolution":
                prop.Value = 600
            if prop.Name == "Current Intent":  # Configurar calidad fotográfica
                prop.Value = 4  # WIA_INTENT_IMAGE_TYPE_COLOR (mejor calidad de imagen)

        # Crear un diálogo de escaneo sin intervención del usuario
        wia_dialog = win32com.client.Dispatch("WIA.CommonDialog")

        # Escanear parte frontal
        print("📄 Escaneando la parte frontal a 600 ppp...")
        temp_bmp_front = f"temp_front_{uuid.uuid4().hex}.bmp"
        image_front = wia_dialog.ShowAcquireImage(
            DeviceType=WIA_DEVICE_TYPE_SCANNER,
            FormatID=WIA_FORMAT_BMP,
            Intent=4  # Escaneo fotográfico para mejor calidad
        )
        image_front.SaveFile(temp_bmp_front)

        # Escanear parte trasera
        print("📄 Escaneando la parte trasera a 600 ppp...")
        temp_bmp_back = f"temp_back_{uuid.uuid4().hex}.bmp"
        image_back = wia_dialog.ShowAcquireImage(
            DeviceType=WIA_DEVICE_TYPE_SCANNER,
            FormatID=WIA_FORMAT_BMP,
            Intent=4
        )
        image_back.SaveFile(temp_bmp_back)

        # Convertir BMP a PNG y recortar el documento
        bmp_image_front = cv2.imread(temp_bmp_front)
        bmp_image_back = cv2.imread(temp_bmp_back)

        if bmp_image_front is None or bmp_image_back is None:
            raise Exception("❌ No se pudieron cargar las imágenes temporales.")

        # Recortar automáticamente el documento
        cropped_front = crop_document(bmp_image_front)
        cropped_back = crop_document(bmp_image_back)

        # Guardar imágenes en PNG
        cv2.imwrite(output_path_front, cropped_front)
        cv2.imwrite(output_path_back, cropped_back)

        print(f"✅ Parte frontal guardada en: {output_path_front}")
        print(f"✅ Parte trasera guardada en: {output_path_back} (Recortadas correctamente)")

        # Eliminar archivos temporales BMP
        os.remove(temp_bmp_front)
        os.remove(temp_bmp_back)

    except Exception as e:
        raise Exception(f"❌ Error al escanear el documento: {str(e)}")
