import win32com.client
from PIL import Image
import os
import uuid
from src.templates_handler.folio_reader import PDf_read

def scan_doc(output_pdf_path: str) -> None:
    """
    Escanea un documento y lo guarda directamente como PDF.

    Args:
        output_pdf_path (str): Ruta para guardar el archivo PDF.
    """
    try:
        WIA_DEVICE_TYPE_SCANNER = 1  # Dispositivo de escaneo
        WIA_FORMAT_BMP = "{B96B3CAB-0728-11D3-9D7B-0000F81EF32E}"  # Formato BMP

        # Iniciar el escaneo
        wia_dialog = win32com.client.Dispatch("WIA.CommonDialog")
        device = wia_dialog.ShowSelectDevice(WIA_DEVICE_TYPE_SCANNER)
        if not device:
            raise Exception("No se seleccionó ningún escáner.")

        print("📄 Escaneando documento...")
        temp_bmp = f"temp_scan_{uuid.uuid4().hex}.bmp"
        image = wia_dialog.ShowAcquireImage(DeviceType=WIA_DEVICE_TYPE_SCANNER, FormatID=WIA_FORMAT_BMP, Intent=1)
        image.SaveFile(temp_bmp)

        # Convertir BMP a PDF
        scanned_image = Image.open(temp_bmp)
        pdf_path = output_pdf_path if output_pdf_path.endswith(".pdf") else output_pdf_path + ".pdf"
        
        scanned_image.convert("RGB").save(pdf_path, "PDF")
        print(f"✅ Documento guardado como PDF: {pdf_path}")

        # Eliminar el archivo temporal BMP
        os.remove(temp_bmp)

        datos = PDf_read(pdf_path)

        return datos


    except Exception as e:
        raise Exception(f"❌ Error al escanear el documento: {str(e)}")
