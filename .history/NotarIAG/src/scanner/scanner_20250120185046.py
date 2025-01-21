import win32com.client
import cv2
import os
import uuid

def list_scanners() -> list:
    """
    Lista los escáneres disponibles en el sistema.

    Returns:
        list: Lista de nombres de dispositivos escáner.
    """
    try:
        device_manager = win32com.client.Dispatch("WIA.DeviceManager")
        scanners = [
            device.Properties["Name"].Value for device in device_manager.DeviceInfos
        ]
        return scanners
    except Exception as e:
        raise Exception(f"Error al listar escáneres: {str(e)}")

def scan_document(output_path_front: str, output_path_back: str) -> None:
    """
    Escanea las partes frontal y trasera de un documento y guarda las imágenes como PNG.

    Args:
        output_path_front (str): Ruta para guardar la parte frontal como PNG.
        output_path_back (str): Ruta para guardar la parte trasera como PNG.
    """
    try:
        WIA_DEVICE_TYPE_SCANNER = 1  # Escáner
        WIA_FORMAT_BMP = "{B96B3CAB-0728-11D3-9D7B-0000F81EF32E}"  # Formato BMP

        wia_dialog = win32com.client.Dispatch("WIA.CommonDialog")
        device = wia_dialog.ShowSelectDevice(WIA_DEVICE_TYPE_SCANNER)
        if not device:
            raise Exception("No se seleccionó ningún escáner.")

        # Escanear parte frontal
        print("Escaneando la parte frontal...")
        temp_bmp_front = f"temp_front_{uuid.uuid4().hex}.bmp"
        image_front = wia_dialog.ShowAcquireImage(
            DeviceType=WIA_DEVICE_TYPE_SCANNER,
            FormatID=WIA_FORMAT_BMP,
            Intent=1
        )
        image_front.SaveFile(temp_bmp_front)

        # Escanear parte trasera
        print("Escaneando la parte trasera...")
        temp_bmp_back = f"temp_back_{uuid.uuid4().hex}.bmp"
        image_back = wia_dialog.ShowAcquireImage(
            DeviceType=WIA_DEVICE_TYPE_SCANNER,
            FormatID=WIA_FORMAT_BMP,
            Intent=1
        )
        image_back.SaveFile(temp_bmp_back)

        # Convertir BMP a PNG
        bmp_image_front = cv2.imread(temp_bmp_front)
        bmp_image_back = cv2.imread(temp_bmp_back)

        if bmp_image_front is None or bmp_image_back is None:
            raise Exception("No se pudieron cargar las imágenes temporales.")

        cv2.imwrite(output_path_front, bmp_image_front)
        cv2.imwrite(output_path_back, bmp_image_back)
        print(f"Parte frontal guardada en: {output_path_front}")
        print(f"Parte trasera guardada en: {output_path_back}")

        # Eliminar archivos temporales
        os.remove(temp_bmp_front)
        os.remove(temp_bmp_back)
    except Exception as e:
        raise Exception(f"Error al escanear el documento: {str(e)}")
