import easyocr
import os
import time

# --- CONFIGURACIÓN KIMAD TECH ---
FOLDER_FOTOS = "fotos_medicinas"
INVENTARIO_FILE = "inventario_kimad.txt"

def banner():
    print(r"""
    ######################################################
    #        👁️  PHARMA-SCAN v1.0 - KIMAD TECH          #
    #         AI Powered Medicine Inventory              #
    ######################################################
    """)

def scan_meds():
    banner()
    
    # 1. Crear carpeta si no existe
    if not os.path.exists(FOLDER_FOTOS):
        os.makedirs(FOLDER_FOTOS)
        print(f"[!] Carpeta '{FOLDER_FOTOS}' creada. Mete tus fotos ahí y reinicia.")
        return

    # 2. Cargar el lector (Español e Inglés)
    print("[*] Cargando Redes Neuronales... (Esto puede tardar)")
    reader = easyocr.Reader(['es', 'en'])
    
    archivos = [f for f in os.listdir(FOLDER_FOTOS) if f.endswith((".jpg", ".png", ".jpeg"))]
    
    if not archivos:
        print(f"[!] No hay fotos en /{FOLDER_FOTOS}. Saca una foto a una caja y guárdala ahí.")
        return

    print(f"[*] Detectadas {len(archivos)} imágenes. Iniciando OCR...\n")

    for foto in archivos:
        print(f"🔍 Escaneando: {foto}...", end="\r")
        path = os.path.join(FOLDER_FOTOS, foto)
        
        # La IA lee la imagen
        resultado = reader.readtext(path, detail=0)
        texto = " ".join(resultado)
        
        # Reporte en pantalla
        print(f"[OK] {foto} -> {texto[:50]}...")
        
        # Guardar en el inventario oficial
        with open(INVENTARIO_FILE, "a") as f:
            f.write(f"Fecha: {time.ctime()} | Archivo: {foto} | Contenido: {texto}\n")

    print(f"\n[✅] Proceso terminado. Revisa '{INVENTARIO_FILE}' para ver el reporte.")

if __name__ == "__main__":
    scan_meds()