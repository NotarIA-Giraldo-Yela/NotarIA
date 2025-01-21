import win32com.client
import cv2
import numpy as np

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

def scan_document(output_path: str) -> None:
    """
    Escanea un documento utilizando WIA y guarda la imagen como PNG.

    Args:
        output_path (str): Ruta donde se guardará la imagen como PNG.
    """
    try:
        # Definir constantes de WIA
        WIA_DEVICE_TYPE_SCANNER = 1  # Escáner
        WIA_FORMAT_BMP = "{B96B3CAB-0728-11D3-9D7B-0000F81EF32E}"  # Formato BMP

        # Inicializar el diálogo WIA
        wia_dialog = win32com.client.Dispatch("WIA.CommonDialog")

        # Seleccionar dispositivo (escáner)
        device = wia_dialog.ShowSelectDevice(WIA_DEVICE_TYPE_SCANNER)
        if not device:
            raise Exception("No se seleccionó ningún escáner.")

        # Escanear documento
        item = device.Items[0]
        image = wia_dialog.ShowAcquireImage(
            DeviceType=WIA_DEVICE_TYPE_SCANNER,
            FormatID=WIA_FORMAT_BMP,
            Intent=1  # Escaneo a color
        )

        # Guardar la imagen como BMP en un archivo temporal
        temp_bmp_path = output_path.replace(".png", ".bmp")
        image.SaveFile(temp_bmp_path)

        # Convertir BMP a PNG usando OpenCV
        bmp_image = cv2.imread(temp_bmp_path)
        if bmp_image is None:
            raise Exception(f"No se pudo cargar la imagen temporal: {temp_bmp_path}")
        cv2.imwrite(output_path, bmp_image)
        print(f"Imagen escaneada guardada como PNG en: {output_path}")
    except Exception as e:
        raise Exception(f"Error al escanear el documento: {str(e)}")
