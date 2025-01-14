import win32com.client

def list_scanners():
    """
    Lista los escáneres disponibles en el sistema.

    Returns:
        list: Lista de nombres de dispositivos escáner.
    """
    try:
        wia = win32com.client.Dispatch("WIA.DeviceManager")
        scanners = [device.Properties["Name"].Value for device in wia.DeviceInfos]
        return scanners
    except Exception as e:
        raise Exception(f"Error al listar escáneres: {str(e)}")

def scan_document(output_path: str):
    """
    Escanea un documento utilizando WIA y guarda la imagen en la ruta especificada.

    Args:
        output_path (str): Ruta donde se guardará la imagen escaneada (formato BMP recomendado).
    """
    try:
        # Crear un diálogo WIA para seleccionar el escáner
        wia_dialog = win32com.client.Dispatch("WIA.CommonDialog")
        device = wia_dialog.ShowSelectDevice()

        if not device:
            raise Exception("No se seleccionó ningún escáner.")

        # Escanear el documento
        item = device.Items[0]
        img_file = wia_dialog.ShowAcquireImage(
            DeviceType=1,            # 1 = escáner
            FormatID="{B96B3CAB-0728-11D3-9D7B-0000F81EF32E}",  # Formato BMP
            Intent=1,                # Escaneo en color
        )

        # Guardar la imagen escaneada
        img_file.SaveFile(output_path)
        print(f"Documento escaneado guardado en: {output_path}")
    except Exception as e:
        raise Exception(f"Error al escanear el documento: {str(e)}")
