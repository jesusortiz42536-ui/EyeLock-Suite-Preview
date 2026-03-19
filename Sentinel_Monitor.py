import psutil
import time
import os
import sys

# --- CONFIGURACIÓN TÁCTICA ---
IP_BANEADAS = ["192.168.1.100", "45.33.22.11"] 
LOG_FILE = "sentinel_tactical.log"

# Colores para la terminal
VERDE = "\033[92m"
ROJO = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{VERDE}")
    print(r"""
    ██╗  ██╗██╗███╗   ███╗ █████╗ ██████╗     ████████╗███████╗ ██████╗██╗  ██╗
    ██║ ██╔╝██║████╗ ████║██╔══██╗██╔══██╗    ╚══██╔══╝██╔════╝██╔════╝██║  ██║
    █████╔╝ ██║██╔████╔██║███████║██║  ██║       ██║   █████╗  ██║     ███████║
    ██╔═██╗ ██║██║╚██╔╝██║██╔══██║██║  ██║       ██║   ██╔══╝  ██║     ██╔══██║
    ██║  ██╗██║██║ ╚═╝ ██║██║  ██║██████╔╝       ██║   ███████╗╚██████╗██║  ██║
    ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝        ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝
    """)
    print(f"{CYAN}    [ SENTINEL v2.5 - ACTIVE NETWORK DEFENSE / BY DR. ENCRYPT ]{RESET}\n")

def loading_sequence():
    chars = "/—\|"
    for i in range(15):
        sys.stdout.write(f"\r{VERDE}[*] Inyectando módulos de seguridad... {chars[i % len(chars)]}{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
    print(f"\n{VERDE}[+] BÚNKER BLINDADO. ESCANEO ACTIVO.{RESET}\n")

def obtener_info_proceso(pid):
    try:
        proc = psutil.Process(pid)
        return proc.name(), proc.username()
    except:
        return "Unknown", "N/A"

def monitorear_red():
    banner()
    loading_sequence()
    
    print(f"{CYAN}{'PID':<8} {'PROGRAMA':<20} {'REMOTE IP:PORT':<25} {'STATUS'}{RESET}")
    print("-" * 75)
    
    try:
        while True:
            conexiones = psutil.net_connections(kind='inet')
            for conn in conexiones:
                if conn.status == 'ESTABLISHED':
                    prog, user = obtener_info_proceso(conn.pid)
                    r_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "LISTENING"
                    
                    # Si la IP es sospechosa, resalta en ROJO
                    color_fila = ROJO if (conn.raddr and conn.raddr.ip in IP_BANEADAS) else VERDE
                    
                    print(f"{color_fila}{conn.pid:<8} {prog[:18]:<20} {r_addr:<25} {conn.status}{RESET}")
            
            time.sleep(3) # Más rápido para que se vea el flujo constante
            
    except KeyboardInterrupt:
        print(f"\n{ROJO}[!] Desactivando Sentinel... Conexión cerrada.{RESET}")

if __name__ == "__main__":
    monitorear_red()