import os

def logo():
    print("""
    ######################################################
    #    👁️  EYELOCK SUITE - BY KIMAD TECH  🛡️         #
    #    Security & Automation Solutions (Demo)          #
    ######################################################
    """)

def menu():
    logo()
    print("[1] Pharma-Scan OCR (Inventario Automatizado)")
    print("[2] KIMAD Sentinel (Defensa Activa)")
    print("[3] Crypto-Vault (Cifrado de Archivos)")
    print("[Q] Salir")
    print("\n" + "="*54)
    
    opcion = input("\nSeleccione una App para ver ficha tecnica: ").upper()
    
    if opcion == "1":
        print("\n[INFO] Pharma-Scan: Digitalización masiva con EasyOCR.")
        print("Status: Lógica protegida en servidor local.")
    elif opcion == "2":
        print("\n[INFO] Sentinel: Monitoreo de IPs y bloqueo de Rootkits.")
        print("Status: Desplegado y Activo.")
    elif opcion == "Q":
        exit()
    else:
        print("\nOpción no válida.")

if __name__ == "__main__":
    while True:
        menu()
        input("\nPresione Enter para volver al menú...")
        os.system('cls' if os.name == 'nt' else 'clear')