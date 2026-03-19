import psutil
import time
import os

# --- CONFIGURACIÓN DE SEGURIDAD KIMAD ---
# Lista negra: Aquí puedes agregar IPs de atacantes o servidores sospechosos
IP_BANEADAS = ["192.168.1.100", "45.33.22.11"] 
LOG_FILE = "sentinel_alerts.log"

def banner():
    """Muestra el logo de KIMAD Sentinel."""
    print(r"""
    ######################################################
    #          🛡️  KIMAD SENTINEL v2.0 - DEEP SCAN        #
    #            Monitoring Network Connections          #
    ######################################################
    """)

def obtener_nombre_proceso(pid):
    """Obtiene el nombre del programa asociado al PID."""
    try:
        return psutil.Process(pid).name()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return "System/Unknown"

def monitorear_red():
    """Escanea conexiones y rastrea el origen del programa."""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    print(f"[*] Iniciando monitoreo en PC Master...")
    print(f"[*] Guardando alertas en: {LOG_FILE}\n")
    
    # Cabecera de la tabla
    print(f"{'PROGRAMA':<20} {'LOCAL ADDR':<25} {'REMOTE ADDR':<25} {'STATUS'}")
    print("-" * 85)
    
    try:
        while True:
            # Escaneamos conexiones de internet (ipv4 e ipv6)
            conexiones = psutil.net_connections(kind='inet')
            
            for conn in conexiones:
                # Solo analizamos conexiones establecidas
                if conn.status == 'ESTABLISHED':
                    # Info de direcciones
                    l_addr = f"{conn.laddr.ip}:{conn.laddr.port}"
                    r_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                    remote_ip = conn.raddr.ip if conn.raddr else ""
                    
                    # Info del programa
                    nombre_prog = obtener_nombre_proceso(conn.pid)
                    
                    # Verificación de Seguridad
                    if remote_ip in IP_BANEADAS:
                        alerta = f"[⚠️ PELIGRO] {nombre_prog} conectado a IP Bloqueada: {r_addr}"
                        print(f"\033[91m{alerta}\033[0m") # Imprime en rojo si tu terminal lo soporta
                        with open(LOG_FILE, "a") as f:
                            f.write(f"{time.ctime()} - {alerta}\n")
                    else:
                        # Imprime la fila de la tabla
                        print(f"{nombre_prog[:18]:<20} {l_addr:<25} {r_addr:<25} {conn.status}")
            
            # Pausa de 4 segundos para no estresar el procesador
            time.sleep(4)
            
    except KeyboardInterrupt:
        print("\n[!] Sentinel desactivado. Regresando al búnker...")

if __name__ == "__main__":
    monitorear_red()