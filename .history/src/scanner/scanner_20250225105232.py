import win32com.client
import cv2
import os
import uuid

def scan_document(output_path_front: str, output_path_back: str) -> None:
    """
    Escanea automáticamente ambas caras del documento y guarda las imágenes como PNG.
    Se configura automáticamente la resolución a 600 dpi.
    """
    try:
        WIA_DEVICE_TYPE_SCANNER = 1  
        WIA_FORMAT_BMP = "{B96B3CAB-0728-11D3-9D7B-0000F81EF32E}"

        # Detectar escáner disponible
        wia_dialog = win32com.client.Dispatch("WIA.CommonDialog")
        device = wia_dialog.ShowSelectDevice(WIA_DEVICE_TYPE_SCANNER)

        if not device:
            raise Exception("⚠️ No se seleccionó ningún escáner.")

        print("📄 Configurando escaneo automático a 600 dpi...")
        for prop in device.Items[0].Properties:
            if prop.Name == "Horizontal Resolution":
                prop.Value = 600
            if prop.Name == "Vertical Resolution":
                prop.Value = 600
            if prop.Name == "Current Intent":
                prop.Value = 1  # Escaneo en escala de grises/color

        # Escanear parte frontal
        print("📄 Escaneando parte frontal...")
        temp_bmp_front = f"temp_front_{uuid.uuid4().hex}.bmp"
        image_front = wia_dialog.ShowAcquireImage(WIA_DEVICE_TYPE_SCANNER, WIA_FORMAT_BMP, 4)
        image_front.SaveFile(temp_bmp_front)

        # Escanear parte trasera automáticamente
        print("📄 Escaneando parte trasera...")
        temp_bmp_back = f"temp_back_{uuid.uuid4().hex}.bmp"
        image_back = wia_dialog.ShowAcquireImage(WIA_DEVICE_TYPE_SCANNER, WIA_FORMAT_BMP, 4)
        image_back.SaveFile(temp_bmp_back)

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
